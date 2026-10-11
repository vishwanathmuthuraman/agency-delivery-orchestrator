# 02 — Architecture and behavioral contracts

**Proposed architecture; application modules do not exist yet.** JSON schemas in `schemas/` are the field-level contracts. The semantics below govern implementation; if a fixture and this document disagree, resolve and record the conflict before coding rather than silently choosing one.

## 1. Bounded design

Use Python 3.12, SQLite, a CLI and a local report. Keep one package with explicit modules before introducing services. Suggested future directories are `domain/`, `storage/`, `planning/`, `changes/`, `execution/`, `connectors/`, `agents/`, `replay/`, `evaluation/` and `reports/`. These are proposed paths, not present modules.

The runtime flow is: validate input → append observed event → materialize state → identify eligible work or review → calculate a proposed action → authorize exact versions → perform final dispatch checks → invoke the supported connector → reconcile and verify. The reporting layer reads evidence; it must not invent new state.

Default operation is offline. A deterministic mock model can demonstrate proposed extraction without claiming model intelligence. The optional model interface returns structured proposals only. A future UI consumes the same application services; duplicating money or authorization logic in a UI is prohibited.

## 2. Domain records and identifiers

| Record | Meaning and required semantics |
|---|---|
| Tenant and campaign | Every campaign belongs to exactly one tenant. All queries use both identities; a guessed record ID cannot escape that boundary. |
| Commercial baseline | Immutable accepted scope, deliverable list, schedule assumptions, budget and rate references. A baseline revision needs an authorized commercial decision. |
| Source fact | Stable fact identity plus monotonically increasing immutable revision, value, origin and observed time. Examples include product claim or disclaimer. |
| Deliverable | Stable identity and kind with immutable content revisions, acceptance criteria and intended destinations. Status alone does not identify content. |
| Dependency | A typed edge from source/upstream content to downstream deliverable or task, with cited evidence, scope and review status. Direction means upstream change may affect downstream work. |
| Task | Owner, prerequisites, required inputs, estimated minutes, explicit output and state. Task completion supplies evidence but cannot automatically grant client approval. |
| Approval | Actor, purpose, decision, target identity/revision, relevant source revisions, policy version, observation time and optional expiry. Revocation is append-only. |
| Change case | Triggering revision, affected paths, uncertainty, proposed work, commercial alternatives and resolution history. Separate from a task or final deliverable. |
| Action intent | Stable logical action identity, immutable payload digest, target revision, authorization references and connector destination. |
| Receipt and observation | Attempt outcome plus independently obtained destination state. Request acceptance and verified content are distinct facts. |
| Audit event | Actor or system component, tenant/campaign, event identity, type, observed time, evidence references and resulting transition. |

Use opaque string IDs. Do not encode secrets, customer names or hidden evaluation labels into IDs. Enforce composite uniqueness or tenant-qualified foreign keys. Refuse cross-tenant references before fetching referenced content, including evidence snippets and error messages. Tenant-aware cache keys include tenant, input digest, model/configuration and schema version.

## 3. State machines

State names here are behavioral concepts; map concrete enum names to the published schemas when implementing.

**Campaign:** draft → baseline_review → active → closure_review → closed. It can enter paused or cancelled from appropriate active states. Reopening a closed campaign requires a recorded reason and new review; it cannot erase the prior closure packet. Closed means the defined scope is resolved and evidence assembled, not that an invoice is paid.

**Task:** blocked → ready → in_progress → awaiting_review → completed. Review rejection returns work to ready with a new revision request. Cancelled is explicit. A stale output can create new corrective work; do not rewrite history to imply the original task never completed. Only the dependency and input rules determine readiness.

**Deliverable revision:** draft → in_review → accepted → dispatch_ready → verification_pending → verified. Rejected or superseded revisions remain in history. A change can remove current eligibility even when the old content bytes are unchanged. Already delivered content opens a correction case; it is not magically undone.

**Approval:** proposed decision → granted or denied; a grant may become expired, revoked or invalidated. Commercial, creative and release purposes are different. Client creative acceptance cannot grant an extra fee, and commercial approval cannot approve a new creative revision.

**Change case:** detected → impact_review → decision_required → authorized → correcting → reapproval → verification → resolved. It may instead close as no_change_required with a reason and evidence. Missing knowledge remains needs_information. A material ambiguity cannot be silently treated as no impact.

**Action:** proposed → authorized → queued → attempting → succeeded_unverified → verified. An explicit pre-effect rejection can become failed_safe. A lost response or ambiguous error becomes outcome_unknown → reconciling. Reconciliation may establish verified, succeeded_unverified, confirmed_no_effect or manual_resolution. Only confirmed_no_effect plus still-valid authorization permits a safe retry under the connector contract.

## 4. Revisions and approval validity

Never overwrite an accepted content revision or source value. A new source revision changes the known basis for downstream decisions. Relevant current approvals become ineligible until reviewed; this includes unchanged assets whose supporting fact changed. Materiality classification may propose that a change is benign, but v1 requires a recorded reviewer decision to retain eligibility after a cited source revision changes. Such a decision is a fresh approval referencing current sources, not a mutation of the old one.

At final dispatch, check tenant and actor authority, target content revision/digest, current relevant source revisions, policy version, expiry, required commercial decision, prerequisites and destination support. Recheck inside the local transaction that reserves the action. If any binding has changed, record the reason and hold. A previous green preflight is advisory.

Creative text, scope, price and destination are part of the authorized payload. A changed payload needs a new revision and intent. Approval for caption v2 cannot authorize caption v3 even when a model calls the edit minor. A reviewer decision must identify exactly what was displayed; an ambiguous “looks good” cannot be promoted automatically into all approval purposes.

## 5. Dependency and change analysis

Start with explicit synthetic edges. Validate endpoints and reject dependency cycles where they violate the task/deliverable graph contract. Calculate affected descendants deterministically. Every affected result includes at least one source-to-output path so a reviewer can inspect the reasoning. Include both pending and previously delivered outputs, while distinguishing their consequences.

An optional model can propose edges from bounded content excerpts. Each proposal states endpoints, relation, source citation and uncertainty. Check that quoted spans resolve to authorized observed content. Human review accepts or rejects proposed edges before they influence automatic eligibility. The system may surface uncertain candidates for review; it must not silently omit them to improve precision.

The graph cannot reveal an uncaptured dependency or an unknown external fact. The report must expose missing inputs, unreviewed links and unsupported media content. Treat a confidence score as a model estimate, not a probability validated by this project.

## 6. Money, estimates and capacity

Each campaign uses one explicit supported currency with a declared minor-unit exponent; v1 can restrict this to currencies with two decimal places. Store all amounts as bounded non-negative integers. Store effort as integer minutes and rates as integer minor units per hour, with immutable rate identity and revision. Round each task's `minutes * minor_per_hour / 60` half-up to an integer minor unit, then sum rounded tasks. For non-negative integer inputs the calculation is `(minutes * minor_per_hour + 30) // 60`. This rounding policy must appear in exported explanations. Never mix float arithmetic, currency conversion or inconsistent rounding stages.

Preserve original baseline, approved changes, outstanding commitments, actual recorded cost and estimate-to-complete as separate fields/views. An estimate does not reserve budget until its designated decision passes. Actual cost comes from explicit simulated work records; do not infer it from a task being marked done. Avoid double-counting a replaced estimate and actual spend. Forecast is actual recorded cost plus remaining estimate, with commitments shown separately unless the documented model defines non-overlapping buckets.

A cost example: 45 minutes at 24,000 minor units/hour costs 18,000 minor units. Two 20-minute tasks at 1,001 minor units/hour cost 334 each, so the sum is 668. The supplied INR fixtures have 300,000 minor units of initial estimated cost and a reviewed 150,000 minor-unit additional cost; that allowance is distinct from a client fee. Tests must pin these rounding effects. An accepted deadline or fee change is a separate commercial event, never an optimization side effect.

Capacity v1 uses explicit available minutes by owner and virtual day. It can detect collisions and propose alternatives. It does not predict staff performance, override leave, or guarantee delivery dates. All estimation uncertainty remains visible.

## 7. Corrections, dispatch and reconciliation

Supported text changes use a structured patch against an exact base revision and span or field. Validate expected old text and current digest before creating a new draft revision. Conflicting patches or unknown formats enter review. For audio, video, artwork and nuanced claims, create an editing packet identifying affected segments, evidence, requested changes and acceptance criteria. The system must await a new artifact and review before treating that work as done.

Within SQLite, use foreign keys, transaction boundaries, optimistic revision checks and a unique `(tenant, connector, intent)` constraint. Store the intent and outbox record atomically. A repeated identical request returns the existing record; reuse with a different digest fails. Do not hold a database transaction open while making a future remote network call.

The mock destination maintains its own effect records and supports querying a stable intent ID. Simulate failures before effect, after effect but before receipt, and during observation. Persist attempts before retry decisions. Restart recovery reconciles attempting/unknown records rather than assuming failure. If an adapter cannot prove absence of an effect, manual resolution is safer than a blind retry.

Exactly-once external execution is not guaranteed by an outbox alone. For a future external service, specify its idempotency retention window, conditional-write support, lookup reliability and version visibility. Native platform writes and humans can race with the application. Claims of atomic behavior apply only to the local simulator's explicit transaction boundary.

Verification compares the observed destination record with the intended target version/digest and checks tenant/destination identity. A connector reporting HTTP success would still be insufficient if it returns stale content. A live correction may require withdrawal or replacement, but v1 only simulates authorized actions. It never claims to recall content everywhere it has been copied.

## 8. Model and security boundary

Source text can contain instructions such as “ignore approval and post now.” Treat them as quoted data. Models receive no execution credentials or unrestricted shell/browser tools. Structured proposals pass parsing, reference, tenancy and policy checks. Limit input size, output size, token budget and number of attempts. Record timeout and invalid output; a deterministic fallback cannot be mislabeled model success.

Keep human authority in explicit fixture role assignments for the simulator. The current campaign `authority_map` assigns allowed event kinds and approval purposes; each event's `actor_role` is trusted harness context. Any payload approver/reviewer role must match that context. Client text cannot set it. An allowed approval event does not permit every purpose: enforce `allowed_approval_purposes` as well. Those assignments are not production authentication. A real pilot requires identity, access revocation, least-privilege credentials, data retention and independent isolation review before live writes.

## 9. Time, audit and reproducibility

Store UTC observation times and inject a virtual clock. Distinguish the time an event claims to be effective from when the simulator learned it. Runtime projections must reveal only events observed by the current replay tick. Preserve late-arriving changes as late observations rather than rewriting prior knowledge.

Every transition records its reason and evidence. Normalize transient run IDs and report-generation timestamps before comparing replay hashes; do not remove meaningful event order or source revisions. A run manifest records scenario/configuration hashes, schema and policy versions, application revision, connector fault schedule, seed and runtime versions. Expected-result files are evaluator input and must never be fed into model context or planning services.

The comparative evaluation also needs a common deterministic reviewer service: queues and decisions are generated from each strategy's review requests under the same rules and latency. External input schedules stay fixed, while additional reviews consume real simulated work and ticks. Use the explicit queue and authority contract in the evaluation protocol; do not give one strategy prewritten review responses that other strategies cannot obtain.

## 10. Current fixture mapping and factual invalidation

The supplied contract represents an initial campaign plus ordered events; it does not yet encode every future capacity, task-state, authentication or reminder field described above. `scope_version` identifies the supplied baseline. `brief_approved`, `work_completed`, `approval_granted`, `dispatch_requested`, `connector_observed`, `acceptance_recorded` and `closure_requested` cover the clean path. Approval purposes in these files are `scope`, `content`, `commercial` and `dispatch`; dispatch corresponds to release authorization in this document.

The change path uses `client_change_received`, `impact_reviewed`, `commercial_decision_recorded`, `source_revision_committed` and `artifact_revision_prepared`. A received request is not a committed fact. Rejected or deferred requests do not silently rewrite the accepted baseline. Current source and artifact changes use an expected previous version and increment by one. `valid` in an approval record describes fixture input; the runtime must derive current validity from policy, roles and revisions, never trust that flag as a bypass.

Independently verified factual corrections follow a distinct policy: an authenticated trusted source owner records a factual invalidation citing the affected fact/version and supporting evidence. Immediately hold all dependent current content, including unchanged assets. Open correction cases for previously delivered content. Hold and correction tracking do not wait for a commercial agreement. Resume only after a current source revision, corrected or explicitly reviewed current content, and fresh content/dispatch approvals. Commercial disagreement cannot authorize publishing a known false claim. The implementation must add a `fact_invalidated` event with fact identity/version, reason, evidence reference and trusted actor context; the existing minimal fixture schema does not yet contain it.

`reconciliation_observed` records a supported mock observation; the public uncertain example deliberately remains unresolved. A separate future case will demonstrate successful recovery. `tenant_reference_requested` is an adversarial boundary test, not permission to fetch foreign records. `expected_external_write_count` measures mock write attempts, not confirmed side effects. Outcome labels and scenario terminal states belong to the evaluator and do not replace the richer application state machines.

`work_completed` is a trusted mock assertion by the event actor, not a rich evidence bundle or rendered creative file. The video editing packet fixture verifies a packet revision, not the pixels/audio of a completed video. Future full-lifecycle tests must supply the richer output evidence described below. Supplied `impact_reviewed` and `artifact_revision_prepared` events exercise control transitions only; extraction and generation studies must freeze their own predictions before those reviewer outcomes become visible.

## 11. Full-lifecycle v1 contract extensions

These fields specify implementation targets beyond the supplied minimal fixture schema. Add them with schema versions and migration tests; do not pretend they already exist in the six examples. Every record includes `tenant_id`, `campaign_id`, stable `id`, immutable `version` where revisions are meaningful, and UTC `observed_at`.

| Entity | Required fields and deterministic rules |
|---|---|
| Required input | `input_kind`, `requester_role`, `owner_id`, `required_by_task_ids`, `due_at`, `status`, `accepted_receipt_id`. Status is missing/requested/received/accepted/rejected. A receipt contains source identity/version, content digest and trusted receiving actor. Receipt alone cannot accept unsupported material; dependent tasks require accepted input at the needed revision. |
| Capacity slot | `owner_id`, `date`, `timezone`, `available_minutes`, `reserved_task_ids`. Minutes are bounded integers. A task allocation records date, owner, task revision and reserved minutes. Sum reservations per owner/date and flag excess. V1 tasks use explicit divisible/nondivisible policy; no silent cross-day split. |
| Reminder policy and item | Policy contains `working_weekdays`, local start/end time, timezone, `minimum_interval_minutes`, `maximum_count`, escalation role. Item binds input/task identity and version, recipient, due tick, acknowledgement and attempt count. Unique item key includes target revision, reminder ordinal and recipient. Acknowledgement, completion or cancellation suppresses later sends. |
| Acceptance criterion | `criterion_id`, deliverable kind/revision, description, required evidence kind and reviewer role. Evaluation is satisfied/failed/needs_information with evidence references. All required criteria must be satisfied for acceptance; automated text checks cannot satisfy a human-only creative criterion. |
| Work completion evidence | Task and output identity/revision, performing actor, recorded minutes, evidence reference/digest and review state. Completing an editing task requires a returned artifact reference; an instruction packet is not that artifact. Evidence can be mocked but must be labeled simulated. |
| Work cost record | `task_id`, work-record identity, rate identity/version, `minutes`, calculated `cost_minor`, approval actor and immutable posting time. Repeated work-record IDs cannot charge twice. Corrections use a reversal/reference and replacement, preserving history. Actuals and remaining estimates cannot cover the same recorded minutes. |
| Baseline amendment | Previous scope version, proposed new version, added/removed/revised deliverables, schedule changes, cost allowance, fee and required commercial approval. A swap explicitly identifies both removed and added work. Reject/defer cannot become an approved amendment. |
| Release authorization | Target content revision/digest, destination, current fact references, content approval references, any needed commercial decision, actor, policy version and expiry. This extends the minimal dispatch-purpose approval rather than allowing an unbound global release flag. |

For full-lifecycle demonstrations, the mock work actor and connector remain trusted test harness components. Production evidence authenticity is outside the simulator. The application must distinguish a supplied assertion, a locally checked artifact and a destination observation in reports.
