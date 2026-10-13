# 05 — Definition of done

**Full workflow and evaluation targets remain unachieved.** Initial components are recorded in [IMPLEMENTATION.md](IMPLEMENTATION.md). A detailed document is not a working product. Use the following four research gates and record actual evidence, date, reviewer and software/document revision. The broader AI project lead additionally requires [Product Gate E](10-ai-project-lead.md#build-sequence-and-release-boundary), including grounded model proposals and Slack/email coordination; the offline gates alone do not complete it.

## Gate A — Blueprint complete

- README explains the scope, current status and future commands accurately.
- Eight numbered documents, schemas, six original synthetic scenarios and separate expected specifications exist and agree.
- Requirements have acceptance criteria and map to the [public milestones](03-build-plan.md).
- Source provenance, existing-product overlap and limitations are documented without a novelty claim.
- Documentation checks pass: schemas, references, arithmetic and local links.
- The public documentation accurately reflects the specification and distinguishes planned work from verified artifacts.

Passing this gate means a reviewer can start implementation. It does not mean expected outcomes occurred or the application is safe.

## Gate B — Offline v1 complete

Milestones M1–M4 have completion evidence; optional model/UI branches are not required. In addition to replaying all six public cases, a separate full-lifecycle integration demonstration must exercise input collection, task readiness, capacity conflict, bounded reminders, baseline revision, supported correction, human editing handoff, role-specific review, mock dispatch, reconciliation and closure.

The six starter examples alone do not cover every lifecycle requirement. They also supply reviewed impact and prepared revisions. Their replay cannot prove semantic discovery or autonomous creative production.

| Requirement group | Future verification evidence | Milestone |
|---|---|---|
| FR-01, FR-19 | Contract rejection, atomic import, duplicate/conflicting events, repeatable replay and restart | M1, M4 |
| FR-02 | Tenant canaries across storage, cache, errors, model context and exports | M1 |
| FR-03, FR-06 | Immutable baseline, rate versions, half-up arithmetic and distinct cost/fee records | M2, M3 |
| FR-04–FR-07 | Missing inputs, readiness graph, capacity conflict and reminder deduplication | M2 |
| FR-08–FR-10 | Evidence-linked impact, known-change handling, uncertainty and rejection of unsupported proposals | M3 |
| FR-11–FR-13 | Authorized commercial choices, exact-base text patches, editing packets and current approvals | M3 |
| FR-14–FR-16 | Final guard race, idempotency conflicts, outbox durability and unknown-outcome recovery | M4 |
| FR-17–FR-18 | Observed target version, explicit acceptance and draft billing packet | M4 |
| FR-20 | Shared-guard comparisons, no hidden labels, meaningful metrics and failure accounting | M5 |

All mandatory behavior must be verified in the offline simulator. Zero unresolved known defects may permit unauthorized dispatch, cross-client disclosure, duplicate effects under the declared mock contract, or false claims of verified completion. A UI screenshot is not evidence that those properties hold.

## Gate C — Evaluated research artifact

Milestone M5 requires the following evidence: 36 additional development and 36 held-out scenarios exist, group splits are reviewed, the protocol is frozen, and all 108 held-out replays are accounted for. Publish actual results and shortcomings. Any model study is separately complete or explicitly deferred.

Proposed product-performance targets, not established industry standards:

1. Zero unsafe dispatches, cross-tenant disclosures or false completions in the frozen deterministic study.
2. Every oracle-required denial or unknown-outcome hold is correctly represented. Missing evidence remains missing.
3. Each strategy completes the eligible work and reaches an acceptable terminal state in at least 34 of 36 held-out scenarios, with all failures explained. Safety violations cannot be offset by successful cases.
4. Selective invalidation identifies every affected deliverable in cases with a complete reviewed graph. This tests traversal, not model extraction quality.
5. Selective invalidation causes fewer unnecessary reopened approvals than invalidate-all on the frozen change subset, while reporting any additional computation. No minimum time or cost saving is assumed.

A reproducible study with failed performance targets can be a completed research artifact. It cannot be labeled operationally validated. A study with missing runs, changed hidden labels or unreported errors remains incomplete. If critical safety defects are discovered, fix and publish regression results; a fresh held-out set is needed for a new independent claim.

## Gate D — Public release ready

Milestone M6 requires completion of the [publication checks](08-publication.md). Select licenses, inspect files/history, verify attribution and privacy, reproduce installation and review all outward claims. The public README must identify which earlier gates actually passed. Public readiness is separate from live customer readiness.

A real pilot additionally needs authorized access, production authentication, deployment and retention decisions, connector-specific guarantees, documented reviewers and an agreed rollback/incident process. Those are future scope, not accomplished by the offline prototype.

## Seven-minute demonstration target

1. **0:00–1:00:** explain synthetic scope; show approved brief, task graph, budget and a missing input.
2. **1:00–2:00:** receive the input, resolve a capacity proposal and show bounded coordination through a handoff.
3. **2:00–3:00:** change a product claim; inspect affected and unaffected work with evidence paths.
4. **3:00–4:00:** inspect deterministic extra cost, approve an absorb decision and prepare a caption patch plus a human editing packet.
5. **4:00–5:00:** demonstrate why old approval cannot authorize a new revision; record fresh decisions.
6. **5:00–6:00:** show a duplicate/uncertain mock dispatch, reconciliation evidence and the exact observed version.
7. **6:00–7:00:** close eligible work, inspect billing-readiness evidence and show measured results or a clear “not yet evaluated” label.

Keep the demonstration honest when a step is simulated. Never describe an editing packet as a completed video or a mock destination as a public post.
