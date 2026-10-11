# 03 — Public milestones

The repository currently contains a specification, six synthetic scenarios and documentation-checking utilities. The application and comparative evaluation are not implemented.

| Milestone | Intended result | Evidence required |
|---|---|---|
| M1 — Contracts and isolation | Validate campaign/event inputs, enforce tenant boundaries and preserve reproducible history. | Contract, import, isolation and restart tests. |
| M2 — Campaign coordination | Represent approved scope, missing inputs, task readiness, capacity and bounded reminders. | Full-lifecycle integration traces and deterministic cost/capacity checks. |
| M3 — Changes and decisions | Explain affected work, prepare supported corrections and require version-bound commercial/content decisions. | Dependency, revision, authority and stale-approval tests. |
| M4 — Verified completion | Reserve action intents, reconcile uncertain mock outcomes and distinguish observed delivery from acceptance and billing readiness. | Race/retry tests, destination evidence, closure and draft-export tests. |
| M5 — Comparative study | Compare the documented strategies on reviewed, separated scenario lineages. | Frozen protocol, complete run inventory, measured results and limitations. |
| M6 — Reproducible release | Another environment reproduces the offline workflow and public conclusions. | Clean-install/demo record and publication review. |

Read the [requirements](01-product-requirements.md), [architecture](02-architecture.md), [evaluation protocol](04-evaluation.md) and [definition of done](05-definition-of-done.md). Optional model extraction and interface work must be evaluated separately; replaying supplied reviewed changes does not establish autonomous understanding or creative production.

Documentation-checking utilities validate supplied artifacts only. They do not run a campaign, contact a client, publish content or measure business performance. Application usage commands must remain absent from a runnable quick start until tested implementation exists.

Milestone evidence should identify the software revision, scenario version, test output and remaining limitations. The full-lifecycle demonstration must exercise missing inputs, capacity, handoffs and closure in addition to the client-change scenario.
