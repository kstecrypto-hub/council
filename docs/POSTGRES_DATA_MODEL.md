# PostgreSQL data model

**October 13, 2026 amendment:** [decision/status index](ARCHITECTURE_DECISIONS.md). Requirements below are specifications; application implementation is NOT STARTED and runtime tests are NOT RUN.

**Status:** approved design model for Part 3; this document defines persistence boundaries and invariants, not executable migrations.  
**Authority:** this document refines section 13 of [APP_DESIGN.md](APP_DESIGN.md). If they conflict, the latest explicit owner instruction and APP_DESIGN remain authoritative.

## 1. Database layout

Each active Council deployment gets its own isolated PostgreSQL instance **inside that deployment's trusted sandbox boundary**. It is not a host-global database shared by unrelated Council deployments, and individual agent sandboxes never receive direct database authority.

Use two logical schemas:

- `council_core` - canonical project/run state, contracts, agents, checkpoints, evidence/provenance, candidates, environments, approvals, continuity records, and audit events for the lifetime of that Council project.
- `council_runtime` - mutable operational state such as queues, leases, attempts, scheduler reservations, live sandbox instances, broker requests, and transient execution state.

The PostgreSQL instance is **project-lifetime control infrastructure**, not the long-term learning store. It may use a persistent volume so crashes/restarts do not destroy an active project, but after user acceptance and successful export of the retained project/learning artifacts, the Council PostgreSQL volume is deleted with the rest of the Council runtime.

Long-term reuse of accepted work is Git-backed and is described in section 13.

Use application-generated UUIDs for canonical identities, `timestamptz` for timestamps, explicit version numbers for versioned aggregates, and a monotonically increasing `bigint` event position for ordered audit/projection processing.

## 2. Root project and contract model

### council_core.workspaces
- `id` PK
- `name`
- `created_at`

### council_core.projects
- `id` PK
- `workspace_id` FK
- `name`
- `status`
- `created_at`
- `closed_at`

### council_core.project_contracts
Stable identity for the user's canonical specification.
- `id` PK
- `project_id` FK UNIQUE
- `created_at`

### council_core.project_contract_revisions
Immutable.
- `id` PK
- `contract_id` FK
- `revision_no`
- `supersedes_revision_id` nullable FK
- `body_json`
- `content_hash`
- `change_reason`
- `created_by_actor_type`
- `created_by_actor_id`
- `created_at`
- UNIQUE(`contract_id`, `revision_no`)

### council_core.project_contract_approvals
Immutable user decision for one exact contract revision.
- `id` PK
- `contract_revision_id` FK
- `user_id`
- `decision` = APPROVED | CHANGES_REQUESTED | CURRENT_APPROACH_REJECTED | PROJECT_CANCELLED
- `interaction_request_id` FK
- `decided_at`
- `note`

A run cannot start from a revision without an APPROVED record. Requested changes and rejected approaches never mutate the old revision; they causally produce a later immutable revision when the project continues.

### council_core.interaction_requests
Durable user-decision/clarification request. A blocking UI prompt is a projection of this record, not a side effect of an activity label.
- `id` PK
- `project_id` FK
- `run_id` nullable FK
- `branch_id` nullable FK
- `type`
- `schema_version`
- `target_type`
- `target_id`
- `target_version` nullable
- `target_hash` nullable
- `title`
- `summary`
- `payload_json`
- `allowed_action_codes_json`
- `blocking_scope`
- `priority`
- `status` = OPEN | PRESENTED | ANSWERED | STALE | CANCELLED
- `created_event_id` FK
- `presented_at` nullable
- `resolved_event_id` nullable FK
- `resolved_at` nullable
- `stale_reason` nullable
- `created_at`

At most one active interaction request may represent the same semantic gate/target revision. Replayed delivery must not create another request.

### council_core.interaction_responses
Immutable user response to one durable interaction request.
- `id` PK
- `interaction_request_id` FK
- `actor_id`
- `action_code`
- `payload_json`
- `expected_target_version` nullable
- `expected_target_hash` nullable
- `idempotency_key`
- `submitted_at`
- UNIQUE(`interaction_request_id`, `idempotency_key`)

Interaction responses do not replace domain-specific canonical records. The response plus the domain decision it authorizes must be committed coherently.

### council_core.instruction_packages
Immutable prompt/instruction package generated from an approved contract revision.
- `id` PK
- `contract_revision_id` FK
- `content_json`
- `content_hash`
- `generated_at`

The package states requirements, permissions, acceptance criteria, definition of done, and communication rules. It must not add an implementation choice that the Project Contract did not require.

### council_core.runs
- `id` PK
- `project_id` FK
- `launch_contract_revision_id` FK
- `instruction_package_id` FK
- `environment_mode` = COUNCIL_MANAGED | MATCH_HOST | CUSTOM
- `status`
- `created_at`
- `started_at`
- `finished_at`

`launch_contract_revision_id` is immutable. Mid-run changes do not rewrite it.

### council_core.run_contract_revisions
Records which later contract revisions became effective for a run.
- `run_id` FK
- `contract_revision_id` FK
- `effective_event_id` FK
- `effective_at`
- PK(`run_id`, `contract_revision_id`)

### council_core.contract_deliveries
Records exactly which branch received which canonical revision.
- `run_id` FK
- `contract_revision_id` FK
- `logical_agent_id` FK
- `delivered_at`
- `acknowledged_at`
- UNIQUE(`run_id`, `contract_revision_id`, `logical_agent_id`)

This makes it possible to reconstruct exactly what an agent was authorized and instructed to build at a given time.

## 3. Council, branches, and sessions

### council_core.council_seats
- `id` PK
- `run_id` FK
- `seat_no`
- `model_profile_version_id`
- UNIQUE(`run_id`, `seat_no`)

### council_core.branches
- `id` PK
- `run_id` FK
- `owner_agent_id` nullable until agent creation completes
- `state`
- `created_at`

### council_core.logical_agents
Persistent logical identity across model sessions.
- `id` PK
- `run_id` FK
- `branch_id` FK
- `seat_id` nullable FK
- `parent_agent_id` nullable FK
- `agent_kind` = COUNCIL_MEMBER | WORKER
- `created_at`
- `ended_at`

### council_core.agent_sessions
Immutable session identity plus lifecycle timestamps.
- `id` PK
- `logical_agent_id` FK
- `session_no`
- `provider_profile_version_id`
- `model_profile_version_id`
- `started_at`
- `ended_at`
- `end_reason`
- UNIQUE(`logical_agent_id`, `session_no`)

A new session is a continuation of the same logical agent, not a new independent reviewer.

## 4. Checkpoint and branch-visibility model

### council_core.checkpoint_policies
Stable identity for a run's checkpoint policy.
- `id` PK
- `run_id` FK

### council_core.checkpoint_policy_versions
Immutable.
- `id` PK
- `checkpoint_policy_id` FK
- `version_no`
- `contract_revision_id` FK
- `reason`
- `created_at`
- UNIQUE(`checkpoint_policy_id`, `version_no`)

### council_core.checkpoint_definitions
Immutable definitions belonging to a policy version.
- `id` PK
- `policy_version_id` FK
- `checkpoint_key`
- `sequence_hint`
- `trigger_type`
- `trigger_json`
- `publication_scope_json`
- `communication_scope_json`
- `required_outputs_json`
- `completion_condition_json`
- `post_checkpoint_state`
- UNIQUE(`policy_version_id`, `checkpoint_key`)

### council_core.checkpoint_definition_participants
- `checkpoint_definition_id` FK
- `branch_id` FK
- PK(`checkpoint_definition_id`, `branch_id`)

### council_core.checkpoint_instances
- `id` PK
- `run_id` FK
- `checkpoint_definition_id` nullable FK
- `policy_version_id` FK
- `is_adaptive`
- `adaptive_reason`
- `status`
- `opened_at`
- `closed_at`

### council_core.publications
Immutable publication event from one branch at one checkpoint.
- `id` PK
- `checkpoint_instance_id` FK
- `publisher_branch_id` FK
- `publication_type`
- `summary`
- `created_at`

### council_core.publication_items
Immutable list of exactly what was exposed.
- `id` PK
- `publication_id` FK
- `item_kind`
- `canonical_ref_type`
- `canonical_ref_id`
- `artifact_id` nullable FK
- `metadata_json`

### council_core.publication_deliveries
- `publication_id` FK
- `recipient_branch_id` FK
- `delivered_at`
- `acknowledged_at`
- PK(`publication_id`, `recipient_branch_id`)

### council_core.structured_escalations
Immutable agent-to-orchestrator escalation.
- `id` PK
- `run_id` FK
- `branch_id` FK
- `logical_agent_id` FK
- `type` = REQUIREMENT_CLARIFICATION | BLOCKED | EXTERNAL_CONSTRAINT_DISCOVERED | INTERFACE_DECISION_REQUIRED | CHECKPOINT_REQUEST | IMPLEMENTATION_COMPLETE | other versioned enum value
- `payload_json`
- `created_at`
- `resolved_event_id` nullable FK

### Visibility invariant

Every branch-private canonical row that can contain unpublished intellectual work carries:
- `run_id`
- `branch_id`
- `visibility_class` = PRIVATE | PUBLISHED | GLOBAL

Agents never connect directly to PostgreSQL. The backend Capability Gateway is the first enforcement layer. PostgreSQL row-level security is the second enforcement layer for branch-scoped canonical tables.

A branch may read a row when:
1. the row belongs to that branch; or
2. it is GLOBAL for that run; or
3. a checkpoint publication item referencing that row has a delivery to that branch.

The backend sets transaction-local run/branch identity before executing branch-scoped queries. RLS must not infer publication from timestamps or checkpoint status alone; an explicit publication + delivery record is required.

Returning to isolation after a checkpoint does not revoke already delivered information. It prevents access to additional unpublished branch state.

## 5. Candidate, repository, and acceptance model

### council_core.candidate_solutions
- `id` PK
- `run_id` FK
- `branch_id` FK
- `status`
- `created_at`
- `completed_at`

### council_core.repositories
- `id` PK
- `candidate_solution_id` FK
- `provider`
- `repository_ref`
- `repository_url`
- `created_at`
- `archived_at`

### council_core.repository_revisions
Immutable observed commits.
- `id` PK
- `repository_id` FK
- `commit_sha`
- `commit_url`
- `observed_at`
- UNIQUE(`repository_id`, `commit_sha`)

### council_core.candidate_snapshots
Immutable candidate checkpoints.
- `id` PK
- `candidate_solution_id` FK
- `snapshot_no`
- `repository_revision_id` FK
- `environment_definition_version_id` nullable FK
- `created_at`
- UNIQUE(`candidate_solution_id`, `snapshot_no`)

### council_core.acceptance_decisions
Immutable user decision.
- `id` PK
- `run_id` FK
- `candidate_snapshot_id` FK
- `decision` = ACCEPTED | REJECTED | REVISION_REQUIRED
- `decided_at`
- `note`

Only an ACCEPTED candidate snapshot is retained as an accepted deliverable in the Git-backed archive. Failed approaches may be retained as attributed lessons; acceptance is not evidence of general validity.

## 6. Environment model

### council_core.environment_definitions
Stable candidate environment identity.
- `id` PK
- `candidate_solution_id` FK
- `mode` = COUNCIL_MANAGED | MATCH_HOST | CUSTOM

### council_core.environment_definition_versions
Immutable reproducible environment definitions.
- `id` PK
- `environment_definition_id` FK
- `version_no`
- `manifest_json`
- `definition_artifact_id` nullable FK
- `content_hash`
- `created_at`
- UNIQUE(`environment_definition_id`, `version_no`)

### council_core.host_profiles
Stable Match My PC profile identity.
- `id` PK
- `project_id` FK

### council_core.host_profile_versions
Immutable sanitized snapshots.
- `id` PK
- `host_profile_id` FK
- `version_no`
- `profile_hash`
- `captured_at`
- `scope_json`
- UNIQUE(`host_profile_id`, `version_no`)

### council_core.host_capabilities
- `id` PK
- `host_profile_version_id` FK
- `capability_key`
- `observed_value_json`
- `sensitivity_class`
- `captured_at`

No secret value belongs in this table.

### council_core.environment_contracts
Stable identity for Match My PC execution requirements.
- `id` PK
- `run_id` FK

### council_core.environment_contract_versions
Immutable.
- `id` PK
- `environment_contract_id` FK
- `version_no`
- `host_profile_version_id` FK
- `contract_revision_id` FK
- `created_at`
- UNIQUE(`environment_contract_id`, `version_no`)

### council_core.environment_contract_capabilities
- `id` PK
- `environment_contract_version_id` FK
- `capability_key`
- `status` = EXACT | COMPATIBLE | BRIDGED | UNAVAILABLE
- `required_value_json`
- `actual_value_json`
- `bridge_kind` nullable
- `limitation` nullable

### council_core.environment_contract_approvals
- `id` PK
- `environment_contract_version_id` FK
- `user_id`
- `decision`
- `decided_at`

### council_core.privileged_broker_grants
Immutable scoped approval.
- `id` PK
- `run_id` FK
- `environment_contract_version_id` FK
- `capability_name`
- `scope_json`
- `approved_by_user_id`
- `approved_at`
- `expires_at` nullable

### council_core.host_mutation_authorizations
Separate from Match My PC inspection/bridging.
- `id` PK
- `run_id` FK
- `requested_operation_json`
- `approved_scope_json`
- `approved_by_user_id`
- `approved_at`
- `expires_at` nullable
- `cleanup_plan_json`
- `status`

### council_core.host_drift_events
- `id` PK
- `run_id` FK
- `old_host_profile_version_id` FK
- `new_host_profile_version_id` FK
- `affected_capabilities_json`
- `detected_at`

A drift event invalidates affected exact-match verification until revalidated.

### council_core.rebuild_verifications
Immutable.
- `id` PK
- `candidate_snapshot_id` FK
- `environment_definition_version_id` FK
- `environment_contract_version_id` nullable FK
- `status`
- `verification_artifact_id` nullable FK
- `started_at`
- `finished_at`

An executable candidate cannot be marked reproducible without a successful clean rebuild verification.

## 7. Evidence, analysis, and graph records

The authoritative product behavior for evidence/provenance is [PART_6_EVIDENCE_PROVENANCE_GRAPH.md](PART_6_EVIDENCE_PROVENANCE_GRAPH.md).

The canonical investigation ledger remains normalized rather than storing the whole graph as one JSON document.

Required canonical tables include:
- `sources`
- `source_versions`
- `evidence_items`
- `assumptions`
- `analysis_steps`
- `claims`
- `claim_versions`
- `support_groups`
- `support_group_members`
- `challenges`
- `challenge_responses`
- `revisions`
- `coverage_items`

### council_core.graph_relationships
Projection edge over canonical records.
- `id` PK
- `run_id` FK
- `from_ref_type`
- `from_ref_id`
- `relationship_type`
- `to_ref_type`
- `to_ref_id`
- `origin` = RUNTIME | AGENT_INTERPRETATION
- `author_agent_id` nullable FK
- `justification_ref_id` nullable
- `review_status`
- `created_at`

The graph is a projection of canonical records. It may not become an independent source of truth.

## 8. Continuity and agent-memory storage hooks

The persistence layer already supports **continuity memory**, but the exact memory-selection policy is intentionally deferred to the context/memory design step.

### council_core.context_manifests
Immutable record of what a session was given.
- `id` PK
- `run_id` FK
- `logical_agent_id` FK
- `agent_session_id` FK
- `reason`
- `token_budget`
- `created_at`

### council_core.context_manifest_items
- `context_manifest_id` FK
- `item_type`
- `canonical_ref_id`
- `rank`
- `mandatory`
- `selection_reason`
- PK(`context_manifest_id`, `item_type`, `canonical_ref_id`)

### council_core.continuation_packets
Immutable bounded handover between sessions of the same logical agent.
- `id` PK
- `logical_agent_id` FK
- `from_session_id` FK
- `to_session_id` FK
- `context_manifest_id` FK
- `handover_text`
- `created_at`

### council_core.agent_state_snapshots
Non-authoritative recovery projection.
- `id` PK
- `logical_agent_id` FK
- `sequence_no`
- `state_json`
- `source_event_position`
- `created_at`
- UNIQUE(`logical_agent_id`, `sequence_no`)

Do **not** create a generic free-form `agent_memory_blob` as an alternate source of truth. Long-term agent continuity must resolve back to canonical tasks, claims, evidence, publications, contract revisions, and events. The later memory/context step will define what gets selected, summarized, ranked, decayed, or carried across projects.

## 9. Audit and ordering

### council_core.events
Append-only.
- `event_position` BIGINT PK, deployment-local committed order allocated by the transactional event clock, not a PostgreSQL sequence
- `event_id` UUID UNIQUE
- `run_id` nullable FK
- `project_id` FK
- `actor_type`
- `actor_id`
- `event_type`
- `payload_json`
- `created_at`

### council_core.projection_offsets
Mutable.
- `projection_name` PK
- `last_event_position`
- `updated_at`

A transaction that changes canonical state also writes the essential audit event and relationship changes required to explain that state.

## 10. Runtime schema

### council_runtime.entity_activity
Mutable/rebuildable projection used by UI and scheduler observability. Durable events remain the history/source for reconstruction.
- `entity_type`
- `entity_id`
- `project_id` FK
- `run_id` nullable FK
- `lifecycle_state`
- `activity_code`
- `detail_schema_version`
- `detail_json`
- `source_event_id` FK
- `updated_at`
- PK(`entity_type`, `entity_id`)

Activity labels never grant permissions or expose unpublished data. The Part 4 State Contract registry defines legal activity codes/transitions and any associated interaction type.


The runtime schema is disposable operational machinery. It must be reconstructable or safely reconciled from canonical state plus external-system truth.

### council_runtime.tasks
- `id` PK
- `run_id` FK
- `branch_id` FK
- `logical_agent_id` FK
- `objective`
- `status`
- `priority`
- `available_at`
- `row_version`
- `created_at`
- `updated_at`

### council_runtime.task_dependencies
- `task_id` FK
- `depends_on_task_id` FK
- PK(`task_id`, `depends_on_task_id`)

### council_runtime.task_leases
- `task_id` PK/FK
- `lease_owner`
- `attempt_no`
- `leased_at`
- `heartbeat_at`
- `expires_at`

### council_runtime.operations
- `id` PK
- `run_id` FK
- `task_id` nullable FK
- `operation_kind`
- `idempotency_key`
- `status`
- `row_version`
- `requested_at`
- `updated_at`
- UNIQUE(`run_id`, `idempotency_key`)

### council_runtime.operation_attempts
Immutable attempt history.
- `id` PK
- `operation_id` FK
- `attempt_no`
- `status`
- `started_at`
- `finished_at`
- `result_artifact_id` nullable
- UNIQUE(`operation_id`, `attempt_no`)

### council_runtime.scheduler_reservations
- `id` PK
- `run_id` FK
- `operation_id` nullable FK
- `resource_kind`
- `amount`
- `status`
- `reserved_at`
- `expires_at`

### council_runtime.sandbox_instances
- `id` PK
- `candidate_solution_id` FK
- `backend_kind`
- `external_instance_ref`
- `status`
- `resource_limits_json`
- `created_at`
- `destroyed_at`

### council_runtime.broker_requests
- `id` PK
- `run_id` FK
- `grant_id` nullable FK
- `mutation_authorization_id` nullable FK
- `operation_type`
- `parameters_json`
- `status`
- `requested_at`
- `completed_at`

### council_runtime.model_calls
- `id` PK
- `run_id` FK
- `logical_agent_id` FK
- `agent_session_id` FK
- `phase_id` / `checkpoint_generation` as applicable
- `operation_id` FK and `usage_reservation_id` FK
- `provider_profile_version_id`
- `model_profile_version_id`
- `pricing_or_local_metering_profile_version_id`
- `execution_epoch`
- `status`
- `input_tokens`
- `cached_input_tokens` (provider-reported subset, not automatically double-counted)
- `output_tokens`
- `cost_amount` nullable (known/settled amount; no UNKNOWN=zero)
- `usage_uncertainty_status`
- `started_at`
- `finished_at`

### council_core.budget_policy_versions (approved run-level budget contract)
- `id` PK, `run_id` FK, `policy_version` monotonic per run
- `contract_revision_id`, `approved_by_user_id`, `approved_at`
- `currency`, `run_cost_ceiling` fixed-precision decimal, `pricing_version_refs`
- `pool_allocations_json` (development, checkpoint_review, orchestration_finalization)
- `member_phase_token_cost_caps_json` (versioned approved per-member/phase/token-unit limits)
- `supersedes_policy_version_id`, `change_reason`
- `initial_proposal_json` (non-authoritative 70/25/5 with equal monetary member shares unless user changes it)

### council_runtime.budget_accounts
- `id` PK, `run_id` FK, `policy_version_id` FK
- `scope_type` = RUN | POOL | MEMBER_PHASE; `pool_kind` = DEVELOPMENT | CHECKPOINT_REVIEW | ORCHESTRATION_FINALIZATION nullable for RUN
- `logical_member_id` nullable, `semantic_phase_id` nullable
- `unit_type` = CURRENCY | TOKENS (explicit provider/model metering unit when tokens)
- `ceiling`, `settled_amount`, `reserved_unsettled_amount`, `row_version`
- Unique active scope per run/policy + pool/member/phase/unit, with nonnegative accounting and enforced ceiling

### council_runtime.usage_reservations
- `id` PK, `operation_id` FK, `attempt_no`, `idempotency_key` / canonical request hash
- `run_id`, `member_id`, `semantic_phase_id`, `worker_parent_id` nullable, `spend_pool`
- `account_refs`, `token_bound`, `cost_bound`, `currency`, `pricing_version_ref`
- `execution_epoch`, `status` = RESERVED | DISPATCHED | SETTLED | RELEASED_UNDISPATCHED | UNKNOWN_PENDING_RECONCILIATION
- `actual_input_output_cached_tokens_json`, `actual_cost` nullable, `settlement_evidence_ref`, `last_reconciled_at`
- Unique logical operation/attempt; a dispatched/unknown record cannot expire into a free reservation

### council_runtime.resource_admissions
- `id` PK, `run_id`, `logical_member_id`, `sandbox_instance_id`, `execution_epoch`
- `requested_and_granted_resource_vector_json` (slots, CPU, RAM, disk, VRAM/device, remote/local model concurrency as applicable)
- `host_capability_snapshot_ref`, `status`, `granted_at`, `confirmed_released_at`
- Resources are not considered available for another sandbox until a trusted backend confirms release

### council_runtime.recovery_attempts
- `id` PK, `run_id`, `logical_member_id`, `operation_id` nullable
- `source_failure_id`, `attempt_number`, `retry_after_at`, `execution_epoch`
- `observed_cleanup_json`, `outcome`, `blocked_reason`, `created_at`
- Initial recovery policy: three retries with default 5s/30s/120s backoff; actual backend timeouts configurable by operation class


### council_runtime.outbox
Used for reliable publication of committed events to SSE/workers.
- `id` BIGINT PK
- `event_id` UUID UNIQUE
- `topic`
- `payload_json`
- `created_at`
- `published_at` nullable

Task leasing uses PostgreSQL row locking with `FOR UPDATE SKIP LOCKED`. Waiting parents do not hold worker slots.

## 11. Mutable versus immutable rule

Immutable/append-only by default:
- Project Contract revisions and approvals
- instruction packages
- contract deliveries
- checkpoint policy versions and definitions
- publications/items/deliveries
- structured escalations
- repository revisions
- candidate snapshots
- Host Profile versions
- Environment Contract versions/capabilities/approvals
- privileged grants and mutation approvals
- rebuild verifications
- source/evidence/claim/challenge/revision versions
- continuation packets/context manifests
- audit events
- operation attempts
- acceptance decisions

Mutable control rows use `row_version` or lease semantics:
- run status
- task status
- operation status
- lease rows
- scheduler reservations
- sandbox instance status
- projection offsets
- current pointers/caches

Never overwrite historical meaning to make current state easier to query.

## 12. Artifact-store boundary

PostgreSQL stores:
- canonical structured data
- small bounded text fields needed for queries
- hashes
- metadata
- provenance
- permissions
- pointers to external artifacts

Versioned artifact storage holds:
- repositories/repository bundles
- container images and exported filesystem layers
- source documents
- binaries
- media
- large raw logs
- test bundles
- large model/tool outputs
- exported reports
- backup bundles

Opaque/unstructured payloads above **256 KiB** should default to artifact storage even if their type is not listed above. Do not index artifact bytes in PostgreSQL.

Every externally stored artifact has a `council_core.artifacts` metadata row:
- `id` PK
- `project_id` FK
- `kind`
- `content_hash`
- `size_bytes`
- `storage_ref`
- `retention_class`
- `created_at`

Artifact references are content-hashed where practical. A database backup without referenced artifacts is not a complete backup.

## 13. Git-backed accepted-project archive

The long-term reuse layer is **not** a permanent PostgreSQL schema.

After the user accepts a project, Council writes a compact reusable archive to Git before destroying the temporary Council runtime database. Git is the durable source for personal reuse and for improving future Council runs.

Retain, at minimum, when available and useful:
- the accepted project/repository or an immutable reference to it;
- final architecture/design notes;
- accepted environment/rebuild definition needed by the project;
- concise capability and stack metadata;
- important approaches that worked;
- important approaches that failed and why;
- material checkpoint conclusions and unresolved caveats worth preserving;
- final acceptance/test results;
- reusable components/patterns;
- relationships to prior accepted projects when one was reused as a base/reference/technique.

Do **not** retain the PostgreSQL control database merely to preserve this information. Raw leases, queue state, runtime sessions, transient checkpoint machinery, caches, and other operational residue are deleted with the Council deployment unless they were deliberately distilled into useful retained project knowledge.

A future Council run may search the Git-backed archive to recognize similar prior projects and use an accepted prior project as a base, reference, technique source, or near-copy where appropriate. Originality is not a requirement.

The exact Git index/file layout is an implementation detail for the later reuse design. The architectural rule is:

> PostgreSQL remembers the active Council run; Git remembers accepted work worth learning from.

## 14. Acceptance, archival, and deletion

1. Freeze the accepted candidate and record the exact user decision.
2. Preserve actual clean-rebuild/acceptance results; do not claim reproducibility without the required successful checks.
3. Export the accepted project, reproducible environment, authorized learning package, and essential provenance/evidence to Git and durable referenced artifact storage.
4. Validate reference closure and restoreability from the retained archive without the temporary control database.
5. Reconcile consequential external effects and unresolved spending/authority operations, retaining the records needed to resolve any still-open obligations.
6. Apply the explicitly authorized repository archival/visibility policy.
7. Only after validation, delete Council's control database/volume, temporary sandboxes, sessions, checkpoint machinery, caches, and credentials. Product-owned databases remain product data.

A user-accepted candidate is eligible for retention, not automatically a validated general rule. Every reusable lesson retains applicable task/environment/version conditions, source and test evidence, limitations, failures/counterexamples, uncertainty, and reassessment triggers. Do not label empirical lessons unconditionally PROVEN. Keep the memory snapshot fixed during a run; independent retrieval must not become live cross-branch communication.

Before deleting the temporary control database, export the accepted project and selected learning/evidence to a durable Git-backed archive. Validate the transitive reference closure from a fresh archive checkout or retained artifact store, with hashes and permissions checked and no dependency on the live Council database, temporary sandbox paths, expiring URLs, or credentials. Essential missing/restricted evidence blocks teardown or requires an explicitly approved archive/retention change that honestly downgrades the unsupported lesson. Do not silently retain forbidden source data or silently delete the only evidence.

Export acceptance/contract history and relevant provenance needed by retained lessons/reports; transient sessions, leases, and caches need not be retained. Archived failed approaches remain distinguishable from accepted candidates. Temporary restore validation and cleanup must be safe to retry. Final archive visibility follows explicit authorization and is not inferred from earlier public checkpoints.

Retention delays remain policy. They do not waive evidence, external-operation reconciliation, or source-access obligations.

## 15. Concurrency and transaction rules

The authoritative transaction/retry contract is [PART_5_TRANSACTIONS_IDEMPOTENCY_CONFLICTS.md](PART_5_TRANSACTIONS_IDEMPOTENCY_CONFLICTS.md).

- Immutable version rows use `UNIQUE(parent_id, version_no)`; concurrent append conflicts re-read current state before a safe retry.
- Mutable control rows update with expected `row_version`; mismatch returns STALE_TARGET, never silent overwrite.
- Retryable commands use scoped idempotency keys plus canonical request hashes.
- Task leasing uses `FOR UPDATE SKIP LOCKED`, explicit expiry/heartbeat, attempt numbers, and lease tokens required for completion.
- External actions use durable logical operations plus append-only attempts. Unknown outcomes remain UNKNOWN_PENDING_RECONCILIATION until reconciled.
- Contract revision activation, checkpoint opening/closing, interaction decisions, claim revisions, and candidate acceptance commit their canonical rows + events + outbox coherently.
- Accepted-project Git archival and Council teardown are external/recoverable operations after acceptance; the temporary control database is not the long-term archive.

## 16. Indexing and HDD-aware defaults

Create narrow indexes for demonstrated hot paths.

Required initial indexes:
- `project_contract_revisions(contract_id, revision_no DESC)`
- `contract_deliveries(run_id, logical_agent_id, delivered_at DESC)`
- `checkpoint_instances(run_id, status)`
- `publication_deliveries(recipient_branch_id, delivered_at DESC)`
- `candidate_snapshots(candidate_solution_id, snapshot_no DESC)`
- `graph_relationships(run_id, from_ref_type, from_ref_id, relationship_type)`
- `graph_relationships(run_id, to_ref_type, to_ref_id, relationship_type)`
- `events(run_id, event_position)`
- partial queue index on `council_runtime.tasks(status, available_at, priority DESC)` for runnable statuses
- `task_leases(expires_at)`
- `operations(run_id, idempotency_key)` UNIQUE
- `sandbox_instances(candidate_solution_id, status)`

Avoid:
- GIN indexes on arbitrary JSONB payloads by default
- indexing every graph property
- storing huge logs/events in indexed text columns
- table partitioning before measurements justify it

On HDD-backed installations, favor sequential append, batched projection updates, bounded graph traversals, and compact hot indexes.

## 17. Migrations, backup, and recovery

- All schema changes are migration-driven and version-controlled from implementation day one.
- Use transactional PostgreSQL DDL where supported.
- Never make production schema changes by hand without a recorded migration.
- Backups include PostgreSQL plus an artifact manifest and the referenced retained artifacts.
- Restore verification is part of backup validation.
- Runtime rows may be reconstructed/reconciled only when canonical state and external truth make that safe.
- Projection tables and caches are rebuildable from canonical records/events.
- A failed side effect remains failed/unknown until reconciled; recovery does not rewrite history.

## 18. Part 3 completion boundary

Part 3 is complete when implementation can derive migrations and typed persistence repositories from this model without making new product-level decisions about:
- canonical ownership
- branch visibility
- contract/checkpoint versioning
- candidate/environment identity
- Match My PC persistence
- artifact boundaries
- runtime versus durable state
- solution promotion/reuse
- retention
- concurrency
- indexing/recovery

Part 4 may refine field types and command DTOs, but it must not silently change these invariants.

## 19. October 13 schema refinements (not migrations)

Use one deployment-local transactional event-clock row for the initial single-PostgreSQL deployment. Every event-producing canonical transaction obtains that row lock before aggregate/budget locks, allocates its event positions by updating the row, and holds the lock through commit/rollback. Allocate all events of the transaction together. Do not use an ordinary sequence, SERIAL, or IDENTITY allocation as a committed-delivery watermark. This deliberately simple serialization trades throughput for clear ordering; measure before replacing it with a different recorded ordering design.

The clock, canonical mutation, events, idempotent result, and outbox entries commit together. No external call runs while holding that transaction. Rollback publishes nothing. Snapshot data and its committed event watermark come from one consistent database snapshot. Replay filters authorization and orders committed canonical events; visibility filtering must not turn hidden events into a spurious missing-data error.

Outbox workers claim unpublished rows, not just IDs greater than the last observed ID. A retry cannot skip an older unpublished row. Consumers deduplicate by event identity and advance projection offsets atomically with effects only across processed committed events. Out-of-order notification delivery triggers ordered canonical replay/buffering rather than falsely advancing a watermark. The snapshot/SSE race and the lower-number-transaction-commits-later scenario require integration tests.

LangGraph checkpoints are continuation projections, not a second authority over effects, permission, or completion. Bind continuation to logical member, execution epoch, contract/permission versions, and source event position. On restore, reconcile against canonical operations and obligations before executing a step. Replayed framework nodes must reuse logical operation identities and may not redispatch uncertain consequential effects. Runtime side-effect and accounting records prevail over an old checkpoint.

Required additional record groups:

- council_core.event_clock: singleton per deployment with last_position; locked through each event-producing canonical transaction.
- checkpoint repository publications: checkpoint/generation, repository, approved refs/history manifest and hashes, user authorization, desired/observed visibility, external operation IDs, first observed exposure, private confirmation, errors. This does not make private database rows public.
- independent checkpoint reviews: immutable checkpoint/generation/reviewer/candidate-bound assessment and evidence hashes; private until an atomic all-five reveal/delivery record.
- checkpoint review frontiers: message sequence, obligation version, review generation, member processed watermark, and version-bound DONE certificate. Communication state is separate from verification/check status and candidate readiness.
- clarification lineage: raw response reference, processed response, source statement locators, scope/strength, branch-local context manifest, confirmation, and effective contract revision.
- budget accounts/reservations/settlements: fixed-precision units, pricing version, run/branch/parent scope, operation/attempt, pre-dispatch bound, protected review allocation, dispatch state, actual usage, and unresolved liability. Expiry cannot refund a dispatched/unknown operation.
- approved budget version governs 70% development / 25% protected checkpoint review / 5% protected orchestration-finalization **proposed defaults**, with equal monetary development shares among five members; user may approve a different distribution, and hard token ceilings remain separately explicit. BYOK billing is outside these Council budget tables.
- event-producing budget reserve/settle transactions lock the deployment transactional event-clock row first, then budgets in run -> pool -> member/phase order, before operations/events/outbox commit. No external request while SQL locks are held.
- BYOK remote-provider configuration: provider/model profile version, owning user/deployment, scoped opaque credential reference in trusted secret storage, verification/revocation metadata, and authorized model-bridge policy. Never store raw API keys in Council control tables, event payloads, agent sandboxes, or Git archives. Local inference requires no external provider key. Provider directly bills user in the MVP; no prepaid Council-wallet ledger is required. Managed credits/payment reconciliation is a deferred, separately designed option.
- member phase admission and blocked/exhausted records: stable seat cursor, execution epoch, resource vector, semantic phase/checkpoint identifier, per-member phase token/cost ceilings and usage, durable suspension point, BUDGET_EXHAUSTED / INCOMPLETE status, block reason/dependency, operation timeout/recovery retry ceiling, and confirmed release state. No mandatory periodic private-work slice is required.
- optional project-total and per-phase token/cost planning forecasts: estimated ranges, source/history basis, assumptions, uncertainty flag and forecast version. Forecasts are never spending authorizations or automatic budget adjustments; actual usage and approved ceilings remain separate.
- archive manifests/validation: retained hashes and reference closure, authorization, validation outcome, missing evidence, and teardown eligibility.

These are accepted data requirements. Concrete field types, constraints, migration code, lock ordering beyond the stated event-clock rule, adapters, and integration tests remain open. There is no permanent SQL learning schema.
