# Part 4 - typed interaction, command, event, state, and action contracts

**Status:** partial architecture for Part 4; Part 4A authority boundaries are approved, but the complete Part 4 contract set is not yet designed.  
**Authority:** this document refines the state/action, user-interaction, command, event, and UI-wiring requirements in APP_DESIGN.md and the persistence model in POSTGRES_DATA_MODEL.md. If a supporting document conflicts with the latest explicit owner instruction or APP_DESIGN.md, the latest owner instruction and APP_DESIGN.md remain authoritative.  
**Implementation status:** specification only. No application code is implied by this document.

## 1. Purpose

Council must never expose a status that is only a label.

Every externally meaningful state or activity must be connected to the action that caused it, the behavior that occurs while it is active, any user interface surface it requires, the commands that can leave it, the events produced by those commands, and its failure/recovery path.

The central rule is:

> State -> trigger -> guarded system behavior -> observable effect -> available action -> typed command -> durable event -> next state.

A developer must not be able to implement AWAITING_PROJECT_APPROVAL as passive text on a dashboard. Entering that condition creates a durable interaction request for one exact Project Contract revision, which the frontend presents as an approval dialog and in the persistent Interaction Center.

## 2. Four different concepts must remain separate

Council uses four related but non-interchangeable concepts.

### 2.1 Lifecycle state

Lifecycle state is a small, stable state machine used for invariants and authorization.

Project lifecycle:
- DEFINING
- READY
- ACTIVE
- FINALIZING
- COMPLETED
- CANCELLED

Run lifecycle:
- CREATED
- PROVISIONING
- ACTIVE
- PAUSED
- STOPPING
- FINALIZING
- COMPLETED
- CANCELLED
- FAILED

Lifecycle state changes relatively rarely. It answers questions such as whether a run may accept new tasks, whether a project can be edited, and whether finalization has begun.

### 2.2 Activity code

Activity code explains what an entity is actually doing now. It is more descriptive and may change frequently.

A project can be ACTIVE while its current run activity is CROSS_EXAMINING_PEER_WORK. At the same moment, one council member can be RUNNING_TESTS, another can be RESPONDING_TO_CHALLENGES, and a worker can be WAITING_ON_MODEL.

Activity codes are scoped to entities; there is no single giant global enum.

### 2.3 Operation/task status

Operational status describes execution mechanics such as queueing, leasing, waiting, retrying, reconciliation, completion, and failure. It is not a substitute for human-readable activity.

Canonical MVP operation statuses:
- QUEUED
- LEASED
- RUNNING
- WAITING_ON_DEPENDENCY
- WAITING_ON_USER_INPUT
- RETRY_SCHEDULED
- SUCCEEDED
- FAILED
- CANCELLED
- UNKNOWN_PENDING_RECONCILIATION

### 2.4 Interaction request

An interaction request is a durable request for a human decision or answer. It is the only mechanism that may cause a blocking user decision surface.

An activity code containing AWAITING does not, by itself, open a pop-up. The backend first persists one interaction request, then publishes its event. This prevents duplicate pop-ups after reconnects, retries, or replayed events.

## 3. Activity-code registry

Every activity code is registered with:
- code
- entity scope
- display label
- short explanation
- entry trigger
- runtime owner
- allowed concurrent activities, where relevant
- whether user action is required
- associated interaction type, if any
- normal completion event
- failure/recovery behavior
- detail-schema version

Unknown activity codes may be rendered as an explicit unknown/forward-compatible state by older clients, but the backend must reject unknown state transitions.

### 3.1 Project Orchestrator activity codes

Initial authoritative set:
- COLLECTING_PROJECT_REQUIREMENTS
- IDENTIFYING_AMBIGUITIES
- REQUESTING_USER_CLARIFICATION
- BUILDING_PROJECT_CONTRACT
- VALIDATING_PROJECT_CONTRACT
- GENERATING_COUNCIL_INSTRUCTIONS
- GENERATING_CHECKPOINT_POLICY
- AWAITING_PROJECT_APPROVAL
- REWORKING_PROJECT_CONTRACT
- VALIDATING_REVISED_PROJECT_CONTRACT
- PREPARING_RUN_LAUNCH
- BROKERING_RUNTIME_CLARIFICATION
- PREPARING_CONTRACT_REVISION
- AWAITING_REVISION_APPROVAL
- PREPARING_FINAL_USER_REVIEW
- ARCHIVING_PROJECT_RECORDS

### 3.2 Run activity codes

Initial authoritative set:
- PROVISIONING_COUNCIL
- CREATING_AGENT_WORKSPACES
- PREPARING_EXECUTION_ENVIRONMENTS
- INITIALIZING_COUNCIL_MEMBERS
- DISTRIBUTING_PROJECT_CONTRACT
- STARTING_INDEPENDENT_INVESTIGATION
- INDEPENDENT_INVESTIGATION
- OPENING_CHECKPOINT_REPOSITORIES
- CROSS_EXAMINING_PEER_WORK
- REVISING_AFTER_PEER_REVIEW
- REVIEWING_COVERAGE
- PREPARING_MATURE_CANDIDATES
- RUNNING_FULL_PEER_REVIEW
- REMEDIATING_REVIEW_FINDINGS
- RUNNING_CLEAN_REBUILDS
- RUNNING_FINAL_ACCEPTANCE_TESTS
- PERFORMING_PREMORTEM
- ASSEMBLING_FINAL_RESULTS
- AWAITING_FINAL_USER_DECISION
- FINALIZING_ACCEPTED_CANDIDATE
- CLEANING_DISPOSABLE_ENVIRONMENTS
- RECOVERING_RUNTIME_STATE

### 3.3 Council-member activity codes

Initial authoritative set:
- IDLE
- PLANNING_INVESTIGATION
- INVESTIGATING
- SPAWNING_WORKERS
- WAITING_FOR_WORKERS
- INTEGRATING_WORKER_RESULTS
- EXECUTING_CANDIDATE_WORK
- RUNNING_TESTS
- PREPARING_CHECKPOINT_REPO
- WAITING_FOR_CHECKPOINT
- REVIEWING_PEER_WORK
- FORMULATING_CHALLENGE
- RESPONDING_TO_CHALLENGE
- REVISING_POSITION
- TESTING_REVISION
- PREPARING_FINAL_CANDIDATE
- WAITING_ON_CLARIFICATION
- AWAITING_FINALIZATION

### 3.4 Worker/task activity codes

Initial authoritative set:
- PREPARING_CONTEXT
- CALLING_MODEL
- WAITING_ON_MODEL
- USING_TOOL
- EXECUTING_SANDBOX
- RUNNING_TESTS
- SEARCHING_PRIOR_RECORDS
- WAITING_ON_DEPENDENCY
- WAITING_ON_USER_INPUT
- INTEGRATING_RESULTS
- RETURNING_RESULT
- RECONCILING_UNKNOWN_OUTCOME

### 3.5 Checkpoint lifecycle

Checkpoint states:
- SCHEDULED
- TRIGGERED
- OPENING_REPOSITORY_ACCESS
- REVIEWING
- CLOSING_REPOSITORY_ACCESS
- REVISION_WINDOW
- CLOSED
- CANCELLED
- FAILED

A checkpoint does not expose branch-private information merely by becoming TRIGGERED. Exposure begins only after the runtime has granted the authorized peer read access and recorded the exact opening commit for each participating repository.

The repository is the primary checkpoint publication surface. Each Council member continues to own and write only its own repository. During REVIEWING, peers may read/clone/test the other participating repositories but receive no write authority over them. The runtime records opening commit, access window, review-period commits, and closing commit. When CLOSING_REPOSITORY_ACCESS completes, reciprocal peer access is revoked and the branches return to private operation while retaining knowledge legitimately learned during review.

### 3.6 Candidate lifecycle

Candidate states:
- BUILDING
- TESTING
- READY_FOR_PEER_REVIEW
- UNDER_PEER_REVIEW
- REVISING
- CLEAN_REBUILD_VERIFYING
- ACCEPTANCE_TESTING
- READY_FOR_USER_REVIEW
- ACCEPTED
- REJECTED
- SUPERSEDED
- FAILED

### 3.7 Environment lifecycle

Environment states:
- REQUESTED
- PROVISIONING
- READY
- BUSY
- REBUILDING
- FAILED
- DESTROYING
- DESTROYED

## 4. State Contract

Every externally meaningful state or activity definition must have a State Contract.

Required fields:
- code
- schema_version
- entity_scope
- purpose
- entered_when
- guards
- owner_component
- system_actions_on_entry
- system_actions_while_active
- user_surface
- user_information_required
- allowed_user_actions
- allowed_system_commands
- emitted_events
- success_transitions
- alternate_transitions
- failure_transitions
- cancellation_behavior
- timeout_behavior
- retry_behavior
- observability_fields
- audit_requirements
- blocking_scope
- resumability_behavior

No state may be added to the product without defining these fields or explicitly marking non-applicable fields.

This is a design and implementation invariant, not documentation decoration. State definitions should be represented in versioned code/configuration so backend transition guards, API schemas, UI rendering, tests, and documentation can be generated from or validated against the same registry.

## 5. Command model

A command is a request to change state or perform an operation. It is not proof that the requested action happened.

Every command uses a common envelope containing:
- command_id
- command_type
- schema_version
- actor_type
- actor_id
- project_id
- run_id when applicable
- branch_id when applicable
- target_type
- target_id
- expected_target_version when applicable
- idempotency_key
- issued_at
- correlation_id
- causation_id when applicable
- payload

Command handling order:
1. authenticate actor;
2. authorize actor for target scope;
3. validate schema;
4. verify expected version/hash;
5. verify lifecycle/activity transition guard;
6. check idempotency;
7. perform canonical mutation atomically;
8. write audit/event/outbox records in the same transaction;
9. return the canonical result;
10. perform external side effects only through a recoverable operation record.

A rejected command produces an explicit typed error. It must not partially mutate canonical state.

## 6. Event model

An event is an authoritative recorded fact.

Every durable event contains:
- event_id
- global monotonic event_position
- event_type
- schema_version
- aggregate_type
- aggregate_id
- aggregate_version where applicable
- project_id
- run_id where applicable
- branch_id/visibility when applicable
- actor attribution
- occurred_at
- causation_command_id
- correlation_id
- payload

Commands and events use different names deliberately.

Examples:
- ApproveProjectContract is a command.
- ProjectContractApproved is an event.
- PublishCheckpoint is a command.
- CheckpointPublicationCreated is an event.
- ExecuteSandboxOperation is a command.
- SandboxOperationSucceeded, SandboxOperationFailed, and SandboxOperationOutcomeUnknown are mutually distinct event outcomes.

The event stream drives audit, projections, SSE updates, state history, and provenance. UI clients must not invent state transitions locally.

## 7. Durable interaction requests

### 7.1 Interaction-request lifecycle

Interaction request states:
- OPEN
- PRESENTED
- ANSWERED
- STALE
- CANCELLED

OPEN means the decision exists durably but may not yet have been displayed on the current client. PRESENTED means at least one client acknowledged rendering it. Neither is a user decision.

Closing or dismissing the visual pop-up does not answer the request. The request remains visible in the Interaction Center and the blocked scope remains blocked.

No request is auto-approved because of timeout, disconnection, application close, or model assumption.

### 7.2 Required interaction fields

Each request records:
- interaction_request_id
- type
- schema_version
- project_id
- run_id/branch_id where applicable
- target_type
- target_id
- exact target revision/version/hash
- title
- explanatory summary
- structured payload
- allowed action codes
- blocking scope
- priority
- created_event_id
- created_at
- status
- presented_at
- resolved_event_id
- resolved_at
- stale_reason when applicable

Every user response records:
- response_id
- interaction_request_id
- actor_id
- action_code
- structured response payload
- expected target revision/version/hash
- idempotency key
- submitted_at

### 7.3 UI rule

A blocking interaction request causes:
1. persistence of the request;
2. commit of its outbox/event record;
3. SSE delivery to connected clients;
4. a blocking dialog or equivalent full-screen decision surface on the active client;
5. simultaneous appearance in the persistent Interaction Center.

The frontend never opens a decision dialog merely because it sees a lifecycle/activity label. It opens one for the durable interaction-request ID. Replaying the same event therefore does not create a second request or a second decision.

If the app was closed, the request remains OPEN and is shown on reconnect.

If several blocking requests exist, the UI presents one decision surface at a time using explicit priority and creation order while keeping the complete queue visible.

## 8. Exact Project Contract approval flow

This is the reference interaction contract.

### 8.1 Entry

The Project Orchestrator has:
- gathered sufficient requirements;
- generated an immutable Project Contract revision;
- validated required fields and internal consistency;
- generated or prepared the neutral instruction/checkpoint configuration required to explain the proposed run.

The backend then:
- sets orchestrator activity to AWAITING_PROJECT_APPROVAL;
- creates one PROJECT_CONTRACT_APPROVAL interaction request targeted to the exact contract revision and content hash;
- emits ProjectContractApprovalRequested.

### 8.2 User surface

The application opens a blocking Project Contract approval dialog. The same request appears in the Interaction Center.

The user must be able to inspect, at minimum:
- objective;
- required deliverables;
- constraints and non-goals;
- acceptance criteria and definition of done;
- council size and configured models/providers;
- execution-environment mode;
- granted permissions;
- budget/usage ceilings;
- checkpoint/communication policy;
- material assumptions;
- differences from the previous revision, if any;
- exact revision identifier/hash being approved.

### 8.3 User actions

#### APPROVE_AND_LAUNCH

Command: ApproveProjectContract.

Guards:
- request is still OPEN/PRESENTED;
- exact revision/hash still matches;
- no newer contract revision superseded it;
- actor has project approval authority.

Atomic canonical effects:
- record immutable APPROVED decision;
- resolve the interaction request;
- activate the revision for launch;
- create or transition the run into PROVISIONING unless the approved contract explicitly uses delayed/manual launch;
- emit ProjectContractApproved and RunProvisioningStarted through the same reliable event/outbox boundary.

Next visible activity:
- PROVISIONING_COUNCIL.

#### REQUEST_CHANGES

The UI expands a feedback field and requires actionable feedback.

Command: RequestProjectContractChanges.

Effects:
- record immutable CHANGES_REQUESTED decision and feedback;
- resolve the current interaction request;
- do not mutate the declined revision;
- set orchestrator activity to REWORKING_PROJECT_CONTRACT;
- create an orchestrator revision task linked to the rejected revision and feedback;
- emit ProjectContractChangesRequested.

The Orchestrator creates a new immutable revision, validates it, and returns to AWAITING_PROJECT_APPROVAL with a new interaction request.

#### REJECT_CURRENT_APPROACH

This means the project objective still stands, but the user rejects the proposed execution approach.

Command: RejectProjectContractApproach.

Effects:
- record immutable CURRENT_APPROACH_REJECTED decision;
- preserve the prior revision for history;
- return control to REWORKING_PROJECT_CONTRACT;
- instruct the Project Orchestrator to propose a materially different execution approach while preserving the user's unchanged objective and constraints;
- link the new proposal causally to the rejection;
- emit ProjectContractApproachRejected.

Feedback is strongly encouraged but may be empty. If hard requirements make a materially different approach impossible, the next proposal must explain the constraint rather than pretend to be different.

#### CANCEL_PROJECT

This is distinct from rejecting an approach.

The first click opens a destructive confirmation dialog. Closing that confirmation does nothing.

After confirmation:
Command: CancelProjectSetup.

Effects:
- resolve/cancel open setup interactions;
- mark the project CANCELLED;
- ensure no run is launched;
- clean any disposable pre-run resources;
- emit ProjectSetupCancelled.

### 8.4 Closing the approval dialog

Closing the visual dialog is not a decision.

The interaction remains OPEN/PRESENTED, the project remains blocked at approval, and the Interaction Center continues to show the request.

### 8.5 Stale approval

If a newer Project Contract revision appears before the user submits a decision:
- mark the old interaction STALE;
- disable its action buttons;
- show that a newer revision requires review;
- create a new request for the new revision.

Approval can never float from one revision to another.

## 9. Runtime clarification flow

When a Council member or worker needs user input:
1. the originating agent creates RequestUserInput;
2. the runtime validates the request structurally and creates a durable USER_CLARIFICATION interaction request without an Orchestrator intellectual veto;
3. only work that actually depends on the answer transitions to WAITING_ON_USER_INPUT; unaffected work continues where safe;
4. the UI identifies the originating Council actor and presents the question to the user;
5. the user's raw answer is recorded immutably as RAW_USER_RESPONSE;
6. the Project Orchestrator receives the raw answer and its small prompt/clarification memory;
7. the Orchestrator produces a processed, agent-ready answer that may improve form but must not change substance;
8. the processed answer is recorded as PROCESSED_USER_RESPONSE and delivered to the requesting agent or worker;
9. if the answer changes a project-wide requirement, the appropriate canonical project revision is created and distributed consistently to every affected branch.

A raw user answer never flows directly to a Council agent or worker. The Orchestrator may structure, compress, resolve obvious references, and make already-clear requirements explicit, but it may not invent, strengthen, weaken, or silently authorize user intent. If material meaning remains unresolved, the Orchestrator asks the user again.

See PART_4A_AUTHORITY_BOUNDARIES.md for the authoritative authority and routing invariants.

## 10. Other user-gated interactions

### 10.1 Permission expansion

If a task requires a permission outside the Project Contract:
- affected operation is blocked;
- Council creates PERMISSION_EXPANSION_REQUESTED;
- the dialog states the exact capability, scope, reason, duration, and affected task;
- user may APPROVE_EXACT_SCOPE, MODIFY_SCOPE where supported, or REJECT.

Rejecting permission does not automatically fail the project. The requesting branch receives a canonical PERMISSION_DENIED outcome and must attempt an alternative within existing permissions or report the blocker.

### 10.2 Budget expansion

If the run reaches a protected budget boundary:
- new spend that would cross the boundary is blocked;
- already safe/recoverable work may continue according to reservation rules;
- dialog shows current usage, requested increase, reason, and protected review allowance;
- user may APPROVE_NEW_CEILING, SET_DIFFERENT_CEILING, or REJECT_INCREASE.

Rejecting an increase causes the runtime/council to continue within the existing ceiling where possible and produce a partial outcome if required. It must not silently exceed the budget.

### 10.3 Match My PC and host mutation

Complete-product interactions, deferred from the MVP unless required:
- ENVIRONMENT_CONTRACT_APPROVAL
- PRIVILEGED_CAPABILITY_APPROVAL
- HOST_MUTATION_APPROVAL

Presence of software/device state never implies permission. Host mutation is a separate gate from host matching. Each requested elevated operation must show the exact action and scope.

### 10.4 Final candidate review

When final results are ready, Council creates FINAL_CANDIDATE_REVIEW.

The user surface shows:
- candidate identities and exact repository revisions;
- acceptance-test and clean-rebuild results;
- peer-review findings and dispositions;
- unresolved objections;
- relevant provenance;
- cost/time/usage;
- environment definition and delivery consequences.

Available actions:
- ACCEPT_CANDIDATE;
- REQUEST_CANDIDATE_REVISIONS;
- REJECT_CANDIDATE;
- CANCEL_FINALIZATION.

The system does not silently choose the user's accepted candidate. Acceptance is a user action. If only one candidate exists, the same rule applies.

ACCEPT_CANDIDATE begins FINALIZING_ACCEPTED_CANDIDATE, promotes accepted metadata to the solution registry, performs delivery cleanup, removes Council-only credentials/control mechanisms, and then archives/disposes run state according to policy.

REQUEST_CANDIDATE_REVISIONS reopens the necessary review/remediation scope and records the user's requested changes.

REJECT_CANDIDATE preserves the candidate and its evaluation history as rejected; another candidate may be reviewed or additional work may be commissioned if the Project Contract/budget permits.

## 11. Primary typed command catalog

The MVP must define versioned schemas for at least:

Project/orchestrator:
- CreateProject
- SubmitProjectMessage
- GenerateProjectContractRevision
- ApproveProjectContract
- RequestProjectContractChanges
- RejectProjectContractApproach
- ConfirmContractRevision
- CancelProjectSetup

Run control:
- StartRun
- PauseRun
- ResumeRun
- StopRun
- CancelRun

Council/task:
- CreateTask
- LeaseTask
- HeartbeatTaskLease
- CompleteTask
- FailTask
- CancelTask
- CreateWorker
- ReturnWorkerResult

Checkpoint/review:
- TriggerCheckpoint
- PublishCheckpoint
- DeliverPublication
- AcknowledgePublication
- SubmitChallenge
- SubmitChallengeResponse
- RecordClaimRevision
- CloseCheckpoint

Escalation/user interaction:
- CreateStructuredEscalation
- CreateInteractionRequest
- MarkInteractionPresented
- RespondToInteraction
- RequestPermissionExpansion
- RequestBudgetExpansion

Model/tool/environment:
- RequestModelCall
- RecordModelCallResult
- CreateSandbox
- ExecuteSandboxOperation
- DestroySandbox
- RequestCleanRebuild

Continuity/finalization:
- CreateContinuationPacket
- StartNewAgentSession
- MarkCandidateReadyForReview
- FinalizeCandidate
- AcceptCandidate
- RequestCandidateRevisions
- RejectCandidate

Implementation may expose specialized public endpoints rather than a generic command endpoint. The typed command definitions remain the domain boundary.

## 12. Primary event catalog

The MVP must define versioned schemas for at least:

Project/contract:
- ProjectCreated
- ProjectContractRevisionCreated
- ProjectContractValidated
- ProjectContractApprovalRequested
- ProjectContractApproved
- ProjectContractChangesRequested
- ProjectContractApproachRejected
- ProjectContractRevisionConfirmed
- ProjectSetupCancelled

Run:
- RunProvisioningStarted
- RunStarted
- RunPaused
- RunResumed
- RunStopRequested
- RunCompleted
- RunCancelled
- RunFailed

Council/task:
- TaskCreated
- TaskLeased
- TaskLeaseExpired
- TaskWaitingOnDependency
- TaskWaitingOnUserInput
- TaskCompleted
- TaskFailed
- TaskCancelled
- WorkerCreated
- WorkerResultReturned

Checkpoint/review:
- CheckpointTriggered
- CheckpointPublicationCreated
- PublicationDelivered
- ChallengeSubmitted
- ChallengeResponseSubmitted
- ClaimRevisionRecorded
- CheckpointClosed

Interaction:
- InteractionRequested
- InteractionPresented
- InteractionAnswered
- InteractionBecameStale
- InteractionCancelled

Model/tool/environment:
- ModelCallRequested
- ModelCallSucceeded
- ModelCallFailed
- ModelCallOutcomeUnknown
- SandboxProvisioningStarted
- SandboxReady
- SandboxOperationStarted
- SandboxOperationSucceeded
- SandboxOperationFailed
- SandboxOperationOutcomeUnknown
- CleanRebuildStarted
- CleanRebuildPassed
- CleanRebuildFailed
- SandboxDestroyed

Continuity/finalization:
- ContinuationPacketCreated
- AgentSessionRolledOver
- CandidateReadyForReview
- CandidateAccepted
- CandidateRevisionRequested
- CandidateRejected
- CandidateFinalized

This is the minimum catalog, not permission to invent untracked side effects outside it.

## 13. Entity-specific transition rules

### 13.1 Run

CREATED -> PROVISIONING only after an approved launch revision exists.

PROVISIONING -> ACTIVE only after required seats/workspaces/environments are ready or explicitly recorded as not required.

ACTIVE -> PAUSED through PauseRun or a system safety condition.

PAUSED -> ACTIVE through ResumeRun after guards pass.

ACTIVE/PAUSED -> STOPPING through StopRun.

STOPPING -> CANCELLED when cancellation/cleanup completes, or -> FAILED when required cleanup/reconciliation cannot complete safely.

ACTIVE -> FINALIZING only when the Council protocol reaches its configured completion gate.

FINALIZING -> COMPLETED only after required final records and cleanup are durable.

No terminal state may return to ACTIVE.

### 13.2 Council member

Member activity changes do not change logical identity. Session rollover preserves the member and branch.

A member cannot enter REVIEWING_PEER_WORK before it has received an explicit publication delivery for the reviewed material.

A member cannot enter RESPONDING_TO_CHALLENGE for a challenge it is not authorized to see.

### 13.3 Task

Only one live lease may own an executable task at a time.

A waiting task releases scarce execution capacity.

An expired lease may be reclaimed only after the runtime applies operation-specific reconciliation rules.

UNKNOWN_PENDING_RECONCILIATION cannot be converted to SUCCEEDED solely because a retry was attempted.

### 13.4 Candidate

READY_FOR_PEER_REVIEW requires a frozen repository revision and environment-definition identity.

READY_FOR_USER_REVIEW requires the configured review/verification gates to have completed or to be explicitly recorded as unresolved/failed for user inspection.

ACCEPTED is a user decision, not a council vote.

## 14. Activity detail and user-facing status

The runtime owns the activity code. Agents may report structured progress, but an agent cannot authoritatively set arbitrary UI status text.

Each activity code may include structured detail, for example:
- REVIEWING_PEER_WORK: reviewer branch, target publication, review task count;
- RUNNING_TESTS: candidate revision, suite identity, completed/total deterministic tests;
- WAITING_ON_USER_INPUT: interaction request ID and blocked task count.

The UI renders a readable sentence from the activity definition plus structured detail, for example:

Active - Cross-examining peer candidates  
Agent 1 is reviewing Agent 3's published checkpoint. 2 challenges submitted, 1 response pending, 3 workers active.

Do not show fabricated percentage progress. Percentages are allowed only when there is a deterministic finite checklist or benchmark denominator.

## 15. Atomicity, idempotency, and stale-action handling

Every user-facing button that mutates state sends:
- interaction_request_id where relevant;
- command_id;
- idempotency_key;
- expected target version/hash.

Double-clicks, mobile retries, reconnects, and repeated SSE delivery must not create duplicate approvals, duplicate launches, duplicate publications, or duplicate host/budget grants.

A user decision and the canonical state change it authorizes must commit atomically where they are part of one local transaction. External work begins only after the durable command/event/outbox boundary commits.

If expected version/hash is stale:
- command is rejected as STALE_TARGET;
- no partial decision is recorded as approval;
- UI reloads the current canonical target;
- old interaction is marked STALE when appropriate.

## 16. Failure and recovery rules

Failures are explicit states/events, not generic text.

For any action with an external side effect, Council records an operation identity before execution.

Possible outcomes are:
- succeeded;
- failed with known non-effect;
- unknown/pending reconciliation.

The runtime may retry only when the operation contract says the retry is safe or reconciliation proves the previous attempt did not already produce the effect.

UI behavior:
- user-actionable failures create an interaction only when the user can make a meaningful decision;
- internal transient failures remain visible in activity/history but do not spam pop-ups;
- unrecoverable failures show the exact failed component, known effects, unresolved uncertainty, and safe available actions.

## 17. Frontend/SSE contract

SSE is a delivery mechanism, not the source of truth.

On connection or reconnect, the frontend first loads a canonical snapshot containing:
- lifecycle states;
- activity projections;
- open interaction requests;
- current tasks/workers;
- checkpoints;
- candidates;
- usage/budget summary.

SSE then delivers incremental events after the snapshot position.

If an event gap is detected, the client refreshes from the canonical snapshot rather than guessing.

Decision dialogs are keyed by interaction_request_id. Activity cards are keyed by entity identity and activity projection. This separation ensures status replay cannot create duplicate prompts.

## 18. Persistence consequences

POSTGRES_DATA_MODEL.md must retain:
- immutable Project Contract decisions;
- durable interaction requests and immutable responses;
- audit/event causation and correlation;
- a runtime activity projection keyed by entity;
- explicit operation records for uncertain external side effects.

Interaction responses do not replace domain-specific canonical records. For example, an APPROVE_AND_LAUNCH response and the resulting Project Contract approval/run transition are written coherently in the same transaction boundary.

## 19. Required deterministic tests

Part 4 is not implemented correctly until tests prove:

1. A validated contract creates exactly one approval interaction for one revision/hash.
2. Replaying InteractionRequested does not create another interaction or duplicate modal identity.
3. Closing the modal without choosing an action leaves the request unresolved.
4. APPROVE_AND_LAUNCH cannot approve a superseded revision.
5. Double-submitting approval cannot launch two runs.
6. REQUEST_CHANGES preserves the old revision and produces a new revision path.
7. REJECT_CURRENT_APPROACH returns to Orchestrator rework rather than cancelling the project.
8. CANCEL_PROJECT cannot be confused with rejecting the current approach.
9. Runtime clarification blocks only the affected scope when safe.
10. No branch receives a revised Project Contract until the canonical revision is confirmed and explicitly delivered.
11. Rejecting permission/budget expansion does not silently grant it.
12. A checkpoint activity change alone never exposes unpublished branch data.
13. A task with UNKNOWN_PENDING_RECONCILIATION cannot be silently marked successful.
14. A reconnect restores all unresolved interactions from canonical storage.
15. An agent session rollover does not change logical-agent identity.
16. Final candidate acceptance requires a user decision.
17. No user gate auto-approves on timeout or disconnect.
18. Every registered externally meaningful activity code has a complete State Contract.

## 20. MVP boundary for Part 4

The MVP must implement:
- lifecycle + scoped activity taxonomy;
- State Contract registry;
- typed command/event envelopes;
- typed schemas for the primary MVP command/event catalog;
- Project Contract approval pop-up and Interaction Center;
- request changes / reject current approach / cancel distinctions;
- runtime clarification interaction;
- budget/permission expansion interactions when those limits are exercised;
- final candidate user review;
- idempotency and stale-version guards;
- canonical snapshot + SSE activity/interaction updates.

The MVP may defer:
- Match My PC approval surfaces;
- privileged-host mutation dialogs;
- advanced interaction prioritization beyond blocking priority + creation order;
- highly customized per-domain interaction components;
- schema backward compatibility across many released application versions.

The architecture hooks and invariants for deferred user gates still apply.

## 21. Part 4 completion boundary

Part 4 is architecturally complete when implementation can derive typed domain DTOs, transition guards, interaction schemas, UI decision surfaces, and deterministic state-machine tests without making new product-level decisions about:
- what a status means;
- what action enters or leaves it;
- when a pop-up appears;
- what every approval button does;
- how rejection differs from cancellation;
- how stale decisions are prevented;
- how user clarifications become canonical;
- how commands differ from events;
- how interaction requests survive reconnects;
- how activity/status is displayed without inventing progress.

Part 5 may refine transactional implementation patterns, but it must not weaken these action/state/UI invariants.
