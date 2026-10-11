# Original synthetic examples

These six examples specify expected behavior. They are not output from an implemented application, a completed benchmark, or customer incidents. Expected files are evaluator-only and must not be given to a future agent or policy.

| Scenario | What it specifies |
| --- | --- |
| `clean-delivery` | Baseline scope approval, work completion, mock dispatch, acceptance and billing-readiness. |
| `client-claim-change` | A source change affects caption and narration; prepare supported text and a human editing handoff. |
| `stale-approval` | The final guard blocks dispatch bound to an obsolete source version. |
| `duplicate-dispatch` | Same intent/key/payload reuses the result; one connector write attempt. |
| `uncertain-dispatch` | Unknown external outcome prevents a blind retry and stays unresolved. |
| `cross-client-reference` | Cross-tenant reference denied before retrieving another client's records. |

## Read a fixture

1. Load only `*.scenario.json` into the future runner.
2. Validate against [scenario schema](../schemas/scenario.schema.json).
3. Treat `initial_campaign` as the supplied starting snapshot, not an observed real business.
4. Process events in listed order. `event_id` identifies input delivery; `action_id` identifies business intent; `idempotency_key` binds that intent to one canonical payload.
5. Write actual observations to a separate output directory. A separate scorer will compare them with `*.expected.json` after the run.

All fixtures are single-tenant at the authorized boundary. A denied target reference is an adversarial input, not permission to retrieve it. All destinations are `mock://`; no fixture authorizes a real message, publication, edit or financial action.

## Contract semantics

The JSON schema files are authoritative for keys. Schemas are self-contained so validation needs no network resolver. `campaign.schema.json` describes the initial campaign object, `event.schema.json` an individual input event, `scenario.schema.json` their envelope, and `expected-result.schema.json` the evaluator's specified outcome. Version 1.0 is the documentation contract, not a software release.

Money uses integer minor units in the campaign's single ISO currency. The fixtures use INR, where 100 minor units equal one rupee. `minor_per_hour` and `estimated_minutes` produce task cost by integer rational arithmetic, rounded half-up once per task. The initial tasks total 300,000 minor units (₹3,000); the budget is 12,000,000 minor units (₹120,000). The reviewed additional 90 minutes costs 150,000 minor units (₹1,500) at the supplied rate. A cost allowance and client fee are different fields. The change example absorbs that cost; it does not bill a fee.

Source and artifact revisions increase by one, with the previous version as a compare-and-set precondition. Approvals bind purpose, subject/version and relevant fact versions within tenant/campaign context. A dispatch request refers to a current valid dispatch-purpose approval, and a separate current content-purpose approval must also cover its artifact. Roles have explicit allowed approval purposes; permission to emit an approval event alone cannot grant every kind of approval. A reviewed dependency can cause an unchanged artifact to require fresh approval when its supporting source changes.

`source_revision_committed` follows a recorded commercial choice in these examples. An incoming unapproved request is not itself a committed source change. Rejected requests must not alter the baseline. The architecture separately specifies immediate holds after a trusted, verified factual invalidation, independent of commercial negotiation. That policy requires the future event-contract extension and tests described there; these six fixtures do not exercise it. Commercial disagreement cannot authorize publication of known-invalid content.

`video_edit_packet` represents editing instructions and human completion evidence, not a rendered video. `work_completed` is a trusted mock completion assertion carrying IDs and a version; it is not an evidence bundle. The clean case verifies delivery of an editing packet, not a rendered video. Real completion evidence and rendered-media verification remain future work. `connector_observed` means evidence from the mock connector; successful observed version must match the attempted version before verification. Its supplied event cannot bypass the action record, scope or authorization checks. A real connector's observations must come from a trusted adapter, not client content.

`expected_external_write_count` counts attempted outbound mock connector writes. It does not count API reads and does not prove a side effect succeeded. The uncertain case has one attempt with no confirmed outcome. Retrying the same intent cannot create another write merely because a response was lost. Reconciliation, new authority and preconditions would be needed to resolve it safely.

Terminal state is the scenario result. `blocked` can describe a denied operation while leaving the campaign open. `review_required` means legitimate work remains; it is not necessarily a fault. `complete` requires current verified outputs and explicit acceptance for every in-scope deliverable; billing-readiness creates only a draft handoff. Expected outcome codes are specification labels, not fabricated run logs.

These control fixtures already supply reviewed impact and prepared text in input events. They can test state transitions and execution guards, not whether an AI independently discovered dependencies or drafted correct text. In the separate semantic evaluation, collect and freeze model proposals before revealing reviewer results or prepared edits.

The fixture `authority_map` and each event's `actor_role` represent trusted harness context. The runner must match the role to permitted event kinds and tenant scope before mutation, and check payload approver/reviewer roles against that context. In a real system identity must come from authenticated users or adapters; role strings inside client content cannot authorize actions. Initial approval `valid: true` must still be checked against authority, purpose, current subject and source bindings.

The exact expected invalidation list in `client-claim-change` describes the selective reference policy. `selective_only_must_not_happen` applies only to the selective reference policy; `must_not_happen` applies to every strategy. The invalidate-all comparison may invalidate more approvals, but is scored for that extra work rather than treated as violating its own policy. All strategies share the final dispatch guard and must not execute stale or unauthorized work.

## Validate documentation today

Run `python3 scripts/validate_blueprint.py` from the repository root. It requires the `jsonschema` package and checks schemas, example structure, reference integrity, task arithmetic, documentation links and task dependencies. It does not run the proposed application or establish expected outcomes. The validator reports its checks and exits nonzero on a defect.

The six public examples are development references and must never be described as unseen evaluation cases. Additional development and held-out datasets remain to be authored under the evaluation protocol.
