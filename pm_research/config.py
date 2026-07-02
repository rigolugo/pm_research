"""Phase-1 configuration. Plain dataclasses — no pydantic, no env magic.

Everything that influences a backtest result lives here so a result can be
reproduced from (config, data snapshot, seed) alone.
"""
from __future__ import annotations

from dataclasses import dataclass, field, asdict
from datetime import date


@dataclass(frozen=True)
class SelectionConfig:
    universe_size: int = 50
    lookback_days: int = 90
    min_resolved_trades: int = 20      # need resolved outcomes to judge skill
    min_volume_usdc: float = 5_000.0
    rebalance_interval_days: int = 7


@dataclass(frozen=True)
class ConsensusConfig:
    window_hours: int = 48
    min_unique_traders: int = 3
    min_weighted_score: float = 0.50
    cooldown_hours_per_market: int = 24


@dataclass(frozen=True)
class LatencyConfig:
    detection_delay_seconds: int = 120   # pessimistic until measured live
    impact_k: float = 0.5                # LEGACY linear coeff: linear = impact_k * x
    impact_cap: float = 0.03             # never assume more than 3c impact
    max_chase: float = 0.04              # abandon if price ran > 4c from leaders' entry
    taker_fee_bps: int = 0               # set to venue schedule when known
    # ---- Phase 1.5 impact-shape hardening (size_usdc & liquidity_usdc only) ----
    # x = size_usdc / liquidity_usdc (participation fraction of STATIC market liq).
    # Modes:
    #   "linear"        impact = impact_k * x                         (legacy)
    #   "sqrt"          impact = impact_k_sqrt * sqrt(x)              (sensitivity only)
    #   "sqrt_guarded"  impact = max(linear, sqrt)                    (DEFAULT, pessimistic)
    # then impact = min(impact, impact_cap) in all modes.
    # NOTE: this is NOT calibrated to order-book depth. No depth/volume/spread
    # data exists in the frames; impact uses only size_usdc and liquidity_usdc.
    impact_shape: str = "sqrt_guarded"
    # Separate sqrt coefficient — NOT impact_k reused. If None it is derived by
    # matching the linear and sqrt terms at x = impact_sqrt_ref_x:
    #   impact_k * x_ref == impact_k_sqrt * sqrt(x_ref)
    #   => impact_k_sqrt = impact_k * sqrt(x_ref)
    # With impact_k=0.5, ref_x=0.01 -> impact_k_sqrt = 0.5*0.1 = 0.05.
    # This is a modeling prior (curves cross at 1% participation), not a
    # calibration. Reusing impact_k directly would cap-out almost every fill.
    impact_k_sqrt: float | None = None
    impact_sqrt_ref_x: float = 0.01      # reference participation for the derivation
    # Data-quality policy for MALFORMED (non-finite) liquidity — NaN/inf.
    # This is distinct from the legacy liq<=0 fallback (which stays a silent
    # cap, since book.liquidity() maps missing markets to 0.0 by design).
    # NaN/inf were NEVER a deliberate fallback in the old code (inf produced an
    # accidental optimistic ~0 impact; NaN propagated). Default "raise" surfaces
    # corrupted liquidity instead of hiding it behind the cap. "cap" is an
    # explicit opt-in to the conservative fallback for NaN/inf.
    invalid_liquidity_policy: str = "raise"   # "raise" (default) | "cap"
    # ---- Phase 1.5 intra-bar fill pessimism ----------------------------------
    # The price series is reconstructed by resampling trade prints to hourly bars
    # and keeping the LAST print per bar (build_prices_from_trades). Pricing a
    # fill at that last/close value is optimistic: within the bar the market may
    # have traded through a WORSE level for the entrant. This policy controls the
    # within-bar fill price when the raw prints are available to PriceBook:
    #   "close"            use the resampled last/close value (LEGACY behavior)
    #   "worst_in_bar"     use the direction-ADVERSE extreme among the REAL prints
    #                      in that bar (max yes_price for a YES/long entrant, min
    #                      for NO). Uses only prints that actually occurred — no
    #                      invented ticks, no fabricated OHLC. Falls back to the
    #                      close value when raw prints are unavailable or the bar
    #                      has <2 distinct prints. Real timestamps are never
    #                      overridden; this only SELECTS which real print prices
    #                      the fill.
    intrabar_fill_policy: str = "worst_in_bar"


@dataclass(frozen=True)
class RiskConfig:
    size_fraction: float = 0.01          # bootstrap sizing: 1% of equity per signal
    use_kelly: bool = False              # only turned on once a calibrator is fitted
    kelly_fraction: float = 0.25
    max_position_fraction: float = 0.10
    max_open_positions: int = 20


@dataclass(frozen=True)
class BacktestConfig:
    start: date = date(2025, 1, 1)
    end: date = date(2025, 12, 31)
    initial_capital: float = 10_000.0
    selection: SelectionConfig = field(default_factory=SelectionConfig)
    consensus: ConsensusConfig = field(default_factory=ConsensusConfig)
    latency: LatencyConfig = field(default_factory=LatencyConfig)
    risk: RiskConfig = field(default_factory=RiskConfig)
    seed: int = 7

    def to_dict(self) -> dict:
        d = asdict(self)
        d["start"], d["end"] = self.start.isoformat(), self.end.isoformat()
        return d
