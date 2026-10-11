# Project working instructions

This repository currently contains a specification and synthetic examples. Read README.md and docs/01-product-requirements.md through docs/05-definition-of-done.md before implementing application behavior. Proposed commands and expected-result files are not evidence that application behavior exists.

## Work sequence

1. Use planning/tasks.csv. Select the earliest task whose dependencies have real completion evidence.
2. Preserve requirement IDs, version semantics and the evaluation protocol. Record a deliberate design change before altering a contract.
3. Implement a bounded task and verify the acceptance criteria in docs/03-build-plan.md. Update status and evidence honestly.
4. Keep money, authority, approval validity, state transitions, identity and idempotency deterministic. Model output is untrusted proposed input.
5. Make tenant scope explicit at storage, retrieval, cache, report and connector boundaries. References alone do not confer access.
6. Bind approval to precise target and source revisions. Known relevant changes prevent old approval from authorizing a new action.
7. Treat external outcome uncertainty separately from failure. Reconcile before deciding whether another dispatch is safe.
8. Keep expected labels and future events outside runtime inputs. Do not tune on held-out cases.
9. Distinguish document/schema checks, application tests and benchmark measurements. Never invent successful runs, savings, interviews or deployments.

## Repository boundary

Use original synthetic data and paraphrased public sources. Keep private notes, commercial strategy, affiliations, customer identities, credentials and operational exports outside the repository. Do not copy full reports or imply endorsement.

This blueprint does not authorize sending messages, connecting accounts, posting content, committing commercial terms, charging money or changing financial systems. Mock connectors are the v1 boundary. Real integrations require a separate concrete scope and authorization.

Do not silently replace a missing model with manufactured evidence. Preserve failures and label fallback output. Never count editing instructions as an edited video, a mock receipt as real publication, or a draft invoice packet as an issued invoice.

Markdown is the editable source of truth. Keep BLUEPRINT.html aligned when the specification changes. Link only to existing files; format planned paths and commands as code. Review docs/08-publication.md before making anything public. License choice remains pending until recorded.
