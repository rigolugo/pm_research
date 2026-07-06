# OPTION C AUTHORIZED — SPEC ONLY

APPROVE.

The user explicitly authorized Option C after Claude correctly noted that earlier project context treated it as out of scope.

This is a narrow reversal for documentation only. Claude may draft:

- `SPEC_price_source_option_c_onchain.md`
- `HANDOFF_orchestrator_option_c_onchain_spec.md`

The spec must preserve current state:

- P1 remains blocked on missing per-side / token-identity price input.
- B1 remains unauthorized.
- P2/P3/probe remain unauthorized.
- `named_binary_probe_blocked` remains true.
- A favorable Option C spec does not unblock P1 by itself.

The spec must not include implementation, run commands, data collection, indexing, scoring, wallet work, or downstream probe work.

Claude should read this file after the normal required read order and then produce the two spec-only deliverables for orchestrator review.
