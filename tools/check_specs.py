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
assert contract['private_work_requires_finite_slices'] is True
assert 'sealed_review' in contract['checkpoint_phases']
assert set(contract['done_requires']) == {'checkpoint_generation', 'processed_message_sequence', 'expected_obligation_version'}
assert len(contract['separate_outcomes']) == 4
assert contract['event_ordering'] == 'deployment_transactional_event_clock'
assert contract['long_term_learning_store'] == 'git_backed_archive'
assert len({x['id'] for x in contract['requirements']}) == 12
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
    for link in re.findall(r'\]\(([^)\s]+)(?:\s+[^)]*)?\)', text):
        if '://' in link or link.startswith(('#', 'mailto:')):
            continue
        target = link.split('#', 1)[0]
        if target:
            assert (path.parent / target).exists(), (path.name, link)
assert 'SEALED_REVIEW' in (root / 'docs/TYPED_INTERACTION_CONTRACTS.md').read_text()
assert 'NOT STARTED' in (root / 'README.md').read_text()
print(f'Static specification checks passed: {len(files)} documents and 12 tracked requirements.')
print('Scope: documentation/contract consistency only. Runtime tests and comparative evaluations NOT RUN.')
