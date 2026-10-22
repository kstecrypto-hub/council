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
assert contract['step7']['spending_lock_order'] == ['deployment_event_clock', 'funding_owner_provider_account_budget', 'run_budget', 'spend_pool', 'optional_member_phase_budget']
# ADR-53 modifies the previously mandatory BYOK and per-member-per-phase hard cap defaults.
assert contract['step7']['requires_approved_user_budget'] is False
assert contract['step7']['requires_approved_funding_owner_budget'] is True
assert contract['step7']['operator_funded_pilot_default'] is True
assert contract['step7']['optional_user_byok'] is True
assert contract['step7']['user_approves_run_and_phase_token_and_cost_limits'] is False
assert contract['step7']['funding_owner_approves_run_account_and_five_protected_pool_spend_limits'] is True
assert contract['step7']['optional_hard_member_phase_token_cost_limits'] is True
assert contract['phase_budget_policy']['per_member_per_phase_token_ceiling_required'] is False
assert contract['phase_budget_policy']['per_member_per_phase_cost_ceiling_required'] is False
assert contract['phase_budget_policy']['optional_member_phase_token_ceiling_allowed'] is True
assert contract['phase_budget_policy']['optional_member_phase_cost_ceiling_allowed'] is True
assert contract['phase_budget_policy']['adaptive_member_phase_shares_within_authorized_pool'] is True
assert contract['phase_budget_policy']['five_protected_spend_pools_and_funded_run_account_exposure_required'] is True
assert contract['phase_budget_policy']['extension_or_cross_pool_transfer_requires_funding_owner_authorization'] is True

assert 'suggested_default_budget_allocation_percent' not in contract['step7']
assert contract['step7']['budget_allocation_policy'] == 'PROJECT_SPECIFIC_FIVE_PROTECTED_FUNDED_SCOPES_ADAPTIVE_WITHIN_POOL_OPERATOR_OR_USER_APPROVAL_NO_UNIVERSAL_PERCENTAGES'
assert contract['final_product_policy']['final_user_acceptance_target'] == 'EXACT_CURRENT_INTEGRATED_ARTIFACT_AND_FROZEN_REPORT_PACKAGE_NOT_ORIGINAL_MEMBER_CANDIDATE'
assert contract['step8']['step8_5cd']['queue_policy']['additional_api_per_key_lanes_required'] is False
assert contract['step7']['initial_remote_model_call_cap_per_provider'] == 2
assert contract['step7']['initial_local_inference_concurrency_cap'] == 1
assert contract['step7']['default_recovery_retries'] == 3
assert 'sealed_review' in contract['checkpoint_phases']
assert set(contract['done_requires']) == {'checkpoint_generation', 'processed_message_sequence', 'expected_obligation_version'}
assert len(contract['separate_outcomes']) == 4
assert contract['event_ordering'] == 'deployment_transactional_event_clock'
assert contract['long_term_learning_store'] == 'customer_owned_native_local_git_archive_with_optional_permitted_general_knowledge'
assert contract['council_runtime_git_backend'] == 'CUSTOMER_OWNED_NATIVE_LOCAL_GIT_NOT_ONLINE_GITHUB'
assert contract['long_term_archive_rag_backend'] == 'QDRANT_CUSTOMER_CONTROLLED_REBUILDABLE_DERIVED_INDEX_NOT_PGVECTOR'
assert len({x['id'] for x in contract['requirements']}) == len(contract['requirements'])
assert len(contract['requirements']) >= 18
assert {'ADR-13', 'ADR-14', 'ADR-15', 'ADR-16', 'ADR-17', 'ADR-18'} <= {x['id'] for x in contract['requirements']}
assert contract['requirements'][0]['design_status'] == 'SUPERSEDED_BY_ADR_17'
assert contract['step11']['negative_exclusion_policy'] == 'no_universal_blacklist_or_silent_filter_based_on_prior_failure'
# Documentation contract guards only; Council agent memory/recovery remains unimplemented.
assert contract['step10']['design_status'] == 'MVP_HANDOFF_APPROVED_ADR54_IMPLEMENTATION_DETAILS_DELEGATED'
assert contract['step10']['network_policy'] == 'DENY_DIRECT_AGENT_EXTERNAL_EGRESS_ALLOW_ONLY_SCOPED_INTERNAL_TOOL_BRIDGE'
assert contract['step10']['runtime_implementation_status'] == 'NOT_STARTED'
assert contract['step10']['runtime_tests_status'] == 'NOT_RUN'
assert contract['step11']['design_status'] == 'MVP_HANDOFF_APPROVED_ADR54_IMPLEMENTATION_DETAILS_DELEGATED'
assert contract['step11']['long_term_rag_index'].startswith('QDRANT_')
assert contract['step11']['pgvector_for_rag'] is False
assert contract['step11']['online_github_for_runtime_agent_repos_checkpoints_or_archive'] is False
assert contract['step11']['continuation_preserves_same_original_logical_member'] is True
assert contract['step11']['continuation_packet_is_canonical_external_effect_authority'] is False
assert contract['step11']['new_memory_or_recovery_service_required'] is False
assert contract['step11']['separate_graph_or_vector_db_required_for_cooldown_continuation'] is False
assert contract['step11']['mcp_cooldown_agent_busy_wait_required'] is False
assert contract['step11']['private_branch_memory_leakage_allowed'] is False
assert contract['step11']['runtime_implementation_status'] == 'NOT_STARTED'
assert contract['step11']['runtime_tests_status'] == 'NOT_RUN'
# ADR-50 is specification-only; verify minimal ontology and no per-call LLM memory work.
assert contract['step11']['immediate_logging_policy'] == 'ADR-50_OPERATIONS_INTENT_BEFORE_DISPATCH_OBSERVATIONS_ON_RECEIPT_GRAPH_ESSENTIAL_EDGES_WITH_MATERIAL_FINDING'
assert contract['step11']['minimal_ontology_reuses_existing_canonical_records'] is True
assert set(contract['step11']['minimal_ontology_reference_types']) == {'Actor', 'Operation', 'Observation', 'Artifact', 'Finding', 'Hypothesis'}
assert contract['step11']['mechanical_graph_origin'] == 'RUNTIME_TRUSTED_OBSERVATIONS'
assert contract['step11']['semantic_graph_origin'] == 'AGENT_INTERPRETATION_WITH_SOURCE_LINKED_EVIDENCE'
assert contract['step11']['semantic_graph_findings_required_for_every_tool_call'] is False
assert contract['step11']['model_inference_required_for_operational_logging'] is False
assert contract['step11']['second_model_memory_summary_after_each_tool_call_required'] is False
assert contract['step11']['working_memory_compaction_after_each_tool_call_required'] is False
assert contract['step11']['graph_retrieval_after_each_tool_call_required'] is False
assert contract['step11']['essential_graph_relationships_saved_atomically_with_canonical_finding'] is True
assert contract['step11']['graph_search_projections_may_lag_with_freshness_watermark_and_canonical_fallback'] is True

assert contract['step8']['design_status'] == 'IN_DESIGN'
assert contract['step8']['runtime_implementation_status'] == 'NOT_STARTED'
assert contract['step8']['runtime_tests_status'] == 'NOT_RUN'
assert contract['step8']['core_evidence_feedback_optional'] is False
assert contract['step8']['formal_executable_experiments_optional'] is True
assert contract['step8']['new_strategic_hypothesis_required_per_inner_action'] is False
assert contract['step8']['karpathy_feedback_cycle_is_core'] is True
assert contract['step8']['self_review_required_before_each_normal_checkpoint'] is True
assert contract['step8']['integrator_output_intent_self_check_required'] is True
assert {'ADR-43', 'ADR-44', 'ADR-45', 'ADR-46', 'ADR-47', 'ADR-48', 'ADR-49', 'ADR-50', 'ADR-51', 'ADR-52', 'ADR-53', 'ADR-54'} <= {r['id'] for r in contract['requirements']}
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
assert '**Design status:** IN DESIGN' in step8_spec
assert 'HYPOTHESIS -> CHANGE/ALTERNATIVE -> TEST/CHECK -> OBSERVE' in step8_spec
assert 'KEEP | REVISE | DISCARD | INCONCLUSIVE' in step8_spec
step8_scope = scope_text.split('STEP 8 -', 1)[1].split('STEP 9 -', 1)[0]
assert 'Status: IN DESIGN' in step8_scope
assert 'Status: MVP DESIGN HANDOFF APPROVED' in scope_text.split('STEP 10 -', 1)[1].split('STEP 11 -', 1)[0]
assert 'Status: MVP DESIGN HANDOFF APPROVED' in scope_text.split('STEP 11 -', 1)[1].split('STEP 12 -', 1)[0]
assert 'Qdrant' in (root / 'docs/STEP_10_11_ADR54_MINIMAL_IMPLEMENTATION_HANDOFF_QDRANT.md').read_text()
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
assert 'DeepSeek powers everything initially' not in (root / 'docs/APP_DESIGN.md').read_text(encoding='utf-8')
assert 'DeepSeek is the initial default' not in (root / 'AGENTS.md').read_text(encoding='utf-8')
assert 'all using the selected DeepSeek model' not in (root / 'docs/APP_DESIGN.md').read_text(encoding='utf-8')
assert 'API_QUEUE_IMPLEMENTATION_PENDING' not in (root / 'docs/architecture_contract.json').read_text(encoding='utf-8')
assert 'R1. Steps 2/3' in (root / 'docs/STEPS_2_TO_8_CROSS_STEP_RECONCILIATION_2026_10_19.md').read_text(encoding='utf-8')

assert set(contract['step8']['pending_design']) == {'ADR43_FEEDBACK_CYCLE_RUNTIME_PROMPT_AND_COMMAND_BINDING', 'ADR43_MATERIAL_APPROACH_EVIDENCE_COVERAGE_AND_UNTESTABLE_CLAIM_HANDLING', 'ADR44_EXACT_DTO_SELF_REVIEW_VERSION_INVALIDATION_AND_UI_PRESENTATION'}
for relpath in ('STEP_2_SNAPSHOT_TRANSFER_CONTRACT_V1.md','STEPS_3_TO_5_EXACT_INTERFACE_CONTRACT_V1.md','STEP_8_ACTION_AND_FINALIZATION_CONTRACT_V1.md','STEP_2_TO_8_VERIFICATION_MATRIX_V1.md','STEP_9_ADR47_OPEN_ENDED_PEER_MODEL_SELECTION.md','STEP_9_ADR51_LIGHTWEIGHT_MODEL_TOOL_COMPATIBILITY_PROBE.md','STEP_9_ADR52_PROVIDER_INTERRUPTION_CONTEXT_RECONSTRUCTION.md','STEP_9_ADR53_OPERATOR_BYOK_CREDENTIALS_MCP_EGRESS_ADAPTIVE_SPENDING.md'):
    assert (root / 'docs' / relpath).exists()

step9 = contract['step9']
assert step9['design_status'] == 'IN_DESIGN'
# ADR-51 design-only Step 9.3 probe method; these are static contract checks, NOT executed provider probes.
probe = step9['step9_3_probe_policy']
assert probe['design_status'] == 'OWNER_APPROVED_ADR_51_LIGHTWEIGHT_MODEL_TOOL_PROTOCOL_CHECK_DESIGN_ONLY'
assert probe['harness_location'] == 'EXISTING_TRUSTED_GATEWAY_NO_EXTRA_SERVICE'
assert probe['tool_kind'] == 'SYNTHETIC_FAKE_ECHO_AND_FAKE_FAILED_RESULT'
assert probe['valid_native_structured_call_required'] is True
assert probe['provider_native_tool_call_id_and_result_continuation_required'] is True
assert probe['unseen_result_nonce_echo_required'] is True
assert probe['fake_failure_continuation_required'] is True
assert probe['deterministic_validation_no_judge_llm'] is True
assert probe['uses_live_mcp_or_real_external_effect'] is False
assert probe['probe_before_every_tool_call_required'] is False
assert probe['run_on_model_configuration_and_relevant_version_change'] is True
assert probe['local_model_runtime_quantization_template_parser_version_bound'] is True
assert probe['versioned_existing_registry_evidence_required'] is True
assert probe['provider_timeout_may_be_inconclusive'] is True
assert probe['charge_actual_model_probe_inference_to_authorized_budget'] is True
assert probe['intelligence_or_task_complexity_gate_allowed'] is False
assert probe['new_external_sandbox_permission_layer_required'] is False
assert probe['sandbox_local_intellectual_autonomy_preserved'] is True
assert probe['runtime_implementation_status'] == 'NOT_STARTED'
assert probe['runtime_tests_status'] == 'NOT_RUN'
# ADR-52 generic provider-session interruption and same-member context reconstruction, specification-only.
interrupted = step9['provider_interruption_recovery']
assert interrupted['design_status'] == 'OWNER_APPROVED_ADR_52_SAME_MEMBER_COMPACTED_MEMORY_GRAPH_LEDGER_RESUME_DESIGN_ONLY'
assert interrupted['restore_same_logical_member_and_original_strategy'] is True
assert interrupted['notify_model_previous_provider_connection_interrupted'] is True
assert interrupted['canonical_operations_permissions_budgets_checked_before_context_or_dispatch'] is True
assert interrupted['recovery_context'] == [
    'LATEST_PERMITTED_PERSISTED_COMPACTED_WORKING_MEMORY',
    'FRESH_RELEVANT_AUTHORIZED_GRAPH_EVIDENCE_SINCE_COMPACTION',
    'CURRENT_STEP5_STEP7_CANONICAL_OPERATION_STATUS_AND_OBSERVED_RESULTS',
]
assert interrupted['valid_same_profile_native_provider_session_continuation_allowed'] is True
assert interrupted['otherwise_start_fresh_bounded_same_model_profile_session'] is True
assert interrupted['auto_switch_provider_on_connection_drop'] is False
assert interrupted['reexecute_confirmed_completed_tools'] is False
assert interrupted['autodispatch_undispatched_tool_proposals'] is False
assert interrupted['unknown_external_effects_require_reconciliation'] is True
assert interrupted['mcp_3_to_7_minute_cooldown_applies_to_all_provider_interruptions'] is False
assert interrupted['no_new_recovery_queue_agent_or_service'] is True
assert interrupted['forced_per_tool_context_refresh_or_compaction'] is False
assert interrupted['routine_user_interaction_required'] is False
assert interrupted['runtime_implementation_status'] == 'NOT_STARTED'
assert interrupted['runtime_tests_status'] == 'NOT_RUN'


# ADR-53 specification guards only — not executed credential or network security tests.
assert step9['remote_inference_billing'] == 'OPERATOR_FUNDED_PILOT_DEFAULT_OR_OPTIONAL_USER_BYOK_ACTUAL_PROVIDER_ACCOUNT_OWNER_BILLED_NO_PREPAID_RESELLER_WALLET'
assert step9['operator_credential_default_pilot'] is True
assert step9['user_byok_supported_optional'] is True
assert step9['automatic_fallback_to_other_funding_owner_key'] is False
assert step9['n8n_code_snippet_copied_without_license_clearance'] is False
assert step9['agent_external_tool_path'] == 'APPROVED_MCP_VIA_EXISTING_TRUSTED_BROKER'
assert step9['model_inference_path'] == 'NATIVE_TRUSTED_PROVIDER_GATEWAY_NOT_MCP_REQUIRED'
assert step9['trusted_internal_host_and_snapshot_ops_use_native_contracts'] is True
assert step9['sandbox_direct_external_network_egress_allowed'] is False
assert step9['sandbox_network_boundary_enforcement_step10_status'] == 'IN_DESIGN_NOT_IMPLEMENTED_OR_TESTED'
assert step9['funded_account_run_and_five_protected_pool_hard_exposure_required'] is True
assert step9['automatic_member_phase_share_reallocation_within_authorized_pool'] is True
assert step9['mandatory_member_phase_hard_token_cost_caps'] is False
assert step9['price_or_success_guarantee_from_token_estimate'] is False
assert step9['no_wallet_reseller_in_mvp'] is True
assert step9['per_model_mcp_server_required'] is False
assert step9['direct_model_to_mcp_bypass'] is False
assert step9['auto_fallback'].startswith('DISABLED')
assert step9['example_nonexclusive_provider_adapter_families'] == ['OpenAI', 'Anthropic', 'DeepSeek']
assert step9['no_main_reasoning_model'] is True
assert step9['distinct_qualified_models_per_original_seat_by_default'] is True
assert step9['same_model_control_requires_explicit_user_choice'] is True
assert step9['unrestricted_catalog_entry_count_by_architecture'] is True
assert step9['maximum_supported_model_count'] is None
assert step9['initial_remote_provider_concurrency_cap'] == contract['step7']['initial_remote_model_call_cap_per_provider']
assert step9['initial_shared_local_inference_concurrency_cap'] == contract['step7']['initial_local_inference_concurrency_cap']
assert {'ADR-41', 'ADR-42'} <= {x['id'] for x in contract['requirements']}
assert all(x['implementation_status'] == 'NOT_STARTED' and x['test_status'] == 'NOT_RUN' for x in contract['requirements'] if x['id'] in {'ADR-41', 'ADR-42', 'ADR-45', 'ADR-46', 'ADR-47'})
step9_scope = scope_text.split('STEP 9 -', 1)[1].split('STEP 10 -', 1)[0]
assert 'Status: IN DESIGN' in step9_scope
assert 'Council-managed tool broker/MCP client layer shared by all models' in step9_scope
step9_doc = (root / 'docs' / 'STEP_9_PROVIDER_ADAPTER_AND_SHARED_MCP_CONTRACT_V1.md').read_text(encoding='utf-8')
for phrase in ('NO PER-MODEL MCP SERVER IS REQUIRED', 'NO PER-MODEL MCP SERVER', 'ModelRequestV1', 'ExposedToolManifestV1', 'NOT RUN'):
    assert phrase in step9_doc, phrase

# Current-authority consistency guards: these do not execute a Council application.
guide_path = root / 'docs' / 'CURRENT_SPEC.md'
guide = guide_path.read_text(encoding='utf-8')
agents_text = (root / 'AGENTS.md').read_text(encoding='utf-8')
handoff_text = (root / 'docs' / 'IMPLEMENTATION_HANDOFF.md').read_text(encoding='utf-8')
blueprint_text = (root / 'docs' / 'STEP_8_5_STRUCTURED_COUNCIL_BLUEPRINT_HANDOFF.md').read_text(encoding='utf-8')
typed_text = (root / 'docs' / 'TYPED_INTERACTION_CONTRACTS.md').read_text(encoding='utf-8')
assert contract['current_specification_guide'] == 'docs/CURRENT_SPEC.md'
assert contract['mvp_inference_billing']['operator_funded_pilot_default'] is True
assert contract['mvp_inference_billing']['user_byok_optional'] is True
assert contract['mvp_inference_billing']['funding_owner_approves_account_run_and_five_protected_pools'] is True
assert contract['mvp_inference_billing']['mandatory_member_phase_hard_caps'] is False
assert contract['mvp_inference_billing']['user_approved_run_phase_token_cost_budgets'] is False
assert 'ADR-53' in guide and 'ADR-40' in guide and 'NOT STARTED' in guide
assert 'docs/CURRENT_SPEC.md' in agents_text
assert 'Propose, but never impose without approval, the configurable 70/25/5 budget split' not in agents_text
assert 'Bring Your Own API Key or compatible local inference is the MVP' not in agents_text
assert 'MVP requires **BYOK for all remote providers**' not in handoff_text
assert 'approved full public-history manifests' not in handoff_text
assert 'full repo-public and failed-private transitions' not in handoff_text
assert "The owner's **small keyed internal API queues** serialize" not in blueprint_text
assert 'incrementally decode UTF-8' in typed_text
assert 'streaming and non-streaming API delivery modes' in typed_text

print(f'Static specification checks passed: {len(files)} documents and {len(contract["requirements"])} tracked requirements.')
print('Scope: documentation/contract consistency only. Runtime tests and comparative evaluations NOT RUN.')

if contract['scope'] == 'specification_only':
    assert contract['runtime_implementation_status'] == 'NOT_STARTED'
    assert contract['runtime_test_status'] == 'NOT_RUN'
    for item in contract['requirements']:
        assert item['implementation_status'] == 'NOT_STARTED'
        assert item['test_status'] == 'NOT_RUN'
    print('Amendment status checks passed: no runtime requirement marked completed.')
