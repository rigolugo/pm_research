"""Latency + impact model: what would we ACTUALLY have paid?

Given a signal detected at t, we fill at the market price at
t + detection_delay, worsened by impact and fees, and we abandon entirely if
the price has chased more than `max_chase` past the leaders' average entry.
Zero-latency runs (delay=0, impact=0) are the upper bound for comparison;
only modeled-latency results count.
"""
from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np
import pandas as pd

from .config import LatencyConfig


@dataclass(frozen=True)
class FillEstimate:
    filled: bool
    fill_price: float
    fill_at: pd.Timestamp
    reason: str = ""


class PriceBook:
    """Fast as-of YES-price lookup per market (prices frame, hourly).

    Lazy-loading variant: instead of groupby-ing the full prices frame
    (15M rows -> 24k Series objects all in RAM simultaneously), we load
    each market's parquet file from disk on first access and cache only
    what we've actually needed. On a t3.micro with a 115-wallet universe
    trading across maybe a few hundred active markets, this keeps peak
    RAM proportional to the active trading universe rather than the full
    24k-market history.

    Falls back to the in-memory prices frame if prices_root is not given
    (synthetic tests, unit tests) — behaviour is identical, just slower
    on large datasets."""

    def __init__(self, prices: pd.DataFrame, markets: pd.DataFrame,
                 prices_root: str | None = None,
                 trades: pd.DataFrame | None = None,
                 freq: str = "1h"):
        self._series: dict[str, pd.Series] = {}
        self._prices_root = prices_root
        if prices_root is None:
            # synthetic / test path: materialise everything up front (small)
            for cid, g in prices.groupby("condition_id"):
                s = g.set_index("ts")["yes_price"].sort_index()
                self._series[cid] = s
        # else: lazy — series loaded on first yes_price_at() call
        self._liq = dict(zip(markets["condition_id"], markets["liquidity_usdc"]))
        # ---- intra-bar worst-case support (optional) ----------------------
        # If raw trades are supplied, PriceBook can price a fill at the
        # direction-adverse extreme among the REAL prints within the fill's
        # bar, instead of the resampled close. Indexed lazily per market. When
        # trades is None this is simply unavailable and callers fall back to the
        # close value — no behaviour change. We precompute per-market YES-price
        # prints once, keyed by condition_id.
        self._freq = freq
        # Distinguish "no trades SOURCE supplied at all" (a wiring problem ->
        # worst_in_bar must raise, never silently no-op) from "source supplied
        # but this market/bar is sparse" (a real data fact -> fall back to
        # close). _has_trades_source records the former; _trade_prints holds the
        # per-market prints when a source exists.
        self._has_trades_source = trades is not None
        self._trade_prints: dict[str, pd.DataFrame] = {}
        if trades is not None and len(trades):
            t = trades.copy()
            # yes_price per print: NO fill at p implies YES at 1-p (binary mkts),
            # exactly as build_prices_from_trades derives it — same convention.
            t["yes_price"] = t["price"].where(t["outcome"] == "YES",
                                              1.0 - t["price"])
            t = t[["condition_id", "traded_at", "yes_price"]]
            self._trade_prints = {
                cid: g.sort_values("traded_at").reset_index(drop=True)
                for cid, g in t.groupby("condition_id")
            }

    def yes_price_at(self, condition_id: str, ts: pd.Timestamp) -> float | None:
        if condition_id not in self._series and self._prices_root is not None:
            import pathlib
            p = pathlib.Path(self._prices_root) / "prices" / condition_id
            for ext in (".parquet", ".pkl"):
                fp = p.with_suffix(ext)
                if fp.exists():
                    df = (pd.read_parquet(fp) if ext == ".parquet"
                          else pd.read_pickle(fp))
                    self._series[condition_id] = (
                        df.set_index("ts")["yes_price"].sort_index())
                    break
            else:
                self._series[condition_id] = None   # not found, don't retry
        s = self._series.get(condition_id)
        if s is None:
            return None
        idx = s.index.searchsorted(ts, side="right") - 1
        if idx < 0:
            return None
        return float(s.iloc[idx])

    def _bar_ts_at(self, condition_id: str, ts: pd.Timestamp):
        """The bar timestamp (left edge) whose close prices an as-of fill at ts.

        Mirrors yes_price_at's as-of lookup but returns the bar's index label
        rather than its value. Returns None when there is no bar at/before ts.
        """
        s = self._series.get(condition_id)
        if s is None:
            return None
        idx = s.index.searchsorted(ts, side="right") - 1
        if idx < 0:
            return None
        return s.index[idx]

    def _worst_yes_in_bar(self, condition_id: str, ts: pd.Timestamp,
                          adverse: str) -> float | None:
        """Direction-adverse extreme YES-price among REAL prints in ts's bar.

        adverse="max" -> highest yes_price the market actually traded in the bar
                         (worst for a YES/long entrant, who pays more).
        adverse="min" -> lowest  yes_price (worst for a NO/short entrant).

        Uses only prints whose real traded_at falls in [bar_ts, bar_ts + freq).
        A return of None means "source exists but this bar/market has NO prints"
        — a sparse-bucket fact, NOT a missing source (the caller checks source
        presence separately and raises for that). Sparse-bucket -> caller falls
        back to the close. A bar with exactly one print returns that one print
        (may equal the close — fine, there is no adverse extreme beyond the one
        real observation). Never fabricates a price; never reorders timestamps.
        """
        g = self._trade_prints.get(condition_id)
        if g is None or len(g) == 0:
            return None   # source exists but no prints for this market -> sparse
        # ensure the (possibly lazy) price series is loaded so _bar_ts_at can
        # read the bar index; yes_price_at performs the lazy parquet load.
        _ = self.yes_price_at(condition_id, ts)
        bar_ts = self._bar_ts_at(condition_id, ts)
        if bar_ts is None:
            return None
        bar_end = bar_ts + pd.Timedelta(self._freq)
        m = (g["traded_at"] >= bar_ts) & (g["traded_at"] < bar_end)
        prints = g.loc[m, "yes_price"]
        if len(prints) == 0:
            return None   # sparse bucket -> caller falls back to close
        return float(prints.max() if adverse == "max" else prints.min())

    # Side-aware intra-bar fill pessimism. price_at() below is the NEUTRAL
    # as-of/close lookup (mark-to-market truth) and takes no side/policy.
    # fill_price_at() is the FILL-specific path: it selects the bar's adverse
    # extreme from real prints based on BOTH outcome and side.
    #
    #   outcome=YES, side=buy  -> max yes_price   (a YES buyer pays the high)
    #   outcome=YES, side=sell -> min yes_price   (a YES seller sells at the low)
    #   outcome=NO,  side=buy  -> min yes_price   (NO buy = YES short; hurt by low yes)
    #   outcome=NO,  side=sell -> max yes_price
    #
    # All other rules unchanged: real prints only, bucket [bar_ts, bar_ts+freq),
    # no-source raises, sparse bucket falls back to close, one print is used.
    _ADVERSE = {
        ("YES", "buy"):  "max", ("YES", "sell"): "min",
        ("NO",  "buy"):  "min", ("NO",  "sell"): "max",
    }

    def price_at(self, condition_id: str, outcome: str,
                 ts: pd.Timestamp) -> float | None:
        """NEUTRAL as-of/close price for `outcome` at `ts`.

        This is the mark-to-market / convergence lookup: the resampled close
        value, with NO intra-bar pessimism and NO side. Fill call sites must use
        fill_price_at() instead. Kept side-/policy-free on purpose so a non-fill
        consumer cannot accidentally receive a pessimistic fill price.
        """
        if outcome not in ("YES", "NO"):
            raise ValueError(f"unknown outcome {outcome!r}; expected 'YES' or 'NO'")
        p = self.yes_price_at(condition_id, ts)
        if p is None:
            return None
        return p if outcome == "YES" else 1.0 - p

    def fill_price_at(self, condition_id: str, outcome: str, ts: pd.Timestamp,
                      side: str,
                      intrabar_fill_policy: str = "close") -> float | None:
        """FILL price for a `side` ('buy'/'sell') order on `outcome` at `ts`.

        intrabar_fill_policy:
          "close"        -> resampled close value (legacy; side-independent).
          "worst_in_bar" -> the SIDE+OUTCOME-adverse extreme among REAL prints in
                            the bar (see _ADVERSE), when raw trades are available;
                            otherwise falls back to close. No invented data.

        no-source raises; sparse/absent bucket falls back to close; a one-print
        bucket yields that print. Real timestamps are never overridden.
        """
        if outcome not in ("YES", "NO"):
            raise ValueError(f"unknown outcome {outcome!r}; expected 'YES' or 'NO'")
        if side not in ("buy", "sell"):
            raise ValueError(f"unknown side {side!r}; expected 'buy' or 'sell'")

        if intrabar_fill_policy == "worst_in_bar":
            if not self._has_trades_source:
                raise ValueError(
                    "intrabar_fill_policy='worst_in_bar' requires raw trades, "
                    "but this PriceBook was constructed without a trades source. "
                    "Pass trades=... to PriceBook, or use intrabar_fill_policy="
                    "'close'. (A sparse/empty bar with a source present is fine "
                    "and falls back to the close; this error is specifically the "
                    "no-source case.)")
            adverse = self._ADVERSE[(outcome, side)]
            worst_yes = self._worst_yes_in_bar(condition_id, ts, adverse)
            if worst_yes is not None:
                return worst_yes if outcome == "YES" else 1.0 - worst_yes
            # source exists but bar/market sparse -> fall through to close below
        elif intrabar_fill_policy != "close":
            raise ValueError(
                f"unknown intrabar_fill_policy {intrabar_fill_policy!r}; "
                "expected 'close' or 'worst_in_bar'")
        # close / fallback path: neutral as-of value for the outcome
        p = self.yes_price_at(condition_id, ts)
        if p is None:
            return None
        return p if outcome == "YES" else 1.0 - p

    def liquidity(self, condition_id: str) -> float:
        return float(self._liq.get(condition_id, 0.0))


def resolve_sqrt_coeff(impact_k: float, impact_k_sqrt: float | None,
                       impact_sqrt_ref_x: float) -> float:
    """Resolve the square-root coefficient, deriving it if not supplied.

    If ``impact_k_sqrt`` is None it is derived by matching the linear and
    square-root terms at the reference participation point ``impact_sqrt_ref_x``:

        impact_k * x_ref == impact_k_sqrt * sqrt(x_ref)
        => impact_k_sqrt = impact_k * sqrt(x_ref)

    With impact_k=0.5 and ref_x=0.01 this gives 0.5 * 0.1 = 0.05. This is a
    deliberate modeling prior (the two functional forms agree at 1% of static
    market liquidity), NOT a calibration to order-book depth — no depth data
    exists in the frames. Reusing impact_k directly in the sqrt term would push
    almost every fill into the cap, which is why a separate coefficient exists.
    """
    if impact_sqrt_ref_x <= 0:
        raise ValueError(f"impact_sqrt_ref_x must be > 0, got {impact_sqrt_ref_x}")
    if impact_k < 0:
        raise ValueError(f"impact_k must be >= 0, got {impact_k}")
    if impact_k_sqrt is not None:
        if impact_k_sqrt < 0:
            raise ValueError(f"impact_k_sqrt must be >= 0, got {impact_k_sqrt}")
        return float(impact_k_sqrt)
    return float(impact_k * math.sqrt(impact_sqrt_ref_x))


def compute_impact(size_usdc: float, liquidity_usdc: float, *,
                   impact_k: float, impact_cap: float,
                   impact_shape: str = "sqrt_guarded",
                   impact_k_sqrt: float | None = None,
                   impact_sqrt_ref_x: float = 0.01,
                   invalid_liquidity_policy: str = "raise") -> float:
    """Price impact in probability space, from size and STATIC liquidity only.

    Uses ONLY size_usdc and liquidity_usdc. No order-book depth, volume, or
    spread is used or inferred — those columns do not exist in the frames.

    Let x = size_usdc / liquidity_usdc (participation fraction). Modes:

        "linear"        impact = impact_k * x                  (legacy)
        "sqrt"          impact = impact_k_sqrt * sqrt(x)       (sensitivity only;
                        CAN be cheaper than linear when x > 1 — surfaced on
                        purpose, not a conservative default)
        "sqrt_guarded"  impact = max(linear, sqrt)             (DEFAULT)

    In all modes the cap is applied last: impact = min(impact, impact_cap).

    "sqrt_guarded" is the pessimistic default: because it takes max(linear, sqrt)
    BEFORE the cap, it can never assign LESS impact than the legacy linear model.
    The hardening pass therefore does not reduce estimated cost relative to the
    previous implementation; it can only raise it (for small participation, where
    the concave sqrt term sits above linear) or leave it unchanged.

    Input handling (no fabricated liquidity):
      - size_usdc <= 0            -> 0.0 impact (nothing traded).
      - liquidity_usdc <= 0       -> LEGACY conservative fallback: impact_cap.
        (incl. 0.0 from a missing  This is a DELIBERATE pre-existing path:
         market via book.liquidity   book.liquidity() returns 0.0 for unknown
         -> 0.0)                     markets, and the old model assigned
                                     impact_cap when liq <= 0. Preserved verbatim.
                                     Does NOT invent a liquidity value.
      - liquidity_usdc NaN / inf  -> MALFORMED input, NOT a legacy fallback.
        (non-finite)                 Old code handled these only ACCIDENTALLY
                                     (inf -> optimistic ~0 impact; NaN -> poison).
                                     Policy-driven, default "raise":
                                       "raise" -> ValueError (surface corruption)
                                       "cap"   -> impact_cap (explicit opt-in)
                                     Never silently capped under the default.
    """
    if impact_cap < 0:
        raise ValueError(f"impact_cap must be >= 0, got {impact_cap}")
    if size_usdc <= 0:
        return 0.0

    # MALFORMED liquidity (NaN/inf): distinct from the legacy liq<=0 fallback.
    # Not a deliberate path in the old code; default policy surfaces it loudly.
    if liquidity_usdc is not None and not np.isfinite(liquidity_usdc):
        if invalid_liquidity_policy == "cap":
            return float(impact_cap)
        if invalid_liquidity_policy == "raise":
            raise ValueError(
                f"liquidity_usdc must be finite and positive; got {liquidity_usdc!r}. "
                "This is malformed (NaN/inf) liquidity, not a missing market. "
                "Set invalid_liquidity_policy='cap' to fall back to impact_cap "
                "explicitly, or fix the upstream liquidity data.")
        raise ValueError(
            f"unknown invalid_liquidity_policy {invalid_liquidity_policy!r}; "
            "expected 'raise' or 'cap'")

    # LEGACY fallback (preserved verbatim): liq <= 0, including the 0.0 that
    # book.liquidity() returns for an unknown market. Conservative cap, no fake.
    if liquidity_usdc is None or liquidity_usdc <= 0:
        return float(impact_cap)

    x = size_usdc / liquidity_usdc
    k_sqrt = resolve_sqrt_coeff(impact_k, impact_k_sqrt, impact_sqrt_ref_x)
    linear = impact_k * x
    sqrt_term = k_sqrt * math.sqrt(x)

    if impact_shape == "linear":
        impact = linear
    elif impact_shape == "sqrt":
        impact = sqrt_term
    elif impact_shape == "sqrt_guarded":
        impact = max(linear, sqrt_term)
    else:
        raise ValueError(
            f"unknown impact_shape {impact_shape!r}; "
            "expected 'linear', 'sqrt', or 'sqrt_guarded'")

    return float(min(impact, impact_cap))


def nearby_trade_diagnostics(trades: pd.DataFrame, condition_id: str,
                             fill_at: pd.Timestamp,
                             window_seconds: int = 300) -> dict:
    """Realized-trade-print diagnostics around a simulated fill — DIAGNOSTIC ONLY.

    Returns coarse stats on this market's actual trade prints within
    +/- window_seconds of fill_at. This is a REALIZED-PRINT PROXY, NOT order-book
    depth: it says how much actually traded near that time, which is a weak and
    biased proxy for available liquidity (it reflects what cleared, not what was
    quoted). It is provided for inspection/analysis and DOES NOT feed the impact
    model. Nothing in the fill path consumes it unless an explicit, separate flag
    is wired in (not done here, by design — keeps this patch narrow).

    Expects `trades` with at least: condition_id, traded_at, size_usdc.
    The +/-300s default window is arbitrary (no existing window to inherit) and
    is parameterized so it can be set deliberately.

    If no prints fall in the window, returns NaN/0 diagnostics — callers should
    then fall back to the static liquidity_usdc model (which the impact function
    uses regardless, since this helper never touches it).
    """
    out = {
        "nearby_median_trade_size_usdc": float("nan"),
        "nearby_trade_count": 0,
        "nearby_window_seconds": int(window_seconds),
    }
    if trades is None or len(trades) == 0:
        return out
    lo = fill_at - pd.Timedelta(seconds=window_seconds)
    hi = fill_at + pd.Timedelta(seconds=window_seconds)
    m = ((trades["condition_id"] == condition_id)
         & (trades["traded_at"] >= lo) & (trades["traded_at"] <= hi))
    g = trades.loc[m, "size_usdc"]
    n = int(len(g))
    out["nearby_trade_count"] = n
    if n > 0:
        out["nearby_median_trade_size_usdc"] = float(g.median())
    return out


class LatencyModel:
    def __init__(self, cfg: LatencyConfig):
        self.cfg = cfg

    def apply(self, *, condition_id: str, outcome: str, detected_at: pd.Timestamp,
              leaders_avg_entry: float, size_usdc: float,
              book: PriceBook) -> FillEstimate:
        fill_at = detected_at + pd.Timedelta(seconds=self.cfg.detection_delay_seconds)
        # entries are BUYS: use the side-aware fill path.
        mkt = book.fill_price_at(condition_id, outcome, fill_at, side="buy",
                                 intrabar_fill_policy=self.cfg.intrabar_fill_policy)
        if mkt is None:
            return FillEstimate(False, 0.0, fill_at, "no price data")
        liq = book.liquidity(condition_id)
        impact = compute_impact(
            size_usdc, liq,
            impact_k=self.cfg.impact_k, impact_cap=self.cfg.impact_cap,
            impact_shape=self.cfg.impact_shape,
            impact_k_sqrt=self.cfg.impact_k_sqrt,
            impact_sqrt_ref_x=self.cfg.impact_sqrt_ref_x,
            invalid_liquidity_policy=self.cfg.invalid_liquidity_policy)
        # FEE SEMANTICS UNCHANGED (Phase 1.5 is an impact-shape patch only).
        # This path uses a flat bps fee on price. NOTE: other parts of the
        # codebase (the randomization skill test) model the Polymarket fee as
        # C * feeRate * p * (1-p); this expression is intentionally NOT altered
        # here. Aligning the two fee models is a separate, deliberate decision.
        fee = mkt * self.cfg.taker_fee_bps / 10_000.0
        fill_price = float(np.clip(mkt + impact + fee, 0.001, 0.999))
        if fill_price - leaders_avg_entry > self.cfg.max_chase:
            return FillEstimate(False, fill_price, fill_at, "price chased beyond max_chase")
        return FillEstimate(True, fill_price, fill_at)


ZERO_LATENCY = LatencyConfig(detection_delay_seconds=0, impact_k=0.0,
                             impact_cap=0.0, max_chase=1.0, taker_fee_bps=0,
                             # explicit so the upper-bound run is a true zero
                             # regardless of default-shape changes: with
                             # impact_k=0 and cap=0, every mode yields 0 impact.
                             impact_shape="sqrt_guarded", impact_k_sqrt=0.0,
                             impact_sqrt_ref_x=0.01,
                             invalid_liquidity_policy="raise",
                             # close: the zero/upper-bound baseline uses legacy
                             # fill pricing, not worst-in-bar. (Also avoids the
                             # no-trades-source raise when used with a tradeless
                             # PriceBook, e.g. in unit tests.)
                             intrabar_fill_policy="close")
