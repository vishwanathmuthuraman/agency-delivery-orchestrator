# 01 — Product requirements

**Specification version 0.1. All application requirements below are proposed and unachieved.** The repository is a build blueprint. The user-facing promise of the eventual demonstration is: “Show what needs doing, why it matters, who must decide, and whether the accepted work actually reached the intended destination.”

## 1. Users and the job

The primary user is an agency delivery or account lead coordinating creative production. Other simulated roles are a producer, editor, client reviewer, commercial approver and release approver. A person may hold several roles, but a fixture must state each permission explicitly. The model is not a person with inherited authority.

The unit of work is a campaign containing deliverables, tasks, source facts, approvals and a commercial baseline. A deliverable might be a script, caption, editing package or simulated social post. A task is an action needed to produce or review it. A source fact is a versioned statement such as an approved product claim, launch date or required disclaimer. Keep these distinct: completing a task does not automatically accept a deliverable.

The public prototype must use fictional parties and records. A future discovery exercise can test the hypothesis with authorized examples, but an interview, customer, saving or deployment must never be implied by a synthetic scenario.

## 2. Full lifecycle and release boundaries

| Stage | Offline v1 | Later, separately scoped work |
|---|---|---|
| Intake | Structured brief, missing-input checks, draft deliverable list | Authorized document/email ingestion and extraction |
| Baseline | Explicit task dependencies, estimates, rate version and budget approval | Historical estimates and real resource calendars |
| Inputs | Simulated requests, owners, due times and receipts | Authorized client portal or communication tools |
| Coordination | Deterministic readiness, reminder proposals and escalation queue | Selected real outbound channels with approved policies |
| Creative production | Supported text patches and human editing packets | Specific creative-tool adapters after feasibility testing |
| Review | Version-bound creative, commercial and release decisions | Authenticated external reviewer identity |
| Changes | Source/deliverable impact, cost options and reapproval | Calibrated extraction across approved real artifacts |
| Delivery | Mock connector, readiness checks and destination verification | One authorized destination at a time |
| Closure | Evidence packet and billing-readiness draft | Integration with existing invoicing/accounting systems |

All v1 paths operate in local simulated time. No actual messages or posts leave the machine. There is no requirement to generate a finished video, change audio, infer legal approval, or operate every business department. The full lifecycle supplies context; selective change handling and verified closure receive the deepest implementation and evaluation.

## 3. Numbered functional requirements

Each acceptance criterion is a future behavior to verify, not a completed test.

| ID | Requirement | Acceptance criterion |
|---|---|---|
| FR-01 | Validate scenario and campaign contracts | Reject invalid types, unresolved references, duplicate conflicting IDs, unsupported currency and invalid version progression before partial state is committed. |
| FR-02 | Isolate clients | Every read, mutation, model context and export is scoped to a tenant. A foreign reference produces a denial with no foreign content in errors or reports. |
| FR-03 | Preserve the approved scope | Store an immutable baseline of deliverables, acceptance criteria, schedule assumptions, rate versions and budget. Later changes create explicit revisions. |
| FR-04 | Identify missing inputs | Required but absent client material blocks only dependent tasks. An input receipt identifies its exact version and releases only eligible work. |
| FR-05 | Plan work and capacity | Validate an acyclic task graph, owners and estimates. Detect overallocated simulated capacity without silently moving a contractual deadline. |
| FR-06 | Calculate money deterministically | Use one currency per campaign, integer minor units, integer minutes and a documented rounding policy. Estimated, approved, committed and actual amounts remain separate. |
| FR-07 | Coordinate work transparently | Produce owner-specific next actions and simulated reminder/escalation events. Respect configured working windows, maximum reminder count and acknowledgement status. |
| FR-08 | Preserve content lineage | Store immutable deliverable revisions and explicit dependency links to source and upstream content revisions. A proposed link records evidence and review status. |
| FR-09 | Distinguish proposals from facts | Model-proposed dependencies, classifications, estimates and patches remain proposals until schema checks and applicable review pass. Unsupported claims cause abstention or rejection. |
| FR-10 | Detect meaningful changes | Ingest a new source or deliverable revision, identify affected current work, show supporting paths and leave unrelated work eligible. Missing or ambiguous evidence enters review. |
| FR-11 | Offer commercial choices | Present absorb, additional-fee, substitution or deadline-change options with explicit costs and assumptions. None becomes an agreed commercial commitment without an authorized decision. |
| FR-12 | Prepare bounded corrective work | Apply supported text replacements only to their stated base revision; produce human editing packets for unsupported media changes. Both remain drafts. |
| FR-13 | Bind and invalidate approvals | Bind each decision to purpose, actor, target revision, relevant source revisions and policy version. A relevant change prevents old approval from authorizing dispatch. |
| FR-14 | Enforce scheduling readiness | Require completed prerequisites, accepted current content, current commercial decision when needed, valid release authorization and a supported destination. Readiness is checked again at dispatch. |
| FR-15 | Dispatch idempotently within the supported boundary | A repeated intent/payload has at most one mock external effect. Reuse with changed payload is a conflict. New content revisions require new intent and authorization. |
| FR-16 | Reconcile unknown outcomes | After a response is lost, preserve an unknown state, query the mock destination by stable intent, and never blindly retry an action that might have completed. |
| FR-17 | Verify delivery and closure | Compare observed destination identity/version or content digest with the approved target. A request receipt alone cannot establish verified completion. |
| FR-18 | Export billing readiness | Produce a local draft packet containing accepted scope, authorized changes and verified delivery references. It must not create an invoice or imply payment. |
| FR-19 | Make runs reproducible and inspectable | Replaying the same fixture/configuration yields the same normalized state and decisions. The report exposes evidence, uncertainty and failure reasons. |
| FR-20 | Evaluate without hidden-label leakage | Strategies see the same observed facts and shared guard; future events and expected labels stay evaluator-only. Report failures, denominators and limitations. |

## 4. Quality and safety requirements

NFR-01: the default simulator runs without network access or a provider key. NFR-02: state changes are durable across restart, with atomic local transactions and a migration version. NFR-03: narrative input, imported files and retrieved text are untrusted data, never tool instructions. NFR-04: logs avoid secrets and unnecessary client content; report rendering escapes untrusted strings. NFR-05: clock, role policy, reminder limits and connector behavior are injectable for tests. NFR-06: missing authority, ambiguous destination state and unsupported transformations produce explicit non-success states.

The application may transparently coordinate routine work under a configured policy. It must not impersonate a human, pressure staff, infer private psychological traits or promise a deadline, price or scope concession on behalf of a client or agency.

## 5. Required demonstration stories

These are intended v1 demonstration behaviors. The six supplied fixture files are narrower control specifications; they do not yet exercise all input, capacity, reminder and handoff behavior end to end. Build a separate full-lifecycle integration scenario before claiming the whole lifecycle works. Reviewed impacts and prepared revisions supplied as fixture events are simulated human inputs, not discoveries made by an implemented model.

1. **Clean delivery:** approved scope progresses through input collection, text drafting, human production, review, mock delivery and billing readiness.
2. **Client claim changes:** identify dependent caption and editing work, protect the old approved destination, approve a cost choice, correct and reapprove new revisions, then verify them.
3. **Stale approval:** a source changes between preflight and dispatch. The final guard rejects old authorization even if the queue has not refreshed.
4. **Duplicate dispatch:** repeated delivery and restart do not create a second effect; changed-payload key reuse fails visibly.
5. **Uncertain dispatch:** a write attempt has no confirmed outcome. The public example remains in reconciliation rather than blindly retrying; a separate future recovery test finds an existing effect without creating another.
6. **Cross-client reference:** a malicious brief points at another tenant's content or requests secret context. Retrieval and report generation deny it without disclosure.

These public stories teach the contract. Additional evaluation cases must vary structure and causes, not merely names.

An optional client request and a verified factual invalidation have different effects. A rejected optional request leaves the accepted baseline unchanged. A factual invalidation recorded by an authenticated trusted source owner immediately holds affected content independent of commercial negotiations; correction, current-source review and fresh approvals are required before dispatch resumes. The latter behavior requires an additional event contract during implementation.

## 6. Success, limits and non-goals

A successful v1 demonstrates the supported lifecycle faithfully, including useful work that can continue and work that needs a human. It does not achieve success by blocking everything, approving everything, or relabeling incomplete work as complete. Performance targets and safety gates are separated in [definition of done](05-definition-of-done.md).

Customer value remains a hypothesis: fewer forgotten consequences, clearer commercial choices and more reliable closure. Synthetic replay cannot establish hours saved, willingness to pay, operating margin improvement, industry-wide demand, legal compliance or competitive advantage. The source document deliberately records existing products with overlapping functionality.
