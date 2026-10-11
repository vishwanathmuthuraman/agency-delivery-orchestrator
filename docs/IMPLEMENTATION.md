# Initial implementation — 0.1.0

This is the first implemented offline slice. “Complete” below means the bounded component passed the recorded checks; it does not mean the proposed product or evaluation is complete.

## Completed component tasks

| Task | Work | Status | Delivered behavior |
|---|---|---|---|
| C01 | Validate campaign contracts and task dependencies | Complete for this slice | Tenant/campaign and role checks, stable topological order, cycle rejection, source references and recomputed minute/rate costs. |
| C02 | Inspect readiness and current approvals | Complete for this slice | Prerequisite-aware initial readiness, exact budget totals and approvals bound to content revision, source versions, purpose and authorized role. |
| C03 | Package, test and document the slice | Complete for this slice | Independent Python package, packaged existing schema resources, locked dependencies, CLI error behavior, behavioral tests, CI and captured demo evidence. |

Source: [core](../src/agency_delivery_orchestrator/core.py), [contracts/utilities](../src/agency_delivery_orchestrator/common.py), [CLI](../src/agency_delivery_orchestrator/cli.py), [behavioral tests](../tests/test_core.py), [CLI tests](../tests/test_cli.py). Runtime selection is recorded in [ADR 0001](decisions/0001-offline-core.md).

## What actually ran

Verified on Python **3.12.13**, Darwin: **24 tests passed, zero failed**, Ruff lint/format checks passed. A wheel was built, installed with locked dependency hashes into a fresh environment and exercised from outside the checkout; its schema files loaded from the installed package. The CLI input/output hashes and implementation-file hashes are in the [verification record](../reports/initial-implementation/verification.json). That file identifies exact tested inputs; expected specifications were not copied into an execution report.

```sh
uv sync --locked
uv run --locked agency inspect examples/duplicate-dispatch.scenario.json
uv run --locked ruff check src tests
uv run --locked ruff format --check src tests
uv run --locked pytest
```

Observed demo: The inspector reports the initial campaign cost, prerequisite readiness and content/dispatch approval bindings. Changing a referenced fact invalidates its binding while unrelated content retains its approval. Events are not replayed and external writes remain zero.

[Captured output](../reports/initial-implementation/demo-1.json). Test use of authored expected files is restricted to development assertions; application code does not open them. These are component regressions, not independent held-out evaluation or performance measurements.

## Relationship to the full plan

M1–M3 have limited initial-state component evidence. There is no event replay, operational coordination loop or completed milestone. M4 and M5 remain pending.

The [build plan](03-build-plan.md), [requirements](01-product-requirements.md), [evaluation](04-evaluation.md) and [definition of done](05-definition-of-done.md) remain the release criteria. Planned acceptance registers describe the wider system; partial progress does not replace their full conditions. Documentation checks validate authored artifacts separately from application CI.

## Explicit limits

This is an initial-state inspector. It does not process client changes, assign capacity, chase people, send reminders, reserve outbox actions, dispatch content, reconcile receipts or complete campaigns. The six lifecycle examples validate as inputs; their full expected outcomes have not been executed.

All example records and observations are synthetic. No network integration or external business action exists in this slice. Financial and property results support human review. No customer impact, trained-model quality, production readiness or independent endorsement is established.

## Next implementation steps

1. Create persisted campaign/event history and an event reducer; replay missing-input, client-change and capacity cases with exact cost deltas.
2. Implement version-bound commercial/content decisions, role checks and immutable handoff history.
3. Add durable action reservations and mock outcome reconciliation; test duplicate dispatch, uncertain delivery and acceptance/billing separation before any live connector.

For each step, add meaningful failure-case tests, capture actual output, preserve evidence/time/money boundaries, and update this record with the revision and unresolved limitations. Do not mark the full release complete from component test counts.
