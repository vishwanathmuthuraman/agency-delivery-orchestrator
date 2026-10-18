import copy
import json
from pathlib import Path

import pytest

from agency_delivery_orchestrator.common import ContractError
from agency_delivery_orchestrator.replay import initial_state, reduce_event, replay, summarize

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture
def scenario():
    return json.loads((ROOT / "examples/client-claim-change.scenario.json").read_text())


@pytest.fixture
def revision(scenario):
    return copy.deepcopy(scenario["events"][3])


def revisions(revision, count):
    events = []
    for number in range(count):
        event = copy.deepcopy(revision)
        event["event_id"] = f"e-rev-{number}"
        event["at"] = f"2026-01-03T00:00:0{number}Z"
        event["payload"]["expected_version"] = 1 + number
        event["payload"]["new_version"] = 2 + number
        events.append(event)
    return events


def test_revision_updates_fact_and_invalidates_only_dependent_approvals(scenario, revision):
    state = reduce_event(initial_state(scenario), revision)
    result = summarize(state)
    assert result["fact_versions"] == {"battery-life": 2}
    bindings = {row["deliverable_id"]: row for row in result["approval_bindings"]}
    for identity in ("d-caption", "d-video"):
        assert bindings[identity]["current_content_approval"] is False
        assert bindings[identity]["current_dispatch_approval"] is False
    assert bindings["d-evergreen"]["current_dispatch_approval"] is True
    assert result["applied_event_ids"] == ["e-004"]
    assert result["external_write_count"] == 0


def test_reduction_does_not_mutate_inputs(scenario, revision):
    state = initial_state(scenario)
    before_state, before_event = copy.deepcopy(state), copy.deepcopy(revision)
    reduce_event(state, revision)
    assert state == before_state
    assert revision == before_event
    assert state["campaign"]["source_facts"][0]["version"] == 1


def test_replay_is_deterministic_and_restart_equivalent(scenario, revision):
    events = revisions(revision, 3)
    full = replay(scenario, events)
    assert full == replay(copy.deepcopy(scenario), copy.deepcopy(events))
    midpoint = json.loads(json.dumps(replay(scenario, events[:2])))
    resumed = reduce_event(midpoint, events[2])
    assert resumed == full
    assert summarize(full)["fact_versions"] == {"battery-life": 4}


def test_history_digest_depends_on_event_order_and_content(scenario, revision):
    first = replay(scenario, revisions(revision, 2))
    altered = revisions(revision, 2)
    altered[1]["payload"]["new_value"] = "Battery lasts 9 hours."
    assert replay(scenario, altered)["history_digest"] != first["history_digest"]


def test_duplicate_event_is_rejected(scenario, revision):
    state = reduce_event(initial_state(scenario), revision)
    with pytest.raises(ContractError, match="already applied"):
        reduce_event(state, revision)


def test_stale_and_skipped_versions_are_rejected(scenario, revision):
    state = initial_state(scenario)
    stale = copy.deepcopy(revision)
    stale["payload"]["expected_version"] = 2
    stale["payload"]["new_version"] = 3
    with pytest.raises(ContractError, match="stale"):
        reduce_event(state, stale)
    skipped = copy.deepcopy(revision)
    skipped["payload"]["new_version"] = 3
    with pytest.raises(ContractError, match="advance"):
        reduce_event(state, skipped)


def test_out_of_order_event_is_rejected(scenario, revision):
    first, second = revisions(revision, 2)
    state = reduce_event(initial_state(scenario), second | {"payload": first["payload"]})
    with pytest.raises(ContractError, match="chronologically"):
        reduce_event(state, first | {"payload": second["payload"]})


@pytest.mark.parametrize("field", ["tenant_id", "campaign_id"])
def test_foreign_tenant_or_campaign_is_rejected_without_state_change(scenario, revision, field):
    state = initial_state(scenario)
    before = copy.deepcopy(state)
    revision[field] = "foreign"
    with pytest.raises(ContractError, match="mismatch"):
        reduce_event(state, revision)
    assert state == before


def test_unauthorized_role_and_unsupported_kind_are_rejected(scenario, revision):
    state = initial_state(scenario)
    revision["actor_role"] = "agent"
    with pytest.raises(ContractError):
        reduce_event(state, revision)
    with pytest.raises(ContractError, match="unsupported"):
        replay(scenario)


def test_unknown_fact_and_invalid_shape_are_rejected(scenario, revision):
    state = initial_state(scenario)
    unknown = copy.deepcopy(revision)
    unknown["payload"]["fact_id"] = "absent"
    with pytest.raises(ContractError, match="unknown source fact"):
        reduce_event(state, unknown)
    revision["payload"]["extra"] = 1
    with pytest.raises(ContractError, match="schema violation"):
        reduce_event(state, revision)
