"""Deterministic event reduction. Only source_revision_committed is implemented."""

import copy

from .common import ContractError, digest, timestamp, validate_shape
from .core import current_approval, validate_scenario

SUPPORTED_KINDS = frozenset({"source_revision_committed"})


def initial_state(scenario):
    campaign = validate_scenario(scenario)
    return {
        "campaign": copy.deepcopy(campaign),
        "applied_event_ids": [],
        "last_event_at": None,
        "history_digest": digest({"tenant_id": campaign["tenant_id"], "genesis": True}),
    }


def reduce_event(state, event):
    """Return a new state; the input state and event are never mutated."""
    validate_shape(event, "event")
    campaign = state["campaign"]
    if (event["tenant_id"], event["campaign_id"]) != (
        campaign["tenant_id"],
        campaign["campaign_id"],
    ):
        raise ContractError("tenant or campaign mismatch")
    roles = {row["role"]: row for row in campaign["authority_map"]}
    role = roles.get(event["actor_role"])
    if role is None or event["kind"] not in role["allowed_event_kinds"]:
        raise ContractError("unauthorized event role")
    if event["kind"] not in SUPPORTED_KINDS:
        raise ContractError("unsupported event kind")
    if event["event_id"] in state["applied_event_ids"]:
        raise ContractError("event already applied")
    at = timestamp(event["at"])
    if state["last_event_at"] is not None and at < timestamp(state["last_event_at"]):
        raise ContractError("events must be chronologically ordered")

    result = copy.deepcopy(state)
    payload = event["payload"]
    fact = next(
        (row for row in result["campaign"]["source_facts"] if row["fact_id"] == payload["fact_id"]),
        None,
    )
    if fact is None:
        raise ContractError("unknown source fact")
    if fact["version"] != payload["expected_version"]:
        raise ContractError("stale source revision")
    if payload["new_version"] != fact["version"] + 1:
        raise ContractError("source revision must advance by one")
    fact["version"] = payload["new_version"]
    fact["value"] = payload["new_value"]
    result["applied_event_ids"].append(event["event_id"])
    result["last_event_at"] = event["at"]
    result["history_digest"] = digest({"previous": state["history_digest"], "event": event})
    return result


def replay(scenario, events=None):
    """Replay events (default: the scenario's own) from the initial state."""
    state = initial_state(scenario)
    for event in scenario["events"] if events is None else events:
        state = reduce_event(state, event)
    return state


def summarize(state):
    campaign = state["campaign"]
    at = state["last_event_at"] or "1970-01-01T00:00:00Z"
    return {
        "fact_versions": {row["fact_id"]: row["version"] for row in campaign["source_facts"]},
        "approval_bindings": [
            {
                "deliverable_id": row["deliverable_id"],
                "current_content_approval": current_approval(campaign, row, "content", at),
                "current_dispatch_approval": current_approval(campaign, row, "dispatch", at),
            }
            for row in campaign["deliverables"]
        ],
        "applied_event_ids": list(state["applied_event_ids"]),
        "history_digest": state["history_digest"],
        "external_write_count": 0,
    }
