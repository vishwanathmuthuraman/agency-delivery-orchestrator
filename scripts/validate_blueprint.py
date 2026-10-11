"""Validate documentation contracts only; never execute proposed application behavior."""
from pathlib import Path
from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP
from urllib.parse import urlparse, unquote
import csv
import json
import re
import sys

try:
    from jsonschema import Draft202012Validator, FormatChecker
except ImportError:
    raise SystemExit('Install the documentation dependencies from requirements-blueprint.txt first.')

ROOT = Path(__file__).resolve().parents[1]


def check(condition, explanation):
    if not condition:
        raise ValueError(explanation)


def unique(items, key, label):
    values = [item[key] for item in items]
    check(len(values) == len(set(values)), f'Duplicate {label}')
    return set(values)


def run():
    schemas = {}
    for path in sorted((ROOT / 'schemas').glob('*.schema.json')):
        schema = json.loads(path.read_text())
        Draft202012Validator.check_schema(schema)
        schemas[path.name] = schema
    check(len(schemas) == 4, 'Expected four self-contained contracts')
    validators = {name: Draft202012Validator(schema, format_checker=FormatChecker()) for name, schema in schemas.items()}
    scenarios = sorted((ROOT / 'examples').glob('*.scenario.json'))
    check(len(scenarios) == 6, 'Expected six public scenario specifications')
    for path in scenarios:
        value = json.loads(path.read_text())
        validators['scenario.schema.json'].validate(value)
        expected_path = path.with_name(path.name.replace('.scenario.json', '.expected.json'))
        expected = json.loads(expected_path.read_text())
        validators['expected-result.schema.json'].validate(expected)
        check(value['scenario_id'] == expected['scenario_id'], f'{path.name}: mismatched oracle ID')
        campaign = value['initial_campaign']
        validators['campaign.schema.json'].validate(campaign)
        fact_ids = unique(campaign['source_facts'], 'fact_id', 'fact IDs')
        deliverable_ids = unique(campaign['deliverables'], 'deliverable_id', 'deliverable IDs')
        task_ids = unique(campaign['tasks'], 'task_id', 'task IDs')
        approval_ids = unique(campaign['approvals'], 'approval_id', 'approval IDs')
        rates = {(rate['role'], rate['version']): rate['minor_per_hour'] for rate in campaign['cost_rates']}
        check(len(rates) == len(campaign['cost_rates']), 'Duplicate role/rate versions')
        fact_versions = {fact['fact_id']: fact['version'] for fact in campaign['source_facts']}
        authority = {entry['role']: set(entry['allowed_event_kinds']) for entry in campaign['authority_map']}
        approval_authority = {entry['role']: set(entry['allowed_approval_purposes']) for entry in campaign['authority_map']}
        check(len(authority) == len(campaign['authority_map']), 'Duplicate authority roles')
        for artifact in campaign['deliverables']:
            for ref in artifact['fact_refs']:
                check(ref['fact_id'] in fact_ids and ref['fact_version'] == fact_versions[ref['fact_id']], 'Initial artifact has missing/stale fact reference')
        for task in campaign['tasks']:
            check(task['deliverable_id'] in deliverable_ids, 'Task has unknown deliverable')
            check(set(task['depends_on']) <= task_ids and task['task_id'] not in task['depends_on'], 'Invalid task dependencies')
            rate = rates[(task['owner_role'], task['rate_version'])]
            cost = int((Decimal(rate) * Decimal(task['estimated_minutes']) / Decimal(60)).quantize(Decimal('1'), rounding=ROUND_HALF_UP))
            check(cost == task['estimated_cost_minor'], 'Task estimate arithmetic mismatch')
        for approval in campaign['approvals']:
            check(approval['subject_id'] in deliverable_ids or approval['subject_id'] == campaign['campaign_id'], 'Unknown approval subject')
            check(approval['purpose'] in approval_authority.get(approval['approved_by_role'], set()), 'Initial approval role lacks purpose authority')
        unique(value['events'], 'event_id', 'event IDs')
        previous = None
        for event in value['events']:
            validators['event.schema.json'].validate(event)
            check(event['tenant_id'] == campaign['tenant_id'] and event['campaign_id'] == campaign['campaign_id'], 'Event has wrong authorized context')
            check(event['kind'] in authority.get(event['actor_role'], set()), 'Event actor lacks fixture authority')
            if event['kind'] == 'approval_granted':
                check(event['payload']['purpose'] in approval_authority.get(event['actor_role'], set()), 'Event actor lacks approval purpose authority')
            for field in ['approver_role', 'approved_by_role', 'reviewer_role']:
                if field in event['payload']:
                    check(event['payload'][field] == event['actor_role'], 'Claimed payload authority differs from trusted event context')
            timestamp = datetime.fromisoformat(event['at'].replace('Z', '+00:00'))
            check(previous is None or timestamp >= previous, 'Fixture events out of order')
            previous = timestamp
        check(set(expected['expected_affected_deliverable_ids']) <= deliverable_ids, 'Unknown expected affected artifact')
        check(set(expected['expected_invalidated_approval_ids']) <= approval_ids, 'Unknown initial approval in expected invalidations')

    documents = [ROOT / 'README.md', ROOT / 'AGENTS.md', ROOT / 'examples/README.md', *sorted((ROOT / 'docs').glob('*.md'))]
    check(len(list((ROOT / 'docs').glob('[0-9][0-9]-*.md'))) == 8, 'Expected eight numbered design documents')
    checked_links = 0
    for document in documents:
        text = document.read_text()
        for target in re.findall(r'(?<!!)\[[^\]]+\]\(([^\s)]+)(?:\s+"[^"]*")?\)', text):
            target = target.strip('<>')
            parsed = urlparse(target)
            if parsed.scheme or not parsed.path:
                continue
            resolved = (document.parent / unquote(parsed.path)).resolve()
            check(resolved.exists(), f'Missing linked file: {document.relative_to(ROOT)} -> {target}')
            checked_links += 1
    rows = list(csv.DictReader((ROOT / 'planning/tasks.csv').open(newline='')))
    check(len(rows) >= 30, 'Expected detailed implementation task tracker')
    ids = [row['task_id'] for row in rows]
    check(len(ids) == len(set(ids)), 'Duplicate tracker task IDs')
    visited = set()
    low = high = 0
    for row in rows:
        dependencies = {x.strip() for x in row['dependencies'].split(';') if x.strip()}
        check(dependencies <= visited, f'Task is not in dependency order: {row["task_id"]}')
        check(row['status'] == 'not_started', 'Blueprint must not claim implementation completed')
        low += float(row['estimate_hours_low'])
        high += float(row['estimate_hours_high'])
        check(float(row['estimate_hours_low']) <= float(row['estimate_hours_high']), 'Invalid task estimate range')
        visited.add(row['task_id'])
    print(json.dumps({'validation_type': 'documentation_only', 'schemas': len(schemas), 'public_scenarios': len(scenarios), 'expected_files_are_specifications': True, 'numbered_documents': 8, 'local_markdown_links_checked': checked_links, 'planned_tasks': len(rows), 'planned_hours_low': low, 'planned_hours_high': high, 'application_executed': False, 'benchmark_executed': False}, indent=2))


if __name__ == '__main__':
    try:
        run()
    except (ValueError, KeyError, OSError) as error:
        print(f'Blueprint validation failed: {error}', file=sys.stderr)
        sys.exit(1)
