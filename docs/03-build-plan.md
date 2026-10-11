# 03 — Build plan, task by task

**Application implementation has not started.** The [tracker](../planning/tasks.csv) is authoritative for task status and estimates. Every task starts `not_started`. Required tasks total **209–329 focused engineering hours**; optional model and UI work add **18–30 hours**, for **227–359 hours** if all branches are included. These are estimates, not elapsed time or delivery promises. Add 25% contingency and independent review time; optional branches are separate from deterministic completion.

## 1. What can run today

The repository's documentation validator and renderer are tooling for the blueprint, not the proposed application. With their dependencies available, run from the repository root:

```sh
python3 scripts/validate_blueprint.py
python3 scripts/render_blueprint.py
```

The validator requires `jsonschema`; the renderer requires `markdown`. The root `requirements-blueprint.txt` pins these documentation dependencies. Follow README's isolated-environment setup if needed. These commands check or render contracts, links and documents. They do not execute the campaign workflow, demonstrate expected outcomes, measure application performance or complete an implementation task.

All `uv run ado ...`, test paths and application modules below are **FUTURE interface contracts**. Implement them before treating them as runnable instructions.

## 2. First working increment: deterministic state

### T01 — Freeze the supported workflow

Read requirements, architecture, examples and expected files. Trace clean delivery and a claim change by hand. Translate the architecture's optional-request and verified-factual-invalidation policies into concrete transition tables, preserving the immediate hold independent of a commercial decision. Define the simulated role matrix and what each acceptance criterion means. Record decisions in future `docs/decisions.md` without private customer material.

Acceptance: every event kind has a responsible actor, preconditions and an outcome. No known-false content can be dispatched while price negotiations continue. Unresolved product policies are explicitly blockers, not implementation guesses.

### T02 — Create the package and development environment

Create `pyproject.toml`, `.python-version`, `src/agency_delivery_orchestrator/`, a CLI entry point named `ado`, and a minimal test harness. Use Python 3.12, a lockfile, pytest, Ruff and a schema validator. Keep provider dependencies optional. Use the current [official uv installation instructions](https://docs.astral.sh/uv/getting-started/installation/) if uv is absent.

Acceptance: future `uv sync --locked`, `uv run ado --help` and `uv run ruff check .` succeed in a clean environment. Help clearly identifies the local simulator. No network-enabled service starts by default.

### T03 — Implement contracts and semantic validation

Create `domain/models.py` and `replay/validation.py`. Load the existing schemas locally. Add semantic checks for tenant scope, unique IDs, references, graph consistency, currency, UTC times and expected-version progression. Extend contracts for planned capacity/reminder fields deliberately, preserving an explicit version or migration.

Acceptance: future `uv run ado validate examples/clean-delivery.scenario.json` passes. Invalid inputs fail with safe field paths and zero partial mutation. Expected-result files are rejected as runtime scenarios.

### T04 — Create durable event and state storage

Create a versioned SQL schema, migrations and a repository abstraction. Enable foreign keys on every SQLite connection. Append immutable events; materialize current state in a transaction. Same event ID and content is a duplicate; same ID with different content is an integrity error. Inject the clock.

Acceptance: fixture loading is atomic, restart preserves state, failed migrations roll back, and out-of-order observation cannot reveal future content. Tests inspect persisted records, not only returned messages.

### T05 — Enforce tenant isolation

Implement tenant-qualified repository methods and reference validation. Carry tenant/campaign context through caches, evidence retrieval, error formatting, exports and eventual model input. Never allow a caller-supplied reference to change the active tenant.

Acceptance: adversarial references, duplicate IDs in different tenants, cache collisions and report links cannot disclose or mutate another tenant. Tests use distinguishable canary strings and verify they never appear in the unauthorized output.

### T06 — Implement source and content revisions

Create append-only source and deliverable histories with expected-version checks. Define current and observed-at-time queries. Preserve prior content when a new draft is prepared; reviewed content is immutable. Record revision authorship and evidence.

Acceptance: conflicting edits fail, version increments are checked, earlier observations reproduce earlier knowledge, and a pending request does not change an accepted fact. A verified correction follows the separately frozen hold policy.

### T07 — Implement actor roles and decisions

Implement the campaign's `authority_map`, allowed event kinds and allowed approval purposes. Treat event `actor_role` as trusted harness context and require any payload approver/reviewer role to match it. Distinguish content, scope, commercial and dispatch authority. Store decisions append-only with reason and precise subject version. Reject model-generated claims of authority.

Acceptance: a content reviewer cannot authorize price or dispatch unless explicitly assigned that role. Revoked or missing authority blocks consequential work. Documentation states that fixture roles are not production authentication.

### T08 — Implement money and rates

Write pure integer arithmetic for task estimates, versioned rates, cost allowances and fees. Apply the architecture's half-up rounding once per task. Keep forecast, actual and outstanding commitments separate. Bound values and reject currency mixing.

Acceptance: the public initial task cost equals 300,000 INR minor units; the reviewed extra cost equals 150,000. Boundary, zero, large-value and rounding tests pass. Fee approval does not overwrite cost, and task completion does not manufacture actual spend.

## 3. Second increment: the everyday delivery lifecycle

### T09 — Preserve the commercial baseline

Implement baseline creation and approval using explicit scope, deliverables, acceptance criteria and rate references. Show a comparison when a new baseline is proposed. A rejected proposal leaves the accepted baseline unchanged.

Acceptance: exports can reconstruct both the original agreement and approved changes; no silent deadline, fee or scope change is possible.

### T10 — Track required inputs

Implement required-input records, owners, virtual due times, requests and receipts. Associate each input with dependent tasks. Link received material to its version and source rather than merely setting a boolean.

Acceptance: one missing client input blocks the relevant task while unrelated ready tasks continue. A duplicate receipt is harmless; a revised receipt triggers the appropriate dependency check.

### T11 — Build the task dependency engine

Implement task creation, graph validation, deterministic topological ordering and readiness checks. Completion requires an output reference and authorized simulated work event. Distinguish failed, cancelled, awaiting review and completed.

Acceptance: cycles fail visibly, cancelled prerequisites follow a documented policy, and marking an upstream task complete cannot bypass required review of its output.

### T12 — Add bounded capacity planning

Represent available minutes by owner and virtual day. Calculate conflicts using explicit task estimates; propose assignment or schedule alternatives without committing them. Document whether tasks are divisible.

Acceptance: a deliberate overload is detected and explained. Accepted deadline changes require the relevant decision. No model-generated hours silently become an approved capacity allocation.

### T13 — Add routine reminders and escalation

Implement a simulated notification queue with acknowledgement, working windows, deduplication and a configured limit. Draft neutral reminders referencing specific missing work. Escalation creates a review item for a named role.

Acceptance: repeated ticks do not spam duplicate reminders; acknowledged or completed requests stop further reminders; escalation does not automatically punish or reassign a person. There is no real outbound messaging adapter.

## 4. Third increment: changes and corrective work

### T14 — Build the reviewed dependency graph

Implement typed source-to-content and content-to-content edges with evidence references and review status. Compute reachable descendants and reproducible explanation paths. Keep unreviewed candidates separate from accepted edges.

Acceptance: a product-claim change reaches caption and narration-dependent editing work; unrelated assets remain outside the affected set. Broken citations and cross-tenant endpoints are rejected.

### T15 — Implement change cases and impact review

Separate incoming requests, confirmed source revisions and consequences for pending versus delivered work. Open or deduplicate a case by trigger identity. Show affected revisions, unknowns and work options. Preserve a no-impact decision only with a reason.

Acceptance: repeated events do not create duplicate cases; a known source change is not ignored because asset bytes stayed the same. Missing dependency evidence produces review rather than an unsupported no-impact claim.

### T16 — Implement commercial options

Calculate proposed absorb, charge, swap and defer options from explicit work estimates. Record rejection as well. Keep proposed extra cost, approved cost allowance and agreed client fee distinct. Show original and proposed scope together.

Acceptance: only an authorized decision allows a commercial baseline amendment. A fee is never inferred from an internal cost estimate. A rejected change cannot commit the source revision in the ordinary optional-request path.

### T17 — Implement supported text corrections

Create a patch format tied to an exact base revision and expected original text. Apply permitted transformations into a new draft, show a diff and cite the new source. Refuse ambiguous matches or stale bases.

Acceptance: caption correction creates a new unapproved revision; old approval cannot dispatch it. Prompt instructions embedded in content cannot grant tools, authority or additional edits.

### T18 — Generate human editing packets

For unsupported video/audio/graphics transformations, assemble affected segments, original and new source facts, requested work, acceptance criteria and owner. Track returned artifact evidence separately.

Acceptance: an editing packet is labeled instructions; no render is claimed. A simulated human completion event must supply the expected output/version before review can progress.

### T19 — Implement approval binding and invalidation

Bind decisions to target and fact revisions, policy and purpose. Derive current validity rather than trusting an imported `valid` flag. Invalidate affected eligibility after known changes; require fresh decisions for new revisions.

Acceptance: changed source, content, actor authority, destination, expiry and policy each have meaningful tests. Benign-change review creates current authorization rather than altering history.

## 5. Fourth increment: dispatch through verified closure

### T20 — Implement the common final readiness guard

Use one deterministic guard for all evaluation strategies. Check scope, prerequisites, current versions, required decisions, tenant and destination. Run it again when reserving dispatch, regardless of earlier preflight.

Acceptance: a source change between preflight and reservation blocks the stale attempt. Use controlled test barriers, not arbitrary sleeps, to demonstrate the race.

### T21 — Implement intents, outbox and idempotency

Persist immutable intent/payload binding and an outbox record atomically. Duplicate identical requests reuse the record. Conflicting payload reuse fails. Record attempts before connector calls and preserve restart recovery information.

Acceptance: repeated events and concurrent workers cannot enqueue duplicate effects inside the supported local boundary. Database failures do not leave a claimed-success record with no corresponding state.

### T22 — Build the fault-injectable mock connector

Implement only mock destinations. Support effect records, stable intent lookup, before-effect failure, response loss after effect and stale observations. Count write attempts separately from actual side effects and read requests.

Acceptance: each fault is independently observable and reproducible. Connector observations cannot be forged by client narrative or bypass the authorized action record.

### T23 — Implement reconciliation and recovery

Move ambiguous results to unknown. Query stable intent state, reconcile known effects and escalate unresolved ambiguity. Retry only after confirmed no effect and current authorization. Persist every observation.

Acceptance: the public uncertain case stays unresolved with one attempted write. Separate tests cover recovered success, confirmed absence, expired authority and lookup failure without blind retries.

### T24 — Verify observed destination content

Compare destination identity and observed content version/digest against the authorized intent. Keep accepted request, observed success and verified delivery separate. Recheck unexpected later changes by opening a correction case.

Acceptance: wrong-version success is not verified, receipt-only success is not closure, and the expected revision can be traced to its decision and source facts.

### T25 — Assemble closure and billing readiness

Require accepted current deliverables, resolved in-scope work and verified supported delivery. Export the scope/change/acceptance/delivery evidence as a local draft packet. Unknown results prevent a complete status.

Acceptance: the clean scenario produces billing-ready true only after explicit acceptance; unresolved scenarios remain false. No invoice, payment, tax entry or external accounting write is created.

### T26 — Implement replay and the offline demo

Create event replay with virtual time, fixed seed and separate runtime/evaluator projections. Record a run manifest and actual observations. Implement future `ado validate`, `ado replay` and `ado demo` interfaces.

Acceptance: two runs reproduce normalized state and outcomes; expected labels never enter runtime context. The six public scenarios are compared with specifications only after execution.

### T27 — Build a readable local report

Show the campaign baseline, task queue, changed facts, affected paths, commercial choices, revision diffs, approvals, connector attempts and closure evidence. Escape all source text. Link to local evidence safely.

Acceptance: a reviewer can explain why an action was allowed, held or unknown without reading raw database tables. The report clearly labels synthetic records, mock destinations and unsupported transformations.

## 6. Fifth increment: evaluation and release evidence

### T28 — Implement three comparison strategies

Implement dispatch-only recheck, invalidate-all and selective dependency invalidation under the same final guard, data and commercial policy. Strategy choice changes when/how much work is reviewed, not authority. Implement the evaluation protocol's common deterministic reviewer queues, generating responses from each strategy's requests under identical rules and latency while preserving the same external input schedule.

Acceptance: the protocol's paired input rules pass tests; each strategy can complete useful work. Extra invalidations receive eligible review responses and add measured review work/time; they are neither silently excluded nor stranded by missing response events. Hidden labels cannot influence reviewer decisions.

### T29 — Author development cases

Create 36 additional development scenarios across the six evaluation families, separate from the public starter examples. Vary dependency structure, revisions and failure schedules. Include valid clean controls and legitimate unresolved endings.

Acceptance: every case has a manually reviewable intended outcome and a lineage group. A renamed copy is not treated as a new independent template.

### T30 — Build the evaluator and metric tests

Keep oracle truth outside runtime inputs. Implement affected-set, invalidation, unsafe-action, closure, coverage and work counters with explicit denominators. Hand-calculate small examples before coding assertions.

Acceptance: a block-everything strategy fails useful-completion targets. Timeouts and unknowns cannot improve success rates by disappearing from denominators.

### T31 — Complete adversarial and restart tests

Exercise prompt injection, tenant canaries, corrupted references, unauthorized decisions, changed idempotency payloads, concurrent revision changes, partial commits, response loss and restarts. Verify each injected fault was actually triggered.

Acceptance: zero known critical authorization/isolation/false-completion failures remain. Preserve discovered failures as regression cases without calling them held-out evidence.

### T32 — Optional semantic model adapter

Add one provider-neutral adapter only after deterministic behavior works. Freeze schema, prompt, context projection, model version, caching and bounded retries on development data. Obtain a separately agreed paid-call budget before any paid experiment.

Acceptance: invalid output is recorded and rejected, citations resolve, no execution tool is exposed, and fallback is labeled. This task may be deferred without misrepresenting a deterministic v1 as model-evaluated.

### T33 — Freeze protocol and seal held-out cases

Finalize metrics, thresholds, budgets and strategy settings. Create 36 held-out cases using disjoint lineage groups, with another reviewer holding labels where possible. Freeze manifests and hashes before access.

Acceptance: no template group crosses partitions; the protocol identifies reviewer limitations and all scheduled runs. The optional model branch has its own frozen subset/configuration or an explicit deferral.

### T34 — Execute the frozen study

Run 36 held-out scenarios across three strategies: 108 deterministic replays. Record first attempts, errors and permitted infrastructure retries. Do not change rules or cases after inspecting results to improve the score.

Acceptance: every assigned run has a recorded outcome. An honest failing study is a result; missing runs are incomplete work.

### T35 — Analyze results and limitations

Generate paired comparisons, per-family tables, denominators and a failure inventory. Report software/runtime versions, clustered uncertainty only where supported, and the lack of real-customer ROI evidence.

Acceptance: conclusions match data, no vendor performance is inferred from these synthetic baselines, and failed targets remain visible. Publish unfavorable results if reproducible.

### T36 — Verify a clean installation and full demonstration

On a clean environment, resolve the lockfile and run the documented offline quick start without hidden global packages or credentials. Record commands and outputs. Walk through the required demonstration.

Acceptance: another person can reproduce the demo and identify unsupported behavior. No proposed command is presented as verified until executed successfully.

### T37 — Complete release review

Follow the publication checklist, choose licenses, inspect tracked files and history, check source attributions and review actual claims. Record completion evidence in a future release checklist. Remote publication is a separate explicitly authorized action.

Acceptance: the artifact can be reviewed safely for publication, with status and limits prominently visible. Public readiness is not customer readiness.

### T38 — Optional local interface

Only after the core demo works, add a small local dashboard for the same evidence and review services. Prioritize a keyboard-usable queue, version comparison and approval details. Do not add a second business-rule implementation.

Acceptance: the CLI and UI produce the same decisions; narrow-screen and keyboard walkthroughs pass. UI work cannot substitute for missing evaluation or connector guarantees.

## 7. Future command contract

These examples become a quick start only after implementation and clean-install verification:

```sh
uv sync --locked
uv run ado validate examples/clean-delivery.scenario.json
uv run ado demo --offline --output reports/runs/demo
uv run ado replay --scenario examples/client-claim-change.scenario.json --strategy selective --output reports/runs/change
uv run ado evaluate --partition dev --output reports/runs/dev
uv run pytest
uv run ruff check .
```

Outputs must separate observations from expected labels and identify simulated operations. A nonzero exit code on invalid data or an incomplete run is preferable to an attractive report claiming success without evidence.
