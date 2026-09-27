# PostgreSQL data model

**Status:** approved design model for Part 3; this document defines persistence boundaries and invariants, not executable migrations.  
**Authority:** this document refines section 13 of [APP_DESIGN.md](APP_DESIGN.md). If they conflict, the latest explicit owner instruction and APP_DESIGN remain authoritative.

## 1. Database layout

Start with **one PostgreSQL instance** and three logical schemas:

- `council_core` - canonical durable project/run state, contracts, agents, checkpoints, evidence/provenance, candidates, environments, approvals, continuity records, and audit events.
- `council_runtime` - mutable operational state such as queues, leases, attempts, scheduler reservations, live sandbox instances, broker requests, and transient execution state.
- `solution_registry` - durable accepted-solution index used to find and reuse prior projects after user acceptance.

Do not split these into separate database servers until measured requirements justify it. Schema boundaries are architectural boundaries; they are not a claim that separate physical databases are needed.

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
Immutable approval/decline record.
- `id` PK
- `contract_revision_id` FK
- `user_id`
- `decision` = APPROVED | DECLINED
- `decided_at`
- `note`

A run cannot start from a revision without an APPROVED record.

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

Only an ACCEPTED candidate snapshot can be promoted to the solution registry.

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
- `event_position` BIGINT PK, monotonically increasing
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
- `provider_profile_version_id`
- `model_profile_version_id`
- `status`
- `input_tokens`
- `cached_input_tokens`
- `output_tokens`
- `cost_amount` nullable
- `started_at`
- `finished_at`

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

## 13. Solution registry

The solution registry receives only user-accepted solutions.

### solution_registry.solutions
- `id` PK
- `source_project_id` FK
- `name`
- `summary`
- `created_at`

### solution_registry.solution_versions
- `id` PK
- `solution_id` FK
- `version_no`
- `accepted_candidate_snapshot_id` FK
- `accepted_at`
- `repo_archive_ref`
- `environment_artifact_ref`
- `search_document`
- UNIQUE(`solution_id`, `version_no`)

### solution_registry.capabilities
- `id` PK
- `capability_key` UNIQUE
- `description`

### solution_registry.solution_capabilities
- `solution_version_id` FK
- `capability_id` FK
- `evidence_ref`
- PK(`solution_version_id`, `capability_id`)

### solution_registry.stack_components
- `id` PK
- `component_key` UNIQUE

### solution_registry.solution_stack_components
- `solution_version_id` FK
- `stack_component_id` FK
- `version_text`
- PK(`solution_version_id`, `stack_component_id`)

### solution_registry.reuse_relationships
Records when a prior accepted solution is used as a base/reference for a later project.
- `id` PK
- `source_solution_version_id` FK
- `target_project_id` FK
- `reuse_type` = BASE | REFERENCE | TECHNIQUE | NEAR_COPY
- `note`
- `created_at`

Initial reuse search uses structured capabilities, stack metadata, tags, and PostgreSQL full-text search. Do not add a separate vector database or embedding store until evaluation shows it materially improves project retrieval.

## 14. Acceptance, archival, and deletion

After user acceptance:

1. Freeze the accepted candidate snapshot.
2. Require successful clean rebuild verification for executable deliverables.
3. Record the acceptance decision.
4. Promote the accepted snapshot into `solution_registry`.
5. Archive the council-member repositories according to the repository lifecycle policy.
6. Retain canonical provenance needed to explain the accepted result, including the Project Contract history, delivered revisions, checkpoint publications used in review, acceptance record, accepted candidate/environment definitions, and cited evidence.
7. Retain minimal metadata and archive references for rejected candidates; full rejected runtime state is not required for normal reuse.
8. Destroy temporary sandboxes and unapproved temporary volumes.
9. Mark `council_runtime` rows eligible for purge after successful archive/backup/reconciliation.
10. Do not purge canonical records that are still referenced by the accepted solution, final report, audit history, or solution registry.

The exact time delay before purging eligible runtime rows is a configurable workspace retention policy, not a hard-coded architectural constant.

## 15. Concurrency and transaction rules

- Version append: immutable version rows use UNIQUE(parent_id, version_no). Concurrent append conflicts are retried after re-reading the current version.
- Mutable control rows: update with expected `row_version`; a mismatch produces a reviewable conflict/retry, never silent overwrite.
- Task leasing: use `FOR UPDATE SKIP LOCKED`, explicit lease expiry, heartbeats, and attempt numbers.
- External actions: use idempotency keys and operation-attempt history. Never claim exactly-once behavior for an external system that does not provide it.
- Contract revision activation: effective revision record, audit event, and intended delivery records are committed atomically.
- Checkpoint publication: publication, publication items, audit event, and initial delivery records are committed atomically.
- Claim revision: new claim version, revision reason, essential graph relationships, and audit event are committed atomically.
- Accepted candidate promotion: acceptance record and registry promotion metadata are transactional; large artifact/archive operations are reconciled through durable operations/outbox state.

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
- `solution_versions(solution_id, version_no DESC)`
- GIN full-text index on the registry `search_document`

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
