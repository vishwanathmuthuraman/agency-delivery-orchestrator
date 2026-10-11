# 04 — Evaluation protocol

**Proposed protocol 0.1. No application runs or measured scores exist.** The six public examples specify a bounded control replay. They supply reviewed impact and prepared content as trusted simulated events; they cannot prove the system discovered dependencies or generated corrections. Evaluate those capabilities separately.

## 1. Questions and fair comparisons

The primary study asks whether selective revalidation can reduce unnecessary review while preserving the same dispatch and completion guarantees. It does not compare this prototype with the actual performance of any commercial vendor.

| Strategy | Planned behavior | What remains identical |
|---|---|---|
| Dispatch-only recheck | Recheck eligibility when an action is attempted; no eager campaign-wide invalidation work | Observed source/content state, reviewed dependency graph, authority, commercial policy, final guard and mock connector |
| Invalidate-all | Reopen all current campaign approvals after a committed source change | Same evidence and guard; intentionally broader review work |
| Selective | Reopen affected approvals using accepted dependency paths and surface ambiguous candidates | Same evidence and guard; links are not privileged hidden truth |

All three strategies must refuse stale or unauthorized dispatch through the shared guard. Do not attribute that common safeguard exclusively to selective invalidation. Dispatch-only can incur late interruption; invalidate-all can create avoidable review. Their tradeoffs are the experiment. Record eager invalidations separately from final-guard holds.

For an independently verified fact invalidation, every strategy must immediately prevent affected dispatch under the common hold policy. Selection changes review workload, not permission to use known-invalid content. Differences in accepted dependency quality belong to a separate extraction study.

## 2. Corpus and units

The six supplied public starter scenarios remain teaching/regression cases. They are excluded from counts below. Plan an additional 36 development scenarios and 36 held-out scenarios, each spanning six families:

1. Source-fact and downstream-content changes.
2. Revision and approval mismatches.
3. Required inputs, task dependencies and capacity conflicts.
4. Duplicate events, retries and conflicting intents.
5. Uncertain outcomes, observations and recovery.
6. Tenant boundaries, authority and untrusted content.

Within each partition, each family contains six cases: three requiring an additional intervention or denial and three matched valid controls. A control can include a safely resolved retry; it need not be a trivial no-op. A legitimately unresolved external outcome has an oracle of unresolved, not a forced-success target. Freeze exact case classifications before scoring.

The primary held-out study is **36 scenarios × 3 strategies = 108 deterministic replays**. These are not 108 independent customer incidents. Keep shared template/incident ancestry in the same partition, including clean/fault pairs and parameter variants. New IDs or random seeds alone do not establish independence.

Create the held-out set only after development decisions are stable. A separate reviewer should hold labels and inspect realism where available. If the same author builds and labels everything, disclose the limited blinding. Once published or inspected during tuning, cases become regression data; new independent claims require new withheld cases.

## 3. Truth, projections and event order

Manually derive expected affected deliverables, required review purposes, acceptable terminal states and forbidden side effects. Preserve an explanation with each oracle. Verify fault triggers; quarantine ambiguous or non-triggered cases before the freeze and record why.

Runtime projections contain only the current authorized campaign state, observed events, policy and accepted evidence. Remove scenario descriptions that reveal the answer, expected files, family/split labels, future events and oracle IDs. Use opaque runtime case IDs and a controller-only join table. Test with canary labels and shuffled filenames to detect leakage.

Control replays may supply reviewed-impact and completed-work events to test transitions. They cannot then score those same supplied answers as discovered insights. For extraction evaluation, capture proposals before revealing reviewed impact, corrections or reviewer labels. For generation evaluation, provide only the permitted pre-change content, source facts and task instructions, not prepared target text.

Freeze a virtual-time schedule and connector faults per case. Record attempts, effects, observations and reconciliations independently. The public `expected_external_write_count` is a count of attempted mock writes; never relabel it successful publications or unique effects.

### Shared reviewer behavior

Freeze exogenous changes, input arrivals and connector fault rules equally across strategies. Review-response events must instead be generated from each strategy's actual requests by the same deterministic reviewer simulator. Otherwise invalidate-all could be stranded because its additional requests never receive the decisions supplied for the selective strategy.

Use one FIFO reviewer queue per authorized role, two virtual ticks of service per request, and stable subject ID plus purpose as the tie-break for simultaneous requests. Check the same public authority rules, current versions and observed acceptance evidence for every strategy. An unchanged eligible artifact can receive a fresh approval; stale or uncorrected content must be rejected or returned for work. The reviewer cannot read hidden labels or approve a commercial choice that the frozen scenario has not authorized. Duplicate requests for the same subject/version/purpose share a queue item.

Additional legitimate requests incur additional review items and queue time. Record generated response events separately from fixed external inputs, continue simulation until the accepted terminal result or shared cap, and report every cap breach. Fault injection keys use logical intent and attempt number rather than the count of unrelated review events. Freeze the reviewer implementation and policy hash with the protocol. The six public supplied-event fixtures remain contract replays; they are not the comparative reviewer experiment.

## 4. Metrics and denominators

| Metric | Definition |
|---|---|
| Unsafe dispatch | Count of effects initiated without the required current authority/content/source state, plus affected runs / all assigned runs. Report every instance. |
| Cross-tenant disclosure | Unauthorized canary/content exposures or mutations, reported individually and by run count. |
| False completion | Runs marked verified/complete despite missing required evidence / all assigned runs. Unknown is not complete. |
| Required-intervention coverage | Oracle-required interventions correctly raised / all required interventions, including timed-out runs as unfulfilled. |
| Affected-set precision/recall | Correct affected deliverables / selected deliverables, and correct selected deliverables / oracle affected deliverables. Undefined zero denominators remain undefined. |
| Unnecessary invalidation | Unaffected current approvals reopened / eligible unaffected approvals. Record raw numerator and denominator per strategy. |
| Useful completion | Runs reaching an oracle-accepted terminal result with required eligible work completed / all assigned runs. Block-all cannot pass. |
| Interruption delay | Virtual ticks from observed change to relevant hold/review; report by event type and include late/no-detection counts. |
| Work proxy | Review items, evidence reads, recalculations, write attempts and reconciliations per run. These are not human hours. |
| Runtime coverage | Runs producing a complete interpretable result / 36 per strategy, with errors/timeouts separately listed. |

An accepted terminal result can be blocked or reconciliation_required when the scenario requires it. This does not excuse unrelated eligible work being abandoned. Record that work explicitly. The public selective-specific expected invalidation list is not a universal correctness rule for invalidate-all; score its extra work as intended by its policy. Global forbidden outcomes apply to every strategy.

Report per-family counts, paired strategy differences and all failures. If calculating uncertainty, cluster at the highest shared template lineage; small independent-group counts may make interval estimates unstable. Synthetic family balance is not real-world incident prevalence. Do not infer live precision, hours saved or return on investment from these counts.

## 5. Budgets and failure accounting

Proposed primary caps: 200 virtual ticks, 100 simulated connector operations and 30 wall seconds per replay on a documented machine. Freeze these before held-out runs. A cap breach is an incomplete run, never silently excluded or counted as a correct denial. Distinguish application error from the deliberately injected connector uncertainty.

Retain the original attempt and any permitted infrastructure retry. A retry cannot become an opportunity to alter policy, hints, inputs or expected outcomes. If a sealed case is later found invalid, publish original-assignment counts and a separately corrected analysis with reasons; apply corrections consistently to all strategies.

## 6. Optional model study

This branch is not required for deterministic v1 completion and must be marked deferred if absent. Proposed held-out subset: 12 cases selected by manifest before outcomes, two bounded proposal samples each, totaling 24 samples. Freeze provider/model snapshot, prompt, projection, schema, generation limits, cost ceiling and failure policy on development data. No paid calls are authorized by this document.

Score dependency proposals against independently reviewed evidence, including unsupported links and abstentions. Score text changes for source support, correct scope, preservation of unrelated meaning and required human review. Cache each proposal before downstream control replay. A model-selected dependency study cannot use the accepted graph as hidden answer material in the prompt.

Retain malformed output, timeout and unsupported claims as outcomes. Do not regenerate until a preferred answer appears. Report measured API cost and latency separately from control runtime; human review effort is measured only if a real timed study is conducted. A negative result can justify keeping explicit human-reviewed edges.

## 7. Completion evidence

Each future run manifest records code/lock/configuration hashes, schema/policy version, scenario hash, split manifest, virtual schedule, seed, strategy, machine/runtime and artifact digests. Store observations, predictions and oracle joins separately. Publish the protocol, aggregate results, failure inventory and reproduction instructions once reviewed.

Meeting the protocol means executing and accounting for the study faithfully. Meeting performance targets is a different claim. The [completion gates](05-definition-of-done.md) preserve that distinction.
