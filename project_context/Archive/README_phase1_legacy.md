# pm-research — Phase 1: prove or disprove the edge

Pure-Python research stack for Polymarket copy-trading. **No database, no SQL,
no ORM, no migrations.** pandas + numpy + stdlib; flat files (parquet, or
pickle where pyarrow is absent). Its only job is to answer one question
honestly: *does copying high-alpha wallets survive realistic latency and
impact?* Phase 2 (durable store, live execution) is only built if the answer
here is yes.

## Layout

```
pm_research/
├── config.py            frozen dataclass configs — a result is reproducible
│                        from (config, data, seed)
├── data/
│   ├── schemas.py       the four canonical frames: TRADES, MARKETS,
│   │                    RESOLUTIONS, PRICES
│   ├── store.py         flat-file store + backfill COVERAGE proof; backtests
│   │                    refuse to run over unproven ranges
│   ├── backfill.py      VERIFIED real endpoints (Data API trades, Gamma
│   │                    markets/resolutions, CLOB prices-history) behind an
│   │                    injectable fetcher; prices-from-prints builder
│   ├── providers.py     optional library backends (polymarket-apis,
│   │                    aiopolymarket) feeding the SAME parsers
│   ├── discovery.py     candidate wallet pool: top-volume markets (active
│   │                    AND closed) → trade prints → filtered, ranked pool
│   └── synthetic.py     synthetic world with KNOWN ground truth (skilled vs
│                        coin-flip traders) — the test harness
├── features.py          point-in-time per-trader features (roi, win rate,
│                        conviction, concentration, automation proxy)
├── scoring.py           within-universe percentile ranks → alpha score
├── selection.py         TrailingAlphaSelector — point-in-time universe
│                        selection; ManualListSelector exists but is flagged
│                        biased in every result
├── consensus.py         windowed multi-trader agreement → Signal (raw,
│                        UNcalibrated confidence) + cooldown filter
├── calibration.py       isotonic (hand-rolled PAVA) raw confidence → p(win);
│                        refuses to fit under min_samples → bootstrap sizing
├── latency.py           detection delay + impact + max-chase abandonment;
│                        ZERO_LATENCY config for the upper-bound run
├── metrics.py           sharpe, sortino, max drawdown, profit factor
├── backtest.py          daily event loop: weekly point-in-time reselection,
│                        consensus, latency-modeled fills, resolution closes
└── cli.py               synth-backtest | backfill | backtest
```

## Run the tests

```bash
pytest                    # if pytest is installed
python -m tests.run       # stdlib fallback runner, identical suite
```

35 tests. The ones that matter most:

- **`test_selector_no_lookahead_...`** — appending future data must not change
  the universe selected as of T. This is the survivorship-bias guard.
- **`test_e2e_detects_real_edge_under_modeled_latency`** — on a synthetic
  world where 10 wallets demonstrably have skill, the full pipeline
  (selection → scoring → consensus → latency-modeled fills → resolution)
  must show positive ROI.
- **`test_e2e_reports_no_edge_when_traders_are_random`** — with only
  coin-flippers, the engine must NOT manufacture profit. An engine that
  fails this test is worse than no engine.
- **`test_e2e_zero_latency_is_upper_bound`** — modeled latency can only hurt.

## Demo (no network needed)

```bash
python -m pm_research.cli synth-backtest --seed 7
```

Prints the zero-latency result (upper bound — do not believe) next to the
modeled-latency result (the number that counts) and the ROI given away to
latency. On the default synthetic world that gap is ~0.39 ROI — which is the
whole thesis of phase 1 in one number.

## Real data

```bash
# 0. discover a broad candidate pool (NOT a hand-picked winner list)
python -m pm_research.cli discover --markets 40 --top 250 --out wallets.txt

# 1. one command assembles all four frames: trades, markets, resolutions, prices
python -m pm_research.cli backfill --wallets $(cat wallets.txt) \
    --start 2025-01-01 --end 2025-12-31 --root ./data
python -m pm_research.cli backtest --root ./data --start 2025-03-01 --end 2025-12-31
```

The endpoint task flagged in earlier revisions is **complete and verified
against the live docs** (June 2026):

- **TRADES** — Data API `GET /trades?user=<wallet>`; rows carry unix-seconds
  `timestamp`, camelCase `conditionId`, `usdcSize`, `transactionHash`, and
  NO per-fill id — dedup uses a stable composite hash of
  (tx, asset, side, price, size, timestamp, outcomeIndex).
- **MARKETS / RESOLUTIONS** — Gamma `GET /markets?condition_ids=...`;
  resolutions are derived from `closed` + `outcomePrices` ('["1","0"]').
  Resolution timestamps use `closedTime`/`endDate` (an approximation;
  exact on-chain timestamps are a phase-2 concern).
- **PRICES** — built from trade prints by default: Data API
  `GET /trades?market=<conditionId>` → every fill is a price observation
  (NO fill at p implies YES at 1−p) → hourly resample + ffill. This is
  deliberate: the CLOB `/prices-history` endpoint degrades to >=12h
  granularity (often empty) for resolved markets, which is exactly the data
  a backtest needs. The CLOB path exists as `backfill_prices_from_clob()`
  for live/active markets.

### Optional library providers

The zero-dependency urllib `Backfiller` is the reference implementation.
Two community libraries can substitute for the HTTP layer — both feed the
same parsers, so frames are byte-identical (proven by test):

```bash
pip install "pm-research[providers]"   # polymarket-apis + aiopolymarket
python -m pm_research.cli backfill --provider polymarket-apis ...
python -m pm_research.cli backfill --provider aiopolymarket ...
```

Caveats, on record: `aiopolymarket` is a v0.0.x single-release package —
pinned in extras; `polymarket-apis` is broader and sync, which suits this
batch workload. If either lags an API change, fall back to `--provider
urllib` and fix the one parser function.

The store and engine remain source-agnostic: anything producing the four
canonical frames works.

## The go/no-go rule

A strategy graduates to Phase 2 only if the **modeled-latency** backtest under
**dynamic selection** (not the manual list) is profitable across multiple
seeds/date splits, and stays profitable when `detection_delay_seconds` is set
to the pessimistic end of what live measurement will support. Anything else
is the system working correctly by saying no.
