"""Shared test helpers. Plain functions, no pytest fixtures, so the suite
runs under pytest AND under tests/run.py (stdlib fallback runner)."""
from __future__ import annotations

import pandas as pd

from pm_research.data import schemas
from pm_research.data.synthetic import World, WorldConfig, generate

UTC = "UTC"


def ts(s: str) -> pd.Timestamp:
    return pd.Timestamp(s, tz=UTC)


def make_trades(rows: list[dict]) -> pd.DataFrame:
    """rows: dicts with any of the trade columns; sensible defaults filled."""
    if not rows:
        return schemas.empty(schemas.TRADES_COLS)
    out = []
    for i, r in enumerate(rows):
        out.append({
            "trade_id": r.get("trade_id", f"t{i:05d}"),
            "wallet": r.get("wallet", "0xw0"),
            "condition_id": r.get("condition_id", "0xc0"),
            "outcome": r.get("outcome", "YES"),
            "side": r.get("side", "BUY"),
            "price": r.get("price", 0.5),
            "size_usdc": r.get("size_usdc", 100.0),
            "traded_at": r.get("traded_at", ts("2025-06-01 12:00")),
        })
    return schemas.validate(pd.DataFrame(out), schemas.TRADES_COLS, "trades")


def make_resolutions(rows: list[dict]) -> pd.DataFrame:
    if not rows:
        return schemas.empty(schemas.RESOLUTIONS_COLS)
    out = [{"condition_id": r.get("condition_id", "0xc0"),
            "winning_outcome": r.get("winning_outcome", "YES"),
            "resolved_at": r.get("resolved_at", ts("2025-06-10"))} for r in rows]
    return schemas.validate(pd.DataFrame(out), schemas.RESOLUTIONS_COLS, "resolutions")


_SMALL_WORLD_CACHE: dict[int, World] = {}


def small_world(seed: int = 7, **overrides) -> World:
    """A compact synthetic world (fast enough for e2e tests), cached by seed."""
    key = (seed, tuple(sorted(overrides.items())))
    if key not in _SMALL_WORLD_CACHE:
        params = dict(n_markets=80, n_skilled=10, n_random=25,
                      trades_per_trader=40, horizon_days=240, seed=seed)
        params.update(overrides)
        _SMALL_WORLD_CACHE[key] = generate(WorldConfig(**params))
    return _SMALL_WORLD_CACHE[key]
