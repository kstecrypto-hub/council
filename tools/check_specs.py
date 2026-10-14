"""Static specification checks only; no Council runtime is exercised."""
from pathlib import Path
import json
import re

root = Path(__file__).resolve().parents[1]
contract = json.loads((root / 'docs/architecture_contract.json').read_text())
assert contract['logical_member_count'] == 5
assert contract['repository_visibility_cycle'] == ['private', 'public', 'private']
assert contract['public_exposure_reversible'] is False
assert contract['changes_council_source_repository_visibility'] is False
assert contract['peer_verification_environment'] == 'separate_disposable'
assert contract['private_work_requires_finite_slices'] is False
for step_no in (3, 4, 5):
    row = contract[f'step{step_no}']
    assert row['design_status'] == 'DESIGNED', step_no
    assert row['implementation_status'] == 'NOT_STARTED', step_no
    assert row['runtime_tests_status'] == 'NOT_RUN', step_no
assert contract['step3']['checkpoints_require_all_five_unique_member_arrivals']
assert contract['step3']['sealed_review'] == 'one_immutable_submission_per_seat_per_generation_and_atomic_all_five_reveal'
assert contract['step4']['command_replay_order'] == 'authenticate_authorize_then_idempotency_before_stale_transition_guards'
assert contract['step5']['external_effects_execute_after_commit'] is True
assert contract['step5']['committed_positions_from_sequence'] is False
assert contract['step7']['design_status'] == 'DESIGNED'
assert contract['step7']['runtime_implementation_status'] == 'NOT_STARTED'
assert contract['step7']['runtime_tests_status'] == 'NOT_RUN'
assert contract['step7']['no_general_reasoning_deadline'] is True
assert contract['step7']['budget_exhaustion_not_semantic_readiness'] is True
assert sum(contract['step7']['suggested_default_budget_allocation_percent'].values()) == 100
assert contract['step7']['initial_remote_model_call_cap_per_provider'] == 2
assert contract['step7']['initial_local_inference_concurrency_cap'] == 1
assert contract['step7']['default_recovery_retries'] == 3
assert 'sealed_review' in contract['checkpoint_phases']
assert set(contract['done_requires']) == {'checkpoint_generation', 'processed_message_sequence', 'expected_obligation_version'}
assert len(contract['separate_outcomes']) == 4
assert contract['event_ordering'] == 'deployment_transactional_event_clock'
assert contract['long_term_learning_store'] == 'git_backed_archive'
assert len({x['id'] for x in contract['requirements']}) == len(contract['requirements'])
assert len(contract['requirements']) >= 13
assert {'ADR-02', 'ADR-05', 'ADR-13'} <= {x['id'] for x in contract['requirements']}
assert all(x['design_status'] == 'DESIGNED' for x in contract['requirements'] if x['id'] in {'ADR-02', 'ADR-05'})
for item in contract['requirements']:
    if item['implementation_status'] == 'IMPLEMENTED':
        assert item['implementation_evidence'], item['id']
    if item['test_status'] == 'PASSED':
        assert item['test_evidence'], item['id']

files = list((root / 'docs').glob('*.md')) + list((root / 'docs').glob('*.txt'))
files += [root / 'README.md', root / 'AGENTS.md', root / 'VERIFICATION.md']
for path in files:
    text = path.read_text(encoding='utf-8')
    for pattern in (r'three configurable council seats', r'three council members', r'3[-\u2013]4', r'solution_registry', r'solution_versions\(solution_id', r'Internet-wide public visibility is not an architectural requirement', r'Temporary collaborator/read access.*preferred default'):
        assert not re.search(pattern, text, re.I), (path.name, pattern)
    for obsolete in ('temporary reciprocal peer read access', 'Revoke reciprocal repo access', 'checkpoint-related peer access grants/revocations', 'checkpoint-visible repository in its own environment'):
        assert obsolete not in text, (path.name, obsolete)
    for link in re.findall(r'\]\(([^)\s]+)(?:\s+[^)]*)?\)', text):
        if '://' in link or link.startswith(('#', 'mailto:')):
            continue
        target = link.split('#', 1)[0]
        if target:
            assert (path.parent / target).exists(), (path.name, link)
assert 'SEALED_REVIEW' in (root / 'docs/TYPED_INTERACTION_CONTRACTS.md').read_text()
assert 'NOT STARTED' in (root / 'README.md').read_text()
scope_text = (root / 'docs/MVP_SCOPE_BY_STEP.txt').read_text(encoding='utf-8')
for n in (3, 4, 5):
    section = scope_text.split(f'STEP {n} -', 1)[1].split(f'STEP {n+1} -', 1)[0]
    assert 'Status: DESIGNED' in section, n
for doc, required in (
    ('POSTGRES_DATA_MODEL.md', '## 20. October 14 Part 3 design closure'),
    ('TYPED_INTERACTION_CONTRACTS.md', '## 26. October 14 Part 4 design closure'),
    ('PART_5_TRANSACTIONS_IDEMPOTENCY_CONFLICTS.md', '## 16. October 14 Part 5 design closure')
):
    text_doc = (root / 'docs' / doc).read_text(encoding='utf-8')
    assert required in text_doc, (doc, required)
    assert 'DESIGNED' in text_doc, doc
assert 'Status: DESIGNED' in (root / 'docs/MVP_SCOPE_BY_STEP.txt').read_text(encoding='utf-8').split('STEP 7 -', 1)[1].split('STEP 8 -', 1)[0]
assert '**Design status:** DESIGNED' in (root / 'docs/PART_7_MEMBER_SCHEDULING_RECOVERY_RESOURCES.md').read_text(encoding='utf-8')
print(f'Static specification checks passed: {len(files)} documents and {len(contract["requirements"])} tracked requirements.')
print('Scope: documentation/contract consistency only. Runtime tests and comparative evaluations NOT RUN.')

if contract['scope'] == 'specification_only':
    assert contract['runtime_implementation_status'] == 'NOT_STARTED'
    assert contract['runtime_test_status'] == 'NOT_RUN'
    for item in contract['requirements']:
        assert item['implementation_status'] == 'NOT_STARTED'
        assert item['test_status'] == 'NOT_RUN'
    print('Amendment status checks passed: no runtime requirement marked completed.')
