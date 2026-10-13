# AI project lead: complete product scope

**Direction recorded 13 October 2026; capabilities below are requirements, not implemented features.** The current implementation remains the initial campaign inspector described in [IMPLEMENTATION.md](IMPLEMENTATION.md). The intended product must operate the coordination loop, including real communication through a configured integration. Finishing the offline simulator alone will not complete this product.

The product promise is: **Keep company context, move projects forward, follow up with the right people, and verify that the work is actually done.** Agencies provide an initial test workflow; the context model must support several projects and shared resources within one organization.

## The complete coordination loop

1. Ingest permitted briefs, project records, discussions and decisions. Retain source, observed time, version, access policy and unresolved contradictions.
2. Maintain project outcomes, owners, dependencies, required inputs, capacity, budgets, deadlines and approval roles. Company context can inform a project only when the requesting principal may access it.
3. Identify what is blocked and choose the next useful intervention: ask for missing information, request work, seek approval, propose reassignment, propose resequencing, escalate, or wait.
4. Contact the mapped person through a configured channel using an explicit automated identity and the organization's approved communication policy. Routine follow-ups can run under that policy; commercial commitments and consequential changes require the relevant decision.
5. Receive a reply, deduplicate its event, resolve its thread and project, and propose a structured update with quoted evidence. A reply saying “done” is a claim to check. Ambiguous replies stay unresolved.
6. Validate and apply permitted updates, recalculate dependencies and capacity, stop acknowledged reminders, and surface deadline or cost tradeoffs for approval.
7. Obtain revision-bound review, verify the actual delivered artifact at its destination, and assemble the closure evidence. Preserve uncertainty and recover safely after a restart or lost receipt.

For example, a missing product claim blocks a script and video. The system requests that specific input from its owner, records the reply, proposes the source revision, releases eligible tasks after validation, notices a shared editor's capacity conflict, requests a decision, and follows the approved work through review and verified delivery. It must not claim the video was edited merely because it sent an editing request.

## Additional requirements

Existing FR-01–FR-20 and their contracts remain in force. These additions define the broader product; they do not change the offline v1 claim.

| ID | Requirement | Acceptance evidence required |
|---|---|---|
| FR-21 | Organization and project context | Two projects can share an explicitly authorized resource or policy; a restricted project, document or message cannot leak through retrieval, summaries, citations, caches or outbound text. Deny before loading unauthorized content. |
| FR-22 | Durable, attributable memory | Every imported assertion retains source identity, source revision, observation time and access policy. Corrections supersede previous facts without rewriting history. Conflicting sources remain visible; deletion/revocation removes cached retrieval access. |
| FR-23 | Bidirectional communication | A real sandbox channel can deliver an authorized request, receive and deduplicate a reply, authenticate its source and map it to the right project. Events carry stable IDs; retry and unknown-outcome reconciliation obey the actual provider contract. |
| FR-24 | Shared capacity and changing plans | Simultaneous projects expose resource conflicts. Proposed changes show downstream tasks, cost and deadline effects. The planner cannot silently alter accepted deadlines, budgets, leave or commitments. |
| FR-25 | Grounded AI proposals | A model can extract a proposed task, blocker, dependency or response update with resolvable citations. Schema validation, access checks and deterministic authority rules govern state changes. Untrusted message text cannot grant tool permissions. |
| FR-26 | Bounded follow-through | A persisted policy enforces working windows, recipient/project limits, acknowledgement stops, escalation roles, opt-outs and a pause control. Test restart recovery, duplicate callbacks, rate limits, bounced delivery and an ambiguous reply. |
| FR-27 | Evidence of completion | One recorded integration demonstration spans brief, missing input, outbound request, inbound reply, capacity decision, revised plan, approval, delivery verification and closure. Include a failure/recovery path and exact application/integration versions. |

Private account credentials, contact mappings and pilot data are configuration outside the public repository. Public fixtures remain synthetic. Implementing an adapter does not itself connect an account or send a message.

## First integrations: Slack and email

Both channels are in the first product integration scope. They share one organization-scoped identity map, conversation history and follow-up policy. A validated acknowledgement in either channel stops the same request's reminders in both. Sending through a second channel is an explicit policy decision, not an automatic response to an uncertain first delivery.

Slack ingestion must authenticate callbacks, persist event identities, handle duplicate delivery and respect channel visibility. Outbound messages retain workspace, channel and thread references. The implementation must follow the provider's [event delivery contract](https://docs.slack.dev/apis/events-api/), [request verification](https://docs.slack.dev/authentication/verifying-requests-from-slack/) and [rate limits](https://docs.slack.dev/apis/web-api/rate-limits/).

The email adapter must preserve provider message IDs and reply-thread references, distinguish accepted sending from delivery or a human acknowledgement, and handle bounces and automated replies without creating loops. A sender address or copied project identifier alone does not establish approval authority. Provider and mailbox authorization remain deployment choices to record before implementing the provider-specific adapter.

Shared acceptance cases include a Slack request answered by email, duplicate callbacks, a late reply after cancellation, two simultaneous projects involving the same person, revocation of source access, and a lost send response. These are requirements; neither live adapter exists yet.

## Where the AI and algorithm belong

The AI interprets permitted language and proposes structured updates. A separate planner evaluates actions against the current dependency graph, uncertain task/response durations, resource capacity and policy. The deterministic core enforces permission, identity, budgets, approval validity and external-effect constraints.

The research question is: **Which intervention is expected to prevent the most downstream delay for the attention it consumes?** A response-time forecast alone does not answer that question. The planner should compare alternatives, including waiting, and ask a question when reducing uncertainty is more valuable than another reminder.

A candidate approach combines a calibrated duration model, constrained scheduling and a budgeted look-ahead policy over partially observed project state. Begin with an inspectable finite-horizon baseline; add learned policies only if they beat it under the same observations and constraints. Historical associations do not establish that a reminder caused faster completion. Evaluate intervention effects in a simulator first, then only in a separately consented real study.

Compare against fixed reminders, earliest-deadline-first, critical-path-first and a resource-constrained scheduler. Report completion/delay, useful work finished, requests sent, interruption load, errors, policy violations and sensitivity to response assumptions. All policies receive the same observable information; hindsight oracles are labeled upper bounds. No improvement or novelty is established yet.

This belongs inside this project: it needs the same memory, task state, permissions, messages and outcome records. An independent planning library is justified later only if another workflow demonstrably reuses it.

## Build sequence and release boundary

1. Complete durable event replay and the existing offline lifecycle, including capacity, bounded follow-ups and verified closure.
2. Add organization/project access contracts and a model proposal interface, with synthetic tests for contradictions, malicious input and missing evidence.
3. Implement Slack and email behind the shared communication contract, with a sandbox contract suite for each and tests spanning both channels. Record the selected email provider and account permissions before provider-specific implementation.
4. Run the complete sandbox demonstration, then an explicitly authorized limited pilot. Measure real outcomes separately from simulation.
5. Evaluate the intervention planner against frozen baselines and seek independent reproduction.

The existing Gates A–D remain the original research milestones. **Product Gate E** additionally requires FR-21–FR-27, a tested real integration, a tested model-backed proposal path and operational pause/recovery controls. A deterministic mock model or mock connector cannot satisfy those requirements. Until Gate E has evidence, describe this as an early implementation of a proposed AI project lead.
