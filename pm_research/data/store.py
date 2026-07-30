"""Read-only local trade store used by the P0 CLOB canary diagnostic.

This compatibility module intentionally exposes only the existing
``Store(root).load_trades()`` interface required by the diagnostic. It reads
wallet trade files from ``<root>/trades`` in Parquet or pickle form.

It does not create directories, write files, manage coverage, load or save
markets/resolutions/prices, or define price/complement semantics.
"""
from __future__ import annotations

from pathlib import Path

import pandas as pd


TRADES_COLS = [
    "trade_id",
    "wallet",
    "condition_id",
    "outcome",
    "side",
    "price",
    "size_usdc",
    "traded_at",
    "tx_hash",
    "token_id",
    "outcome_index",
]

_BACKWARD_COMPAT_FILL = {"tx_hash", "token_id", "outcome_index"}


def _empty_trades() -> pd.DataFrame:
    """Return an empty frame with the accepted trade-column shape."""
    frame = pd.DataFrame({column: pd.Series(dtype="object") for column in TRADES_COLS})
    frame["traded_at"] = pd.Series(dtype="datetime64[ns, UTC]")
    frame["price"] = pd.Series(dtype="float64")
    frame["size_usdc"] = pd.Series(dtype="float64")
    return frame


def _validate_trades(frame: pd.DataFrame) -> pd.DataFrame:
    """Normalize and validate the trade columns needed by the diagnostic."""
    missing = [column for column in TRADES_COLS if column not in frame.columns]
    fillable = [column for column in missing if column in _BACKWARD_COMPAT_FILL]
    hard_missing = [column for column in missing if column not in _BACKWARD_COMPAT_FILL]

    if hard_missing:
        raise ValueError(f"trades frame missing columns: {hard_missing}")

    if fillable:
        frame = frame.assign(
            **{
                column: pd.Series([pd.NA] * len(frame), index=frame.index)
                for column in fillable
            }
        )

    traded_at = pd.to_datetime(frame["traded_at"], utc=True)
    frame = frame.assign(traded_at=traded_at)
    return frame[TRADES_COLS].copy()


def _read(path: Path) -> pd.DataFrame | None:
    """Read one trade file without creating or modifying anything."""
    parquet_path = path.with_suffix(".parquet")
    pickle_path = path.with_suffix(".pkl")

    if parquet_path.exists():
        return pd.read_parquet(parquet_path)
    if pickle_path.exists():
        return pd.read_pickle(pickle_path)
    return None


def _is_present(series: pd.Series) -> pd.Series:
    """Return true where values are non-null and non-blank."""
    not_null = series.notna()
    blank = series.astype("string").str.strip().isin(["", "nan", "None"])
    return not_null & ~blank.fillna(True)


def _drop_null_condition_id(frame: pd.DataFrame) -> pd.DataFrame:
    """Drop rows that cannot be assigned to a condition."""
    if "condition_id" not in frame.columns or len(frame) == 0:
        return frame

    keep = _is_present(frame["condition_id"])
    dropped = int((~keep).sum())
    if dropped:
        output = frame[keep].reset_index(drop=True)
        output.attrs["dropped_null_condition_id"] = dropped
        return output

    frame.attrs["dropped_null_condition_id"] = 0
    return frame


def _dedup_prefer_populated_keys(frame: pd.DataFrame) -> pd.DataFrame:
    """Deduplicate by trade_id, preferring rows with populated join keys."""
    if "trade_id" not in frame.columns or len(frame) == 0:
        return frame

    work = frame.copy()
    score = (
        _is_present(work["tx_hash"]).astype("int8") * 4
        if "tx_hash" in work
        else pd.Series(0, index=work.index)
    )
    if "token_id" in work:
        score = score + _is_present(work["token_id"]).astype("int8") * 2
    if "outcome_index" in work:
        score = score + work["outcome_index"].notna().astype("int8")

    work["_keyscore"] = score
    work = work.sort_values(
        ["trade_id", "_keyscore"],
        ascending=[True, False],
        kind="mergesort",
    )
    return (
        work.drop_duplicates(subset="trade_id", keep="first")
        .drop(columns="_keyscore")
    )


class Store:
    """Read-only compatibility wrapper for local wallet trade files."""

    def __init__(self, root: str | Path):
        self.root = Path(root)

    def load_trades(self, wallets: list[str] | None = None) -> pd.DataFrame:
        """Load, normalize, filter, deduplicate, and sort local trade rows."""
        trades_dir = self.root / "trades"
        files = sorted(trades_dir.glob("*")) if trades_dir.exists() else []
        frames: list[pd.DataFrame] = []

        for file_path in files:
            if wallets is not None and file_path.stem not in wallets:
                continue
            frame = _read(trades_dir / file_path.stem)
            if frame is not None and len(frame):
                frames.append(frame)

        if not frames:
            return _empty_trades()

        output = pd.concat(frames, ignore_index=True)
        output = _validate_trades(output)
        output = _drop_null_condition_id(output)
        output = _dedup_prefer_populated_keys(output)
        return output.sort_values("traded_at").reset_index(drop=True)
