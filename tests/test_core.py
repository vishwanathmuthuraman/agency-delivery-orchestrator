import copy
import json
from pathlib import Path

import pytest

from agency_delivery_orchestrator.common import ContractError
from agency_delivery_orchestrator.core import (
    current_approval,
    estimate_cost,
    inspect,
    topological_order,
    validate_scenario,
)

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture
def scenario():
    return json.loads((ROOT / "examples/duplicate-dispatch.scenario.json").read_text())


@pytest.mark.parametrize(
    "path", sorted((ROOT / "examples").glob("*.scenario.json")), ids=lambda path: path.stem
)
def test_all_original_scenarios_validate_without_effects(path):
    result = inspect(json.loads(path.read_text()))
    assert result["estimated_cost_minor"] == 300000
    assert result["external_write_count"] == 0
    assert result["events_replayed"] is False


def test_half_up_rounding_and_exact_integer_boundary():
    assert estimate_cost(1, 30) == 1
    assert estimate_cost(1, 29) == 0
    with pytest.raises(ContractError):
        estimate_cost(1.0, 100)


def test_prerequisites_control_readiness(scenario):
    tasks = scenario["initial_campaign"]["tasks"]
    tasks[0]["status"] = "in_progress"
    tasks[1]["status"] = "blocked"
    tasks[1]["depends_on"] = [tasks[0]["task_id"]]
    result = inspect(scenario)
    task = next(row for row in result["tasks"] if row["task_id"] == tasks[1]["task_id"])
    assert task["ready"] is False
    assert task["incomplete_prerequisites"] == [tasks[0]["task_id"]]


@pytest.mark.parametrize(
    "mutation", ["cycle", "foreign", "unauthorized", "bad_cost", "unknown_fact", "unknown_rate"]
)
def test_semantic_contract_rejections(scenario, mutation):
    campaign = scenario["initial_campaign"]
    if mutation == "cycle":
        campaign["tasks"][0]["depends_on"] = [campaign["tasks"][0]["task_id"]]
    elif mutation == "foreign":
        scenario["events"][0]["tenant_id"] = "foreign"
    elif mutation == "unauthorized":
        campaign["approvals"][0]["approved_by_role"] = "agent"
    elif mutation == "bad_cost":
        campaign["tasks"][0]["estimated_cost_minor"] += 1
    elif mutation == "unknown_fact":
        campaign["deliverables"][0]["fact_refs"][0]["fact_id"] = "absent"
    else:
        campaign["tasks"][0]["rate_version"] = 99
    with pytest.raises(ContractError):
        validate_scenario(scenario)


def test_source_change_invalidates_binding_without_touching_unrelated_content(scenario):
    campaign = validate_scenario(scenario)
    at = "2026-01-02T00:00:00Z"
    assert current_approval(campaign, campaign["deliverables"][0], "dispatch", at)
    campaign["source_facts"][0]["version"] = 2
    assert not current_approval(campaign, campaign["deliverables"][0], "dispatch", at)
    assert current_approval(campaign, campaign["deliverables"][2], "dispatch", at)


def test_changed_content_version_requires_new_approval(scenario):
    campaign = scenario["initial_campaign"]
    campaign["deliverables"][0]["version"] = 2
    assert not current_approval(
        campaign, campaign["deliverables"][0], "dispatch", "2026-01-02T00:00:00Z"
    )


def test_topological_order_is_stable_across_input_order(scenario):
    tasks = scenario["initial_campaign"]["tasks"]
    assert topological_order(tasks) == topological_order(list(reversed(tasks)))


def test_no_input_mutation_or_hidden_dispatch(scenario):
    original = copy.deepcopy(scenario)
    assert inspect(scenario) == inspect(scenario)
    assert scenario == original


def test_running_task_is_not_ready_to_start(scenario):
    scenario["initial_campaign"]["tasks"][0]["status"] = "in_progress"
    result = inspect(scenario)
    assert result["tasks"][0]["ready"] is False


def test_approval_helper_rechecks_role_authority(scenario):
    campaign = scenario["initial_campaign"]
    campaign["approvals"][0]["approved_by_role"] = "agent"
    assert not current_approval(
        campaign, campaign["deliverables"][0], "dispatch", "2026-01-02T00:00:00Z"
    )
