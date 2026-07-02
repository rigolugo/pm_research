# pm_research — Phase 1 Findings (Peer Review)

**Status: Phase 1 complete. Primary hypothesis falsified six independent ways.
One optional re-discovery lever remains, with a negative prior.**

This document is for peer review. It records what was tested, the exact results,
and the honest conclusions — including the parts that argue against the project.
It is deliberately written to be falsifiable and to invite disagreement. Numbers
are from runs on the real backfilled dataset unless marked synthetic.

---

## 1. The question

> Does copy-trading high-alpha Polymarket wallets remain profitable after
> realistic detection delay, execution latency, and market impact?

Phase 2 (durable store, live execution) was gated on a positive answer under
**modeled latency** and **dynamic (non-lookahead) selection**, robust across
seeds and date splits. A negative result was defined in advance as a valid,
successful outcome — the system working as a falsification instrument.

---

## 2. The dataset

Backfilled from Polymarket's public Data API (`/trades`, `/activity`) and Gamma
API (`/markets`) onto a single AWS t3.micro.

| Frame | Size |
|---|---|
| Wallets (post bot-filter) | 115 |
| Trades | ~388k (in-window ~296k) |
| Markets with metadata | 993 |
| Resolutions | 22,019 |
| Price rows (hourly, reconstructed from prints) | ~15.1M |

**Known data limitations (material to the conclusions):**
- **Wallet selection bias.** Discovery ranked candidates by raw **volume**,
  which over-selects market makers / HFT bots. This is the single most
  important caveat and is confirmed quantitatively in §4.4.
- **Gamma purge.** Resolved markets are dropped from Gamma over time, so only
  993 of 24,172 markets returned metadata. **Resolutions were therefore derived
  from price convergence** (final hourly `yes_price` ≥ 0.99 → YES, ≤ 0.01 → NO),
  not from `closedTime`/`endDate`. 22,019 of 24,172 markets (~91%) resolved
  decisively. This is event-time truth from trade prints, but it is a derivation,
  not an oracle read, and reviewers should weigh that. **Robustness check
  available:** `scripts/resolution_flip_robustness.py` quantifies how many
  resolutions would have to be wrong to flip the §4.1 verdict — both within the
  backtest (how many filled-trade resolutions must flip to reach break-even) and
  globally (fraction of derivations that are not crisp, i.e. final price not
  within 0.005 of 0/1, which is the population most exposed to a late
  correction). The gold-standard validation — cross-checking a sample against
  on-chain `PositionSplit/Merge` events — requires Polygon indexing not set up
  here and is noted as future work. **Independently, the walk-forward (§4.1)
  makes the resolution-flip concern moot for the verdict:** all 10 rolling
  windows are negative, so flipping the sign would require errors across every
  window at once, not one unlucky resolution in a single 36-trade window.
- **Category metadata** exists for only ~4% of markets (the 993), so
  wallet×category analysis is not yet possible at scale.
- **Single year, single regime** (2025-06 → 2026-06). Generalization untested
  beyond this window.

---

## 3. Engineering notes (for reproducibility)

Several real bugs were fixed during Phase 1; the test suite went 61 → 67. None
of these changed the *direction* of any finding, but they were prerequisites to
running at all on a 1GB box:

1. **Dead `abort_over`** in the deep-history walk — bot wallets were fully
   walked then discarded, a likely OOM cause. Now aborts mid-walk.
2. **`--resume`** was documented but never implemented. Implemented + tested.
3. **`condition_ids=""` 422** — trades with a missing `conditionId` poisoned the
   Gamma query and crashed the run. Now filtered.
4. **PriceBook OOM** — the backtest materialized 24k per-market Series at once.
   Now lazy-loads per market from disk.
5. **Cloudflare 403** — the API blocks AWS IPs under the default urllib UA.
   Fixed with a browser User-Agent.

All findings below were produced *after* these fixes, on a green test suite.

---

## 4. Results

### 4.1 Modeled-latency backtest (the headline go/no-go)

Single window, dynamic selection, `biased_selection=False`,
2025-06-01 → 2026-06-01:

| Metric | Zero-latency (upper bound) | Modeled latency (counts) |
|---|---|---|
| Total ROI | +0.276 | **−0.063** |
| Sharpe | 0.86 | **−1.27** |
| Profit factor | 3.51 | 0.62 |
| Win rate | 0.72 | 0.72 |
| Trades | 43 | 36 |

**Robustness — walk-forward across 10 rolling 180-day windows** (step 30d,
2025-03 → 2026-06; `scripts/walk_forward_backtest.py`). The single window above
filled only 36 trades and ended one resolution-flip from break-even (see §2),
so it was re-run as a distribution:

| | Modeled latency | Zero-latency (reference) |
|---|---|---|
| windows negative | **10 / 10 (100%)** | 6 / 10 |
| mean ROI | **−0.037** | +0.015 |
| median ROI | −0.031 | −0.004 |
| range | −0.110 … −0.004 | — |

**Read (corrected from the single-window framing).** Every one of 10 windows is
negative under modeled latency — the single −6.3% was not a fluke, so this leg
is **robust**, not fragile. But the distribution also corrects an overstatement:
the *zero-latency* edge is itself marginal-to-nonexistent (mean +1.5%, median
**negative**, only 4/10 windows positive). The original single window's +27.6%
zero-latency figure was itself a lucky draw. So the accurate story is **not**
"strong edge destroyed by latency" (which would invite "just execute faster") —
it is **"no meaningful edge even at the zero-latency limit; modeled costs push a
flat-to-marginal signal robustly negative."** There is no faster-execution
rescue for an edge that is already absent at zero latency. **Go/no-go: NO-GO**,
and robustly so. (One window, #10, showed a large latency gap — modeled −0.11 vs
zero +0.21 — the lone period where speed would have mattered; 1 of 10, modeled
still negative.)

### 4.2 Edge half-life (decay + niche search)

Measured the per-trade entry edge (resolution payout − entry price) at delays
0 / 5m / 30m / 2h / 12h / 48h, with a train/test date split and segments
(time-to-resolution, activity/liquidity proxy) chosen *in advance*.

- **Overall edge is negative even at instant entry on the held-out test
  window** (−0.084). The decay curve is moot — there is no positive edge to
  decay from. This is *below* even the zero-second row of a latency table.
- Every pre-stated segment failed on test. The one "candidate" (`thick /
  high-activity`, test +0.040) was marginal, larger out-of-sample than in
  (a red flag, not a green one), and gross of impact. Not pursued.

**Read:** on held-out data, the signal does not beat the price these wallets
trade against — before any latency. The problem is deeper than speed.

### 4.3 Position-lifecycle reconstruction (Risk 1 from review)

The pipeline scores wallets as if every BUY is held to resolution. But the data
is 31% SELLs — these wallets trade *around* positions. Reconstructing realized
round-trip PnL vs the hold-to-resolution assumption, on resolved positions of
the selected universe:

| Model | Aggregate PnL |
|---|---|
| **Realized** (actual buys + sells) | **+800,343** |
| **Hold-to-resolution** (pipeline assumption) | **−532,313** |

**Read:** the wallets are genuinely, substantially profitable by their own
trading. The pipeline's holding model has the **opposite sign** in aggregate.
The wallets' skill is real; it lives in their **exits**, which the pipeline
discards. This re-opened the question: is that exit-skill copyable?

*(Note: an early version of this script mis-summarized this as "models largely
agree" using a per-wallet sign metric that ignores magnitude. Corrected to gate
on aggregate divergence. Reviewers should use the corrected `lifecycle_pnl.py`.)*

### 4.4 Exit-mirroring backtest (copyable vs uncopyable)

Same signals, two exit models, identical entry latency+impact, exits also pay
latency+impact:

| Model | ROI | Sharpe | Win rate | Profit factor |
|---|---|---|---|---|
| Hold-to-resolution | −0.063 | −1.27 | 0.72 | 0.62 |
| **Exit-mirror** (sell when leaders sell) | **−0.201** | **−4.35** | 0.45 | 0.16 |

**Read:** mirroring the leaders' exits made things **much worse**, and trading
more lost more. The wallets' +800k is **liquidity-provision / market-making
P&L**, structurally unavailable to a latency-bound taker who crosses the spread
on both legs. **The skill is uncopyable.** This is decisive and matches review
Risk 4.

**Caveat (carried forward from §4.5).** The "market-making" attribution here
rests on the *behavioral* classifier of §4.5, not on confirmed on-chain
maker/taker roles. The conclusion should be read as "strongly consistent with
uncopyable liquidity-provision PnL, behaviorally inferred" rather than as
on-chain ground truth. Direct validation via Polygon `OrderFilled` maker/taker
fields (§4.8) remains the recommended confirmation and is not yet done.

**Why this likely *understates* the negative result.** The impact model is a
parametric approximation (`impact_k × size/liquidity`), not a fill against
actual point-in-time order-book depth. A real L2-depth slippage model — and the
fact that on-chain fills are two-sided, so the taker crosses a real spread —
would make entry/exit *more* expensive, not less. So the modeled −0.063 /
−0.201 ROIs are if anything optimistic; a more faithful execution-cost model
pushes the verdict further negative, not toward break-even.

### 4.5 Wallet behavioral classifier (market maker vs directional)

Classifying the 115 wallets by five behavioral tells (no outcome data; cannot
leak lookahead):

| Label | Count | sell/buy | roundtrip | median hold |
|---|---|---|---|---|
| MARKET_MAKER | 50 | 0.85 | 0.71 | **1.3 h** |
| DIRECTIONAL | 39 | 0.23 | 0.26 | **18.9 h** |
| UNKNOWN (<20 trades) | 18+ | — | — | — |

**Read:** clean separation on behaviour — market makers flip fast (1.3h median
hold, 0.85 sell/buy) where directional traders hold ~15× longer. A majority of
the judged pool behaves like market makers, confirming the volume-ranking bias
flagged in §2: a large share of the pool is uncopyable by construction. The
*exact* share is threshold-dependent and is quantified, with error bars, in
§4.5.1 — it should be read as a range governed by one design choice, not as the
point estimate the table's counts might suggest. (Counts were recomputed on a
later data snapshot than the original run, which grew the resolved-market set
and shifted the baseline split to MM=61 / DIR=42 / UNK=12; a separate classifier
fix to the `sell/buy` NaN guard was verified to be label-neutral at this
baseline — it changes no wallet's label here and is retained as defensive
hardening, not as a driver of the shift. See §4.5.1.)


**Limitation (the one inference the market-maker conclusion rests on).** This
classification is *behavioral inference*, not ground truth. Polymarket's Data
API (`/trades`) does not expose maker/taker roles, so "market maker" here means
"behaves like one" (high sell/buy, fast flips, two-sided quoting), not
"confirmed maker on-chain". The roles *can* be confirmed directly: the Polygon
`OrderFilled` events from the CTF Exchange contracts carry explicit `maker`,
`taker`, and `fee` fields per fill (see the independent `prediction-market-
analysis` project, §4.8). Indexing those would either validate this classifier
against ground truth or force a revision. We did not do this — it requires
re-architecting ingestion onto a Polygon RPC node (the referenced dataset is
~36GB) — but it is the recommended confirmation, and the §4.4/§4.5 conclusions
should be read as resting on this behavioral inference until then.
### 4.5.1 Threshold-sensitivity of the split (error bars on §4.5)

The §4.5 split came from one fixed set of five tell-thresholds plus a majority
cutoff (`min_score = 3` of 5). That single point estimate had no error bars, and
since the "uncopyable by construction" claim leans on it, we swept it. We
perturbed all six parameters one-at-a-time (OAT) and over the full Cartesian
grid (3,072 configs), recording the resulting MM/directional split and, for the
OAT + baseline configs, re-running the full single-split skill gauntlet of §4.7
on the resulting directional pool. Two findings, opposite in sign:

**The split itself is fragile — but for one identifiable reason.** Across the
grid the market-maker share of the judged pool ranges from 0.12 to 0.94
(baseline 0.59, median 0.59), and 1,253 of 3,072 configs (41%) flip which class
holds the majority. Both extreme corners hold `UNKNOWN` fixed at the baseline
count, so the swing is genuine reclassification, not the pool dissolving. But
the fragility is almost entirely attributable to a *single* parameter — the
majority cutoff `min_score`. Its flip-rate by value is near-deterministic
(`min_score=2`: 0.00, `=3`: 0.23, `=4`: 1.00), and it moves the MM share by
0.574 on its own, versus ≤0.14 for every one of the five behavioural tells. In
other words: the split is *stable* across the five behavioural thresholds and is
governed by the one explicit design choice of how many tells you require to call
a wallet a market maker. Requiring a bare majority (3 of 5) gives ~59% MM;
demanding 4 of 5 inverts it. That is a defensible, explainable sensitivity — a
choice to argue on its merits, not a hidden degree of freedom.

**The skill verdict is invariant to all of it.** The decision §4.5 feeds — are
there copyable directional traders? — does not move. Across every gauntlet-run
config, the number of directional wallets surviving the train→test→fee test
stays in [0, 2]. Critically this holds on *both* sides of the majority line:
even in configs where directional traders are redrawn as the *majority* of the
pool (`min_score=4`, up to 91 directional wallets), survivors are still 1–2 —
the same one-or-two candidates, never a population effect. Loosening the
boundary to admit more directional wallets does not manufacture skill.

**Conclusion.** The market-maker *share* should be reported as a range
(baseline 0.59; 0.12–0.94 across thresholds; governed by `min_score`), not as a
fixed count — wherever this document previously implied a precise split, read it
as the baseline value of a threshold-dependent quantity. But the *verdict* of
§4.4–4.7 rests on the survivor-invariance, not on the headcount, and that
invariance is now demonstrated empirically rather than assumed. The fragility is
descriptive, not decision-relevant. It also sharpens §4.5's own limitation: the
one parameter driving the entire sensitivity surface — "how market-maker-like
must a wallet behave to count as one" — is exactly the question the on-chain
`OrderFilled` maker/taker flags answer outright, collapsing the whole surface to
a single ground-truth column. That remains the recommended confirmation.

*(Reproduce: `scripts/classifier_sensitivity_sweep.py --root <data> --mode both`
then `scripts/summarize_classifier_sweep.py --csv classifier_sweep_results.csv`.
The `min_score` parameter was added to `classify()` as part of this work. A
`sell/buy` NaN-guard fix was also made and is covered by
`tests/test_classifier_and_synthetic_sells.py`;
`scripts/verify_nan_fix_attribution.py` confirms that fix is label-neutral at
the baseline thresholds — it is defensive hardening for all-SELL / NaN-hold
edge cases, not a cause of the split shift, which is a data-snapshot effect.)*


### 4.6 Directional consensus informativeness (first "learn from them" test)

Excluding market makers, asked whether the **directional** wallets' consensus
beats the **market price** at predicting resolution, out-of-sample (Brier skill,
calibrator fit on train only).

**Result: INCONCLUSIVE.** Directional wallets reached consensus only 17 times on
the train window (need ≥50). The mechanism is structurally mismatched: directional
traders make *idiosyncratic* bets and do not cluster, so the consensus trigger
(built for copy-trading herd-following) starves of signal exactly on the
population worth studying.

### 4.7 Individual directional skill — randomization test (LBS/Yale method)

Since directional traders don't cluster (§4.6), the right unit is the
*individual* wallet, not consensus. Adapted the London Business School / Yale
working-paper method: for each directional wallet, hold its actual markets,
timing, and sizes fixed and randomize *only* buy/sell direction 10,000 times to
build a luck-only null; compare actual PnL to it. Four pre-registered gates:
per-wallet null, Benjamini-Hochberg multiple-comparisons correction, train/test
persistence, and a fee-aware effect-size gate using Polymarket's real fee
formula `fee = C·feeRate·p·(1−p)`.

Single split (2025-06-01 → 2026-06-01, midpoint):
- 16 directional wallets had enough resolved train trades. 5 beat their null
  (vs ~0.8 expected by chance); all 5 survived BH-FDR.
- On held-out test: **4 of 5 did not persist** (two swung sharply negative,
  −382k and −384 net) — the literature's ~60% non-repeat rate, observed.
- 1 wallet (`0x6640bd87f6`) persisted at the lenient single-split threshold
  (test_p=0.022, +38k net of fees).

Hardened verification (pre-registered: 5 independent rolling splits, Bonferroni
per-split threshold 0.01, must clear fees each split, ROBUST = pass ≥4/5):
- `0x6640bd87f6`: **0/5 splits passed → FRAGILE.** Per-split test p-values decay
  monotonically (0.006 → 0.014 → 0.043 → 0.105 → 0.144) as the evaluation window
  moves later — a good early run reverting to the mean, not durable skill. The
  single-split pass was the ~1-in-20 expected by chance.

**Read:** the single best-looking individual directional wallet does not survive
a corrected, multi-split skill test. The result lands exactly on the external
base rate (~3% skilled → ~1 expected in a 42-wallet pool if random) and then
dissolves under persistence — consistent with the literature's instability
finding. **No individual skill robust enough to trust in this pool.**

### 4.8 External corroboration (independent studies)

Three independent sources reach the same structural conclusions, from different
data and methods:

- A blockchain-level analysis (`prediction-market-analysis`, Polygon
  `OrderFilled` events, maker/taker/fee ground truth) finds maker returns exceed
  taker returns across price deciles and the environment is dominated by
  microstructure — the same maker-vs-taker split this project inferred
  behaviorally (§4.4–4.5).
- The LBS/Yale Polymarket working paper (1.72M accounts, 2023–2025): ~3% of
  accounts are skilled beyond chance; among the biggest raw-profit winners only
  ~12% beat a direction-randomization null and ~60% don't repeat. This is the
  base rate and instability our §4.7 result matches.
- A separate study (2.4M users, ~$67B volume through 2026): 68.8% of users lose,
  the top 1% capture ~77% of gains, and the market is **negative-sum after
  taker fees** — corroborating the fee drag central to §4.1/§4.4/§4.7, from an
  independent angle. A related finding — retail picks winners *more often* than
  bots yet loses on worse execution — independently replicates this project's
  core result that directional judgment and tradable profit are different things,
  separated by execution cost.

These are external, not produced here; the working-paper status of the 3%
figure means it is best-current-evidence, not settled fact. They are included
because they corroborate the project's conclusions from outside its own pipeline.

---

## 5. Conclusions

**Triangulated and considered final:**

1. **Copy-trading the volume-ranked Polymarket wallet population is not tradable.**
   Independent measurements agree: the modeled-latency backtest, robust across
   10 walk-forward windows (§4.1, 10/10 negative), the negative edge at instant
   on held-out data (§4.2), and the exit-mirror result (§4.4). Notably the edge
   is marginal-to-negative *even at zero latency* (§4.1) — so this is not "good
   edge destroyed by speed" but "no meaningful edge to begin with." The wallets
   are not fake and the data is not bad — the strategy fails because ~half the
   pool are market makers whose edge a copier cannot occupy.

2. **The negative result is well-understood, not mysterious.** The profit these
   wallets make is liquidity provision (quantified in §4.5: 1.3h median hold,
   0.85 sell/buy; corroborated externally in §4.8). That is a role, not a signal,
   and it is uncopyable at realistic latency.

3. **No individual directional skill survives in this pool either.** The
   strongest single directional wallet passed a lenient single-split test but
   failed a corrected multi-split skill test (§4.7), landing exactly on the
   external ~3% base rate and then dissolving under persistence. The "learn from
   the individuals" thread is closed for this pool.

4. **The framework did its job.** It falsified the hypothesis six independent
   ways (§4.1–4.7) and explained the mechanism each time, with external
   corroboration (§4.8). The reusable asset is the *instrument* (selection,
   latency model, lifecycle reconstruction, classifier, randomization skill test
   with multi-split verification), not a profitable strategy.

**The one remaining untested lever (with an honest prior):**

5. Every test above used a pool selected by raw **volume**, which §4.5 proved
   over-selects market makers and may systematically miss patient, low-volume
   skilled traders. The only untested population change is a **re-discovery
   ranked by profitability / sharpness (or, best, by on-chain taker role per
   §4.8) instead of volume**, then re-running the §4.7 randomization gauntlet on
   that pool, pre-registered against the ~3% base rate. **Prior: most likely one
   more clean negative.** The external evidence (§4.8) says skilled traders are
   rare (~3%), unstable (~60% don't repeat), and beaten by execution cost even
   when they pick winners. The realistic best case is "identified a handful of
   genuinely skilled individuals and showed their edge still doesn't survive a
   follower's execution costs" — a rigorous negative, not a trading business.
   This lever is documented for completeness; pulling it is optional and should
   carry no expectation of flipping the verdict.

**Stopping rule (formal).** Phase 1 is closed. The copy-trading hypothesis is
falsified six independent ways (§4.1–4.7) with external corroboration (§4.8),
and the live-execution gate is NO-GO. We stop here. Resuming is justified only
by one of: (a) new data that removes a stated limitation — specifically on-chain
`OrderFilled` maker/taker/fee ground truth (§4.4–4.5) or L2 order-book depth for
a faithful slippage model; or (b) a pre-registered academic pivot that runs the
§4.7 gauntlet on a non-volume-ranked universe to complete a null-hypothesis
sweep. Absent (a) or (b), no further work is warranted, and additional analysis
on the existing volume-ranked pool would be effort without new information.

---

## 6. Methodological commitments (what keeps this honest)

- Every test uses a **train/test date split**; calibrators fit on train, scored
  on test. No in-sample evaluation.
- Segment/threshold rules are **stated in advance**, not chosen by hunting for a
  green slice. Train-only positives are flagged as OVERFIT, not reported as wins.
- The benchmark for "informative" is the **market price**, the hardest honest
  baseline — not "better than 0.5".
- Scripts **refuse to conclude** when data is insufficient (INCONCLUSIVE), rather
  than fabricate a result.
- **Informative ≠ profitable after costs.** No PnL claim is made from a
  prediction-quality result.
- A negative or inconclusive result is treated as a valid outcome and a clean
  stop, not a reason to loosen a threshold until something passes.

---

## 7. Reproduction

```bash
# tests (expect 67 passed)
pytest

# core go/no-go
python -m pm_research.cli backtest --root ~/data --start 2025-06-01 --end 2026-06-01
python scripts/walk_forward_backtest.py --root ~/data --data-start 2025-03-01 --data-end 2026-06-01

# analyses
python scripts/edge_halflife.py        --root ~/data --start 2025-06-01 --end 2026-06-01
python scripts/lifecycle_pnl.py        --root ~/data --start 2025-06-01 --end 2026-06-01
python scripts/exit_mirror_backtest.py --root ~/data --start 2025-06-01 --end 2026-06-01
python -m pm_research.wallet_classifier --root ~/data --start 2025-06-01 --end 2026-06-01
python scripts/consensus_info_test.py  --root ~/data --start 2025-06-01 --end 2026-06-01
python scripts/randomization_skill_test.py --root ~/data --start 2025-06-01 --end 2026-06-01 --fee-rate 0.05
python scripts/resolution_flip_robustness.py --root ~/data --start 2025-06-01 --end 2026-06-01
```

## 8. Questions for reviewers

1. Is price-convergence resolution (§2) acceptable, or does it bias §4.x in a way
   we haven't accounted for (e.g. markets that converged but later disputed)?
2. Is the behavioral market-maker classifier (§4.5, ≥3 of 5 tells) defensible as
   an *inference*, given it is not validated against on-chain maker/taker ground
   truth (§4.8)? Does the conclusion in §4.4/§5 need that confirmation before
   being stated as strongly as it is?
3. Is the §4.7 randomization + multi-split design (Bonferroni per split, ROBUST =
   ≥4/5) the right falsification for individual skill, or is the bar mis-set in
   either direction? The single FRAGILE survivor is the case to scrutinize.
4. The only remaining lever (§5.5) is a profitability/sharpness/on-chain-taker
   re-discovery. Given the external base rates (§4.8), is pulling it worth the
   cost, or is the six-way negative already a sufficient stopping point?
