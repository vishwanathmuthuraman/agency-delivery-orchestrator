"""Campaign contracts, task readiness and revision-bound approval checks."""

from .common import ContractError, exact_integer, timestamp, unique, validate_shape


def estimate_cost(minutes, minor_per_hour):
    numerator = exact_integer(exact_integer(minutes) * exact_integer(minor_per_hour))
    return (numerator + 30) // 60  # half-up to one minor unit


def topological_order(tasks):
    indexed = unique(tasks, lambda row: row["task_id"])
    result, visited, active = [], set(), set()

    def visit(identity):
        if identity not in indexed:
            raise ContractError("unknown task prerequisite")
        if identity in active:
            raise ContractError("cyclic task dependencies")
        if identity in visited:
            return
        active.add(identity)
        for parent in sorted(indexed[identity]["depends_on"]):
            visit(parent)
        active.remove(identity)
        visited.add(identity)
        result.append(identity)

    for identity in sorted(indexed):
        visit(identity)
    return result


def validate_scenario(scenario):
    validate_shape(scenario, "scenario")
    campaign = scenario["initial_campaign"]
    exact_integer(campaign["budget_minor"])
    facts = unique(campaign["source_facts"], lambda row: row["fact_id"])
    deliverables = unique(campaign["deliverables"], lambda row: row["deliverable_id"])
    approvals = unique(campaign["approvals"], lambda row: row["approval_id"])
    roles = unique(campaign["authority_map"], lambda row: row["role"])
    rates = unique(campaign["cost_rates"], lambda row: (row["role"], row["version"]))
    topological_order(campaign["tasks"])
    for deliverable in deliverables.values():
        for reference in deliverable["fact_refs"]:
            if reference["fact_id"] not in facts:
                raise ContractError("unknown source fact")
    for task in campaign["tasks"]:
        if task["deliverable_id"] not in deliverables:
            raise ContractError("unknown task output")
        key = task["owner_role"], task["rate_version"]
        if key not in rates:
            raise ContractError("unknown rate version")
        if estimate_cost(task["estimated_minutes"], rates[key]["minor_per_hour"]) != exact_integer(
            task["estimated_cost_minor"]
        ):
            raise ContractError("inconsistent task cost")
    for approval in approvals.values():
        timestamp(approval["approved_at"])
        role = roles.get(approval["approved_by_role"])
        if role is None or approval["purpose"] not in role["allowed_approval_purposes"]:
            raise ContractError("unauthorized approval role")
        if any(reference["fact_id"] not in facts for reference in approval["fact_refs"]):
            raise ContractError("unknown approval evidence")
    unique(scenario["events"], lambda row: row["event_id"])
    previous = None
    for event in scenario["events"]:
        if (event["tenant_id"], event["campaign_id"]) != (
            campaign["tenant_id"],
            campaign["campaign_id"],
        ):
            raise ContractError("tenant or campaign mismatch")
        role = roles.get(event["actor_role"])
        if role is None or event["kind"] not in role["allowed_event_kinds"]:
            raise ContractError("unauthorized event role")
        at = timestamp(event["at"])
        if previous is not None and at < previous:
            raise ContractError("events must be chronologically ordered")
        previous = at
    return campaign


def current_approval(campaign, deliverable, purpose, at):
    roles = {row["role"]: row for row in campaign["authority_map"]}
    facts = {row["fact_id"]: row["version"] for row in campaign["source_facts"]}
    needed = {(row["fact_id"], row["fact_version"]) for row in deliverable["fact_refs"]}
    if any(facts.get(identity) != version for identity, version in needed):
        return False
    for approval in campaign["approvals"]:
        role = roles.get(approval["approved_by_role"])
        if role is None or purpose not in role["allowed_approval_purposes"]:
            continue
        bound = {(row["fact_id"], row["fact_version"]) for row in approval["fact_refs"]}
        if (
            approval["valid"]
            and approval["purpose"] == purpose
            and approval["subject_id"] == deliverable["deliverable_id"]
            and approval["subject_version"] == deliverable["version"]
            and timestamp(approval["approved_at"]) <= timestamp(at)
            and bound == needed
        ):
            return True
    return False


def inspect(scenario):
    campaign = validate_scenario(scenario)
    tasks = {row["task_id"]: row for row in campaign["tasks"]}
    costs = exact_integer(sum(row["estimated_cost_minor"] for row in tasks.values()))
    at = scenario["events"][0]["at"] if scenario["events"] else "1970-01-01T00:00:00Z"
    readiness = []
    for identity in topological_order(campaign["tasks"]):
        task = tasks[identity]
        missing = [parent for parent in task["depends_on"] if tasks[parent]["status"] != "complete"]
        readiness.append(
            {
                "task_id": identity,
                "status": task["status"],
                "ready": task["status"] in {"ready", "blocked"} and not missing,
                "incomplete_prerequisites": missing,
            }
        )
    approvals = [
        {
            "deliverable_id": row["deliverable_id"],
            "current_content_approval": current_approval(campaign, row, "content", at),
            "current_dispatch_approval": current_approval(campaign, row, "dispatch", at),
        }
        for row in campaign["deliverables"]
    ]
    return {
        "schema_version": "0.1",
        "kind": "initial_campaign_inspection",
        "tenant_id": campaign["tenant_id"],
        "campaign_id": campaign["campaign_id"],
        "currency": campaign["currency"],
        "estimated_cost_minor": costs,
        "over_budget": costs > campaign["budget_minor"],
        "tasks": readiness,
        "approval_bindings": approvals,
        "events_replayed": False,
        "external_write_count": 0,
    }
