Claude, new task: design the Dune wallet-discovery spec for the named-binary branch.

First, read the pinned project files — especially PROJECT_STATE.md (§8 yes_price rewrite, §9 this parallel task), GUARDRAILS.md, and DECISION_LOG.md. This spec must reconcile with them.

## Direction

After Rank 2 closure, I want to move toward the named-binary unlock (yes_price rewrite), but I also want to stop being limited by the saved 250 volume-ranked wallets. Question: can we use Dune to discover a better wallet universe based on what Rank 2 taught us? Decision: yes — but ONLY as wallet-universe discovery / cohort construction. Not copy-trading, not performance-chasing.

## Critical reconciliation requirement (read before designing)

The "named-binary" definition is the SAME semantic problem the yes_price rewrite (PROJECT_STATE §8) must solve. Do NOT invent a second, independent definition here. The named-binary classification rules (YES/NO vs OVER/UNDER vs UP/DOWN vs team-vs-team vs unusable) must be specified ONCE — owned by the yes_price rewrite — and this discovery spec should CONSUME them, not duplicate them. Where this spec needs classification logic that the yes_price rewrite hasn't defined yet, flag it as a shared dependency rather than defining it ad hoc. The two branches must not drift into inconsistent definitions of the central concept.

## Context (from CLOSED_FINDINGS / DECISION_LOG — do not re-derive)

- Rank 1A YES/NO price-recalibration: closed negative.
- Rank 2 role-recovery: economic role is recoverable via OrdersMatched (takerordermaker = economic taker; maker via positive OrderFilled pairing).
- Expanded role distribution: STABLE_MIXED / taker-leaning / wallet-level bimodal (117 trades, 96 wallets).
- Original "wallets are mostly makers" H1: NOT supported.
- Not doing PnL-by-role now. Not reviving wallet-copying. Not testing named-binary until yes_price semantics are fixed.

## Design the spec to cover:

### 1. Objective
Use Dune to discover wallet cohorts relevant to named-binary markets — broader and better-targeted than the old saved 250 volume-ranked wallets.

### 2. Wallet cohort definitions
- named-binary active wallets
- named-binary maker-type wallets
- named-binary taker-type wallets
- mixed / control wallets
- optional high-diversity wallets
(Reuse the validated Rank 2 role-recovery machinery for maker/taker typing — OrdersMatched takerordermaker. Note the bimodal finding: typing needs adequate per-wallet depth, not n=1.)

### 3. Dune data sources
- polymarket_polygon.market_trades for broad wallet/market activity
- OrdersMatched event tables for economic role if needed (polymarket_polygon.ctfexchange_evt_ordersmatched / negriskctfexchange_evt_ordersmatched — old contracts; remember the varchar-cast lesson from DECISION_LOG)
- market metadata tables for question/outcome labels
- hourly prices only if needed for diagnostics

### 4. Named-binary identification
Define how this spec OBTAINS the classification (YES/NO, named-binary, OVER/UNDER, UP/DOWN, team-vs-team, unusable/ambiguous) — preferably by consuming the yes_price rewrite's rules. If those rules don't exist yet, specify the minimal shared contract this spec needs from them.

### 5. Selection criteria (per wallet)
- minimum named-binary trade count
- minimum unique conditions
- minimum active days/weeks
- maximum concentration in one condition
- role sample depth (per the bimodal lesson — n must be deep enough to type a wallet)
- role share thresholds
- exclude pathological wallets if needed

### 6. Anti-leakage design (non-negotiable)
- discovery window vs holdout window, strictly separated
- do NOT select wallets on full-period profitability
- do NOT use future outcomes in discovery
- cohort defined on discovery, never evaluated on the same data

### 7. Output artifacts
- artifacts/dune_named_binary_wallet_candidates.sql
- artifacts/named_binary_wallet_cohorts.json
- artifacts/named_binary_wallet_cohorts.csv
- artifacts/named_binary_wallet_discovery_report.md

### 8. Local integration
How the discovered wallet list feeds the local pipeline: backfill selected wallets if needed; join named-binary outcomes; apply the yes_price rewrite; evaluate wallet-flow features ONLY after semantics are fixed and audit-gated.

### 9. Guardrails (restate and honor)
No wallet-copying. No live/paper trading. No PnL-based selection without holdout. No category-specialist claim yet. No named-binary test until yes_price semantics are fixed.

### 10. Sequencing recommendation (answer explicitly)
Tell me whether this discovery spec should be built before, after, or in parallel with the yes_price rewrite — and justify it given that §4 depends on the rewrite's named-binary classification. Be honest if the dependency means parts of this spec cannot be finalized until the rewrite lands.

End with a Claude-to-Orchestrator handoff memo and a list of any open design questions you need me to resolve before implementation. Spec only — no implementation.
