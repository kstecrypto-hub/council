"""Static specification checks only; no Council runtime is exercised."""
from pathlib import Path
import json
import re

root = Path(__file__).resolve().parents[1]
contract = json.loads((root / 'docs/architecture_contract.json').read_text())
assert contract['logical_member_count'] == 5
assert contract['repository_visibility_cycle'] == ['private_work', 'approved_checkpoint_local_read_only_snapshot', 'private_work']
assert contract['checkpoint_public_github_default'] is False
assert contract['repository_backend_default'] == 'native_local_git'
assert contract['cross_customer_knowledge_sharing_default'] is False
assert contract['failure_memory_policy'] == 'success_first_conditional_failure_warning_never_universal_blacklist'
assert contract['step2']['design_status'] == 'DESIGNED'
assert contract['public_exposure_reversible'] is False
assert contract['changes_council_source_repository_visibility'] is False
assert contract['peer_verification_environment'] == 'separate_disposable'
assert contract['private_work_requires_finite_slices'] is False
for step_no in (3, 4, 5):
    row = contract[f'step{step_no}']
    assert row['design_status'] == 'DESIGNED', step_no
    assert row['baseline_design_status'] == 'DESIGNED_UNDER_SUPERSEDED_PUBLIC_GITHUB_POLICY', step_no
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
assert 'suggested_default_budget_allocation_percent' not in contract['step7']
assert contract['step7']['budget_allocation_policy'] == 'PROJECT_SPECIFIC_FIVE_PROTECTED_SCOPES_WITH_EXPLICIT_USER_APPROVAL_NO_UNIVERSAL_PERCENTAGES'
assert contract['final_product_policy']['final_user_acceptance_target'] == 'EXACT_CURRENT_INTEGRATED_ARTIFACT_AND_FROZEN_REPORT_PACKAGE_NOT_ORIGINAL_MEMBER_CANDIDATE'
assert contract['step8']['step8_5cd']['queue_policy']['additional_api_per_key_lanes_required'] is False
assert contract['step7']['initial_remote_model_call_cap_per_provider'] == 2
assert contract['step7']['initial_local_inference_concurrency_cap'] == 1
assert contract['step7']['default_recovery_retries'] == 3
assert 'sealed_review' in contract['checkpoint_phases']
assert set(contract['done_requires']) == {'checkpoint_generation', 'processed_message_sequence', 'expected_obligation_version'}
assert len(contract['separate_outcomes']) == 4
assert contract['event_ordering'] == 'deployment_transactional_event_clock'
assert contract['long_term_learning_store'] == 'customer_owned_git_archive_with_optional_permitted_general_knowledge'
assert len({x['id'] for x in contract['requirements']}) == len(contract['requirements'])
assert len(contract['requirements']) >= 18
assert {'ADR-13', 'ADR-14', 'ADR-15', 'ADR-16', 'ADR-17', 'ADR-18'} <= {x['id'] for x in contract['requirements']}
assert contract['requirements'][0]['design_status'] == 'SUPERSEDED_BY_ADR_17'
assert contract['step11']['negative_exclusion_policy'] == 'no_universal_blacklist_or_silent_filter_based_on_prior_failure'
assert contract['step8']['design_status'] == 'DESIGNED'
assert contract['step8']['runtime_implementation_status'] == 'NOT_STARTED'
assert contract['step8']['runtime_tests_status'] == 'NOT_RUN'
assert contract['step8']['experiment_is_optional_under_act'] is True
assert contract['step8']['separate_ai_judge_or_experiment_scheduler'] is False
assert contract['step8']['worker_may_declare_parent_checkpoint_ready'] is False
assert contract['step8']['checkpoint_work_excursion'] == 'verification_only_disposable_read_only_candidate'
assert contract['step8']['member_controls_local_worker_count_and_depth'] is True
assert contract['step8']['fixed_member_local_worker_count_cap'] is None
assert contract['step8']['fixed_member_local_worker_delegation_depth_cap'] is None
assert contract['step8']['no_central_scheduler_for_internal_workers'] is True
assert contract['step8']['direct_docker_engine_socket_access_to_agent_sandbox'] is False
assert contract['step8']['resource_monitor']['monitor_owner'] == 'trusted_deployment_control_plane_outside_agent_sandboxes'
assert contract['step8']['resource_monitor']['sampling_seconds_initial_range'] == [2, 5]
assert contract['step8']['resource_monitor']['soft_sandbox_memory_threshold_percent'] == 80
assert contract['step8']['resource_monitor']['high_sandbox_memory_threshold_percent'] == 90
assert contract['step8']['resource_monitor']['monitors_every_internal_worker_individually'] is False
assert contract['step8']['resource_monitor']['monitor_guarantees_crash_prevention'] is False
assert contract['step8']['resource_monitor']['implementation_status'] == 'NOT_STARTED'
assert contract['step8']['resource_monitor']['test_status'] == 'NOT_RUN'
assert contract['step7']['resource_monitor_approved'] is True
assert contract['step7']['member_workspace_storage'] == 'stable_private_docker_volume'
assert contract['step7']['council_worker_recovery_daemon_required'] is False
worker_store = contract['step8']['worker_persistence']
assert worker_store['durable_storage'] == 'dedicated_named_Docker_volume_or_authorized_bind_mount_per_member'
assert worker_store['container_writable_layer_survives_recreation'] is False
assert worker_store['in_memory_process_resumption_on_restart'] is False
assert worker_store['parent_member_controls_local_worker_resume'] is True
assert worker_store['dedicated_council_worker_recovery_service'] is False
assert worker_store['uncontrolled_docker_restart_during_pause_or_checkpoint'] is False
assert worker_store['external_effect_reconciliation_still_required'] is True
assert worker_store['implementation_status'] == 'NOT_STARTED'
assert worker_store['test_status'] == 'NOT_RUN'
assert 'worker_result_return_cancellation_crash_recovery_and_merge_protocol' not in contract['step8']['pending_design']

assert contract['step7']['shared_local_inference_one_job_cap_applies_to'] == 'trusted_shared_local_model_gateway_not_arbitrary_sandbox_local_subagent_processes'
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
assert 'Status: DESIGNED' in scope_text.split('STEP 2 -', 1)[1].split('STEP 3 -', 1)[0]
local_repos = (root / 'docs/LOCAL_REPOSITORY_AND_KNOWLEDGE_RETENTION.md').read_text(encoding='utf-8')
assert 'Success-first retrieval' in local_repos
assert 'FAILED_IN_CONTEXT' in local_repos
assert 'customer' in local_repos.lower() and 'Git' in local_repos
assert 'no internet-public publication' in local_repos or 'No internet-public publication' in local_repos
assert 'Status: DESIGNED' in (root / 'docs/MVP_SCOPE_BY_STEP.txt').read_text(encoding='utf-8').split('STEP 7 -', 1)[1].split('STEP 8 -', 1)[0]
assert '**Design status:** DESIGNED' in (root / 'docs/PART_7_MEMBER_SCHEDULING_RECOVERY_RESOURCES.md').read_text(encoding='utf-8')
step8_spec = (root / 'docs/PART_8_AGENT_LOOP_EXPERIMENTATION_DELEGATION.md').read_text(encoding='utf-8')
assert '**Design status:** DESIGNED' in step8_spec
assert 'HYPOTHESIS -> CHANGE/ALTERNATIVE -> TEST/CHECK -> OBSERVE' in step8_spec
assert 'KEEP | REVISE | DISCARD | INCONCLUSIVE' in step8_spec
step8_scope = scope_text.split('STEP 8 -', 1)[1].split('STEP 9 -', 1)[0]
assert 'Status: DESIGNED' in step8_scope
assert 'optional' in step8_scope.lower()
assert 'no fixed worker-count or delegation-depth limit' in step8_scope
assert '2–5' in step8_scope
assert 'Bounded worker delegation (one simple depth/worker cap is enough)' not in step8_scope
assert 'Deep worker hierarchies.' not in step8_scope
part7_text = (root / 'docs/PART_7_MEMBER_SCHEDULING_RECOVERY_RESOURCES.md').read_text(encoding='utf-8')
assert '### 14.4 Approved trusted Docker resource monitor' in part7_text
assert 'monitoring **cannot guarantee**' in part7_text
assert '80%' in part7_text and '90%' in part7_text
assert 'Docker Engine' in part7_text
assert '### 7.1 Docker storage and process-restart policy' in part7_text
assert 'Docker restart does not' in step8_spec
assert "Docker's **named volumes**" in step8_scope
assert 'per-worker recovery manager' in step8_scope
assert '## 4.1 Accepted Step 8.2 policy' in step8_spec
assert '## 4.2 Accepted Step 8.2 resource monitoring boundary' in step8_spec
assert '## 4.3 Accepted Step 8.2a — Docker-backed persistence' in step8_spec
assert 'no worker recovery manager' in step8_spec.lower()
assert 'No Council-imposed fixed worker count' in step8_spec
assert 'OOM' in step8_spec
assert 'MemberSandboxOOMObserved' in (root / 'docs/TYPED_INTERACTION_CONTRACTS.md').read_text(encoding='utf-8')
assert 'member_resource_monitor_latest' in (root / 'docs/POSTGRES_DATA_MODEL.md').read_text(encoding='utf-8')

assert 'verified customer-authorized local immutable read-only snapshot export' in (root / 'docs/TYPED_INTERACTION_CONTRACTS.md').read_text(encoding='utf-8')
assert 'the customer-authorized hosted OpenAI Moderation API' in scope_text
assert 'Invoke local open-weight OpenAI Moderation API' not in scope_text
assert 'per-current-checkpoint/review/premortem-generation internal API dispatch queues' not in (root / 'docs/CHECKPOINT_COMMUNICATION_GATEWAY.md').read_text(encoding='utf-8')
assert 'R1. Steps 2/3' in (root / 'docs/STEPS_2_TO_8_CROSS_STEP_RECONCILIATION_2026_10_19.md').read_text(encoding='utf-8')

assert contract['step8']['pending_design'] == []
for relpath in ('STEP_2_SNAPSHOT_TRANSFER_CONTRACT_V1.md','STEPS_3_TO_5_EXACT_INTERFACE_CONTRACT_V1.md','STEP_8_ACTION_AND_FINALIZATION_CONTRACT_V1.md','STEP_2_TO_8_VERIFICATION_MATRIX_V1.md'):
    assert (root / 'docs' / relpath).exists()

print(f'Static specification checks passed: {len(files)} documents and {len(contract["requirements"])} tracked requirements.')
print('Scope: documentation/contract consistency only. Runtime tests and comparative evaluations NOT RUN.')

if contract['scope'] == 'specification_only':
    assert contract['runtime_implementation_status'] == 'NOT_STARTED'
    assert contract['runtime_test_status'] == 'NOT_RUN'
    for item in contract['requirements']:
        assert item['implementation_status'] == 'NOT_STARTED'
        assert item['test_status'] == 'NOT_RUN'
    print('Amendment status checks passed: no runtime requirement marked completed.')
