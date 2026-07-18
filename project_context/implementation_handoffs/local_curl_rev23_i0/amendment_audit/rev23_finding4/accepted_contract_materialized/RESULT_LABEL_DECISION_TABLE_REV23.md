# RESULT-LABEL DECISION TABLE — Local-Curl Revision 23

| Order | Exact condition | Label/outcome | Interpretation boundary |
|---:|---|---|---|
| 1 | finalized pre-run stop | `typed pre-run stop code only` | no empirical result; run_id absent |
| 2 | unfinalized pre-run/run finalization residue | `UNFINALIZED_OPERATIONAL_RESIDUE` | operational residue only |
| 3 | run-scoped structural stop | `typed run stop code only` | no coverage inference |
| 4 | incomplete closure disposition or unproven reservation | `STOP_REQUEST_POPULATION_INCOMPLETE` | missing evidence is not empty series |
| 5 | 496 token vector all one or 248 pair vector all one | `LOCAL_CURL_REPLAY_INCONCLUSIVE` | all-one safeguard |
| 6 | strict completed-response compatibility disagreement | `LOCAL_CURL_REPLAY_INCONCLUSIVE` | strict diagnostic cannot support reproduction |
| 7 | any subclass THRESHOLD_INCONCLUSIVE | `LOCAL_CURL_REPLAY_THRESHOLD_INCONCLUSIVE` | below-threshold labels forbidden |
| 8 | all 248 comparisons exact; numerators exactly 19/50, 51/98, 65/100; no unresolved | `LOCAL_CURL_REPLAY_REPRODUCES_S1_NEGATIVE` | exact accepted negative reproduction |
| 9 | comparison complete; at least one transition; no threshold inconclusive; at least one subclass fails | `LOCAL_CURL_REPLAY_DIFFERS_FROM_S1_BELOW_THRESHOLD` | comparison difference, not causal attribution |
| 10 | all subclasses clear; comparison complete; confirmed transitions are gains only | `LOCAL_CURL_REPLAY_SAMPLE_COVERAGE_CLEAR` | sample threshold only; no P1 viability |
| 11 | all subclasses clear; comparison complete; at least one confirmed loss also exists | `LOCAL_CURL_REPLAY_COVERAGE_CLEAR_WITH_COMPARISON_DIFFERENCES` | nonmonotone comparison differences |
| 12 | otherwise | `LOCAL_CURL_REPLAY_INCONCLUSIVE` | total residual branch |

Threshold formula per subclass:

```text
lower_rate = confirmed_both_numerator / fixed_denominator
upper_rate = (confirmed_both_numerator + unresolved_count) / fixed_denominator
CLEAR if lower_rate >= 0.95
FAIL if upper_rate < 0.95
otherwise THRESHOLD_INCONCLUSIVE
```

Exact accepted-S1 reproduction is necessarily below threshold and cannot enter either clear branch. Clear branches are mutually exclusive by `confirmed_loss_count == 0` versus `> 0`. No causal language is authorized.
