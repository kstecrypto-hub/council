"""Reconcile older cross-references; documentation changes only."""
from pathlib import Path
root = Path(__file__).resolve().parents[1]

def edit(name, replacements):
    path = root / name
    text = path.read_text(encoding='utf-8')
    for old, new in replacements:
        if old not in text:
            if new in text:
                continue
            raise ValueError(f'Missing expected source in {name}: {old[:100]!r}')
        text = text.replace(old, new)
    path.write_text(text, encoding='utf-8')

edit('docs/MVP_SCOPE_BY_STEP.txt', [
    ('one early/mid checkpoint with temporary reciprocal peer read access to the\n    participating repositories; and', 'one early/mid checkpoint that makes approved member repositories public,\n    collects all five sealed reviews, then opens shared discussion; and'),
    ('the peer-access window', 'the observed public-visibility window'),
    ('Revoke reciprocal repo access when the checkpoint closes.', 'Make member repositories private and verify visibility/isolation before private work resumes; public copies already taken cannot be recalled.'),
    ('Peers may clone/test another member\'s repo but never receive write access to it.', 'Peers may inspect pinned snapshots and test them in separate disposable verifiers; they receive no peer write/admin credentials or writable persistent reviewer mounts.'),
    ('/work uses a frozen or disposable checkpoint snapshot and is limited to verification activities.', '/work uses a separate disposable verification environment with pinned checkpoint inputs; it is limited to verification activities.'),
])

edit('docs/CHECKPOINT_COMMUNICATION_GATEWAY.md', [
    ('The exact DONE/ACTIVE/quiescing state contract will be specified in Part 4.', 'The AVAILABLE/WORKING/DONE/DISCONNECTED states and version-bound completion guards are defined in Part 4 and the October 13 refinements below; wire framing and executable integration remain pending.'),
    ('- the member has no accepted outbound message still pending delivery.', '- the member has no accepted outbound message still pending delivery;\n- its processed message frontier and expected obligation version match the current checkpoint generation;\n- it has no active verification work, and the completion decision is committed under the same guard as message/action acceptance and closure.'),
    ('may return that member to ACTIVE before checkpoint closure.', 'invalidates its completion certificate and returns that member to AVAILABLE before checkpoint closure.'),
    ('Verification must run against the frozen checkpoint snapshot or a disposable copy of that snapshot.', 'Executable verification must run in a separate disposable verifier with pinned checkpoint inputs, no writable reviewer workspace/continuation mounts, and externally retained execution evidence.'),
    ('checkpoint-visible repository in its own environment.', 'checkpoint-visible repository in a separate disposable verification environment.'),
    ('- peer repository access is absent;', '- live access to new unpublished peer repository work is absent; previously authorized frozen snapshots may remain available;'),
    ('The trusted runtime is responsible for checkpoint-related peer access grants/revocations.', 'The trusted runtime is responsible for approved checkpoint public/private visibility transitions, publication-safety checks, write freezes, and verification of the actual resulting visibility.'),
    ('- repository-access grant/revocation events;', '- public/private visibility requests and verified outcomes, including partial exposure, failed transitions, and publication-manifest references;'),
    ('-> freeze snapshots\n-> peer inspection and discussion', '-> freeze snapshots and pass publication approval/safety checks\n-> confirm member repositories public\n-> sealed independent review by all five members\n-> reveal assessments and open shared discussion'),
    ('-> close communication and peer access', '-> close communication and confirm repositories private'),
    ('- exact /done wire representation and ACTIVE/DONE/DISCONNECTED state transitions;', '- exact /done wire representation and integration of AVAILABLE/WORKING/DONE/DISCONNECTED transitions with versioned completion frontiers;'),
])

edit('docs/TYPED_INTERACTION_CONTRACTS.md', [
    ('- RECOVERING_RUNTIME_STATE\n', '- RECOVERING_RUNTIME_STATE\n- QUIESCING_FOR_PAUSE\n'),
    ('- RunPaused\n', '- RunPauseRequested\n- RunPaused\n'),
    ('ACTIVE -> PAUSED through PauseRun or a system safety condition.', 'PauseRun or a system safety condition stops new ordinary admissions and enters QUIESCING_FOR_PAUSE. ACTIVE -> PAUSED occurs only when the required durable pause boundary is confirmed. In-flight unknown external operations remain separately recorded and are not implicitly cancelled.'),
    ('| PauseRun | RunPaused | run PAUSED | paused state/banner |', '| PauseRun | RunPauseRequested | admissions stop; runtime quiesces controllable work | pausing state/banner, not yet PAUSED |\n| confirmed durable pause boundary | RunPaused | run PAUSED | paused state/banner |'),
    ('AVAILABLE may enter DONE only when no required peer obligation remains unanswered and no accepted outbound message remains pending.', 'AVAILABLE may enter DONE only when required response obligations are satisfied, required messages are processed, accepted outbound delivery is settled, no verification work remains active, and the checkpoint generation/message frontier/obligation version in its completion certificate match current canonical state.'),
])
p = root / 'docs/TYPED_INTERACTION_CONTRACTS.md'
with p.open('a', encoding='utf-8') as f:
    f.write('''\n### Pause-request contract refinement\n\nQUIESCING_FOR_PAUSE is runtime-owned activity entered by an authorized PauseRun or recorded safety trigger. It immediately closes ordinary work admission; fencing, safe persistence, reconciliation, and cleanup remain allowed. The UI shows pausing with affected members/operations and StopRun available, without a new blocking dialog. Repeated pause requests deduplicate. RunPaused is emitted only after the required controllable execution boundaries have quiesced and durable state is recorded; unknown provider outcomes remain visible independently. StopRun supersedes pending pause with STOPPING. Quiescence failure/ceiling records a blocked or failed pause operation rather than falsely declaring PAUSED; scope-specific recovery is governed by Part 7. ResumeRun is available only after PAUSED and current safety/authority/budget guards pass. No runtime implementation or test completion is implied.\n''')

p = root / 'tools/check_specs.py'
t = p.read_text(encoding='utf-8')
anchor = "        assert not re.search(pattern, text, re.I), (path.name, pattern)"
assert anchor in t
t = t.replace(anchor, anchor + "\n    for obsolete in ('temporary reciprocal peer read access', 'Revoke reciprocal repo access', 'checkpoint-related peer access grants/revocations', 'checkpoint-visible repository in its own environment'):\n        assert obsolete not in text, (path.name, obsolete)")
t += '''\nif contract['scope'] == 'specification_only':\n    assert contract['runtime_implementation_status'] == 'NOT_STARTED'\n    assert contract['runtime_test_status'] == 'NOT_RUN'\n    for item in contract['requirements']:\n        assert item['implementation_status'] == 'NOT_STARTED'\n        assert item['test_status'] == 'NOT_RUN'\n    print('Amendment status checks passed: no runtime requirement marked completed.')\n'''
p.write_text(t, encoding='utf-8')
for name in ('PART_5_TRANSACTIONS_IDEMPOTENCY_CONFLICTS.md', 'TYPED_INTERACTION_CONTRACTS.md'):
    p = root / 'docs' / name
    lines = p.read_text(encoding='utf-8').splitlines()
    p.write_text('\n'.join(line.rstrip() if line.startswith('**Status:** DESIGN AMENDED') else line for line in lines) + '\n', encoding='utf-8')
print('Public-checkpoint, verifier, completion, and pause references reconciled. Runtime remains unimplemented.')
