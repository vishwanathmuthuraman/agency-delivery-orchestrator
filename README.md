# Agency Delivery Orchestrator

**Status: documentation blueprint and original synthetic examples. The application is not implemented.** No completed benchmark, customer deployment, autonomous production capability or time saving is claimed. Expected-result files describe intended behavior, not measured output.

A planned local simulator for coordinating an agency campaign from an approved brief to verified delivery. It models the work around creative production: collecting inputs, planning tasks and capacity, arranging handoffs, gathering feedback, handling changes, checking approvals and preparing a billing evidence packet.

The most detailed demonstration asks: **when a client changes a fact, requirement or deadline, can we identify the affected work, make its consequences clear, obtain the right decisions, and verify that the correction was completed?** That demonstration is one part of the full delivery lifecycle.

## A concrete example

A fictional client approves a campaign containing a script, a video editing task, a caption and a scheduled social post. The client then changes an approved product claim. The proposed system identifies dependent outputs, pauses affected dispatches, estimates additional work using versioned rates, and presents a commercial choice. After an authorized decision, it drafts a supported caption correction, prepares a work packet for the human editor, requests approval of the new versions, and verifies the mock destination contains the approved version. Unrelated work continues.

The system must never turn “I sent a request” into “the work is finished.” A timeout means the result is unknown until the destination is reconciled. Changing a caption does not mean the spoken words inside a video have been changed.

## The whole product scope

| Delivery stage | Planned v1 behavior |
|---|---|
| Brief and scope | Validate a structured synthetic brief, deliverables, acceptance criteria and missing inputs. |
| Plan and budget | Propose a task graph; calculate cost and capacity from explicit inputs; preserve an approved baseline. |
| Collect and coordinate | Track input requests, task owners, blockers, handoffs and mock reminders. |
| Produce and review | Route versioned work; prepare text drafts and human editing packets; collect role-specific decisions. |
| Manage changes | Trace affected content, compare options and require approval of commercial consequences. |
| Complete delivery | Recheck readiness, use a mock connector, reconcile uncertain results and verify observed versions. |
| Close the campaign | Produce acceptance and delivery evidence plus a draft billing-readiness export. |

This is a bounded agency workflow prototype. It is not a general ledger, tax engine, payroll system, purchasing suite, real publishing integration or a guarantee that every creative task can be automated. Future connections to those systems require separate scope and authorization.

## Start here

1. Read [product requirements](docs/01-product-requirements.md) for users, scenarios and acceptance criteria.
2. Read [architecture](docs/02-architecture.md) before implementing revisions, approvals, money or dispatch.
3. Follow [the build plan](docs/03-build-plan.md) and maintain [the task tracker](planning/tasks.csv).
4. Freeze [the evaluation protocol](docs/04-evaluation.md) before using held-out cases.
5. Use [definition of done](docs/05-definition-of-done.md) to distinguish a finished blueprint, working v1, evaluated result and release-ready artifact.
6. Review [sources and rationale](docs/06-sources-and-design-rationale.md), [delivery risks](docs/07-delivery-and-risk.md) and [publication](docs/08-publication.md).

[BLUEPRINT.html](BLUEPRINT.html) is the offline reading edition. The Markdown documents are the editable specification. The JSON files under `schemas/` define machine-readable contracts. The examples under `examples/` are synthetic teaching cases; they do not constitute the proposed evaluation corpus.

The current blueprint tooling can run in a local environment:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-blueprint.txt
.venv/bin/python scripts/validate_blueprint.py
.venv/bin/python scripts/render_blueprint.py
```

These commands validate and render documentation only. They do not execute the proposed application. The supplied control fixtures include reviewed impact and prepared text; successful future replay would not by itself prove semantic discovery or model-generated correction.

## Intended implementation

Python 3.12, SQLite, a deterministic command-line runner and a local HTML report. Default execution must work without credentials, network access or a model provider. An optional model adapter can propose dependency links, classifications and text revisions. Deterministic rules and explicit reviewer decisions remain responsible for authorization, money and state changes. An optional UI follows the working core.

The build plan contains **future interface contracts**, not a runnable installation guide. No product CLI or application package is claimed to exist today. Any documentation/schema validation scripts supplied with the blueprint validate only the specification artifacts.

## Evidence and originality

Consulting reports motivate investigating disconnected content operations. Existing agency management, proofing, asset management and professional-services products already cover substantial parts of this scope. This project tests a specific implementation and evaluation design; it does not claim to invent agency management, lack competitors, demonstrate demand or establish research novelty. [The source register](docs/06-sources-and-design-rationale.md) explains those overlaps.

All examples are original synthetic records. No private client records, affiliations, contacts, contracts or credentials belong in this repository. This repository is prepared for authorized public GitHub sharing as a documentation blueprint; public availability is not an application release or deployment. License selection is pending, and no code, documentation or synthetic-data license grant is supplied. Choose and record terms before an openly licensed reusable release.
