# Part 4 - typed interaction, command, event, state, and action contracts

**October 13, 2026 amendment:** [decision/status index](ARCHITECTURE_DECISIONS.md). Requirements below are specifications; application implementation is NOT STARTED and runtime tests are NOT RUN.

**Design status:** BASELINE DESIGNED; **ADR-17 local checkpoint interface REOPENED IN DESIGN**. Other command/interaction semantics remain established. **Implementation:** NOT STARTED. **Runtime/state-machine tests:** NOT RUN.
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
- GENERATING_PROJECT_CHECKPOINT_PLAN
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
- QUIESCING_FOR_PAUSE

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
- WAITING_ON_PHASE_BUDGET
- RECOVERING_MEMBER_SANDBOX
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

Checkpoint states: SCHEDULED, TRIGGERED, OPENING, SEALED_REVIEW, REVIEWING, CLOSING, CLOSED, CANCELLED, FAILED.

TRIGGERED does not expose any candidate. OPENING pins all five members' current local Git commits/trees, validates customer-authorized snapshot manifests and read-only recipient scopes, creates recoverable local export/grant operations and verifies actual content hashes/access. Only successfully verified local snapshots enter SEALED_REVIEW. Partial/unknown grants remain guarded and reconciled; no internet-public GitHub publication is implied.

SEALED_REVIEW permits independent repository inspection and isolated verification but not shared discussion or access to peer assessments. Each member submits an immutable review bound to the frozen candidates. RevealCheckpointReviews atomically publishes all required submissions and enters REVIEWING. Missing reviewers remain explicit blockers; ceiling-forced abort is incomplete, not successful review.

During REVIEWING candidates stay frozen. /work uses separate disposable verifiers; no implementation commits or pushes. Normal CLOSING requires current versioned DONE certificates, processed message/obligation frontiers, and no active work excursion. CLOSING fences the gateway, persists closeouts/transcript, revokes all temporary peer snapshot grants/routes, verifies the safe boundary, and creates return packets before CLOSED permits private revision. Failures remain observable/blocked rather than emitting a premature successful closure.

Communication completion, verification coverage, candidate readiness, and acceptance remain independent. See section 25 and CHECKPOINT_COMMUNICATION_GATEWAY.md.

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
1. authenticate actor and authorize its exact scope;
2. validate the command schema and canonicalize the request body/hash;
3. inside the event-clock-first canonical transaction, **check the scoped idempotency receipt/key before expected-version or transition guards**: same request returns the original authorized result even if the target has since changed; same key with different hash rejects as IDEMPOTENCY_CONFLICT;
4. for new commands only, verify expected version/hash and lifecycle/activity/permission/phase guards;
5. atomically perform the canonical mutation, append audit events/outbox records and persist the command receipt/result;
6. commit, then return the canonical result and dispatch any durable external operations **outside** the SQL transaction.

An idempotent replay must still authenticate/authorize the requesting actor, and it must not execute a second external operation. This ordering prevents a retry of a successful approval or /done from returning a spurious STALE_TARGET simply because the original command already advanced the state.

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
- PublishCheckpointSnapshots is a command.
- CheckpointSnapshotsAvailable is an event.
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
6. the Project Orchestrator receives the raw answer and only its authorized project-wide plus requesting-branch prompt/clarification memory;
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

The initial user-approved budget policy is immutable and versioned; propose a configurable 70% private development / 25% checkpoint review / 5% orchestration-finalization allocation. Equal monetary development shares across five seats are a starting suggestion only, not equal token entitlement. Users approve the hard run/member/semantic-phase token and cost ceilings and every material top-up or redistribution. The protected review/finalization pools cannot be debited by development without the appropriate new explicit authorization. The UI must distinguish a rough uncertain estimate from a ceiling and actual usage.

If the run reaches a protected budget boundary:
- new spend that would cross the boundary is blocked;
- already safe/recoverable work may continue according to reservation rules;
- dialog shows current usage, requested increase, reason, and protected review allowance;
- user may APPROVE_NEW_CEILING, SET_DIFFERENT_CEILING, or REJECT_INCREASE.

Rejecting an increase causes the runtime/council to continue within the existing ceiling where possible and produce a partial outcome if required. It must not silently exceed the budget. If the blocked work is a member's semantic phase, the member enters WAITING_ON_PHASE_BUDGET / BUDGET_EXHAUSTED_INCOMPLETE, retains its logical identity and unfinished phase, and cannot satisfy an all-five barrier.

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

ACCEPT_CANDIDATE begins FINALIZING_ACCEPTED_CANDIDATE, promotes accepted metadata to the Git-backed accepted-project archive, performs delivery cleanup, removes Council-only credentials/control mechanisms, and then archives/disposes run state according to policy.

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
- PublishCheckpointSnapshots
- CreateCheckpointCommunicationSession
- SubmitIndependentCheckpointReview
- RevealCheckpointReviews
- SendCheckpointMessage
- PromoteMessageToPeerAction
- CreatePeerAction
- AddPeerActionAddendum
- AcknowledgePeerAction
- SetPeerActionDisposition
- StartCheckpointWorkExcursion
- CompleteCheckpointWorkExcursion
- FailCheckpointWorkExcursion
- MarkCheckpointCommunicationDone
- ReopenCheckpointCommunicationMember
- CloseCheckpointCommunicationSession
- RevokeCheckpointSnapshotAccess
- SubmitCheckpointCloseout
- CreateCheckpointReturnPacket
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
- ApproveRunBudgetPolicy (user-authorized, immutable policy revision)
- ReserveModelCallAllowance (trusted runtime; atomic budget + resource operation before dispatch)
- RecordBudgetReservationSettlement (trusted runtime; actual usage or conservative unknown liability)
- RecordMemberPhaseBudgetExhaustion (trusted runtime; incomplete, not readiness)
- RecordResourceAdmission
- RecordSandboxResourceRelease
- RecordMemberRecoveryAttempt
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
- RunPauseRequested
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
- CheckpointSnapshotsAvailable
- CheckpointCommunicationSessionCreated
- IndependentCheckpointReviewSubmitted
- CheckpointPeerReviewsRevealed
- CheckpointMessageAccepted
- CheckpointMessageDelivered
- PeerActionCreated
- PeerActionAcknowledged
- PeerActionDispositionChanged
- PeerActionAddendumAdded
- CheckpointWorkExcursionStarted
- CheckpointWorkExcursionCompleted
- CheckpointWorkExcursionFailed
- CheckpointMemberMarkedDone
- CheckpointMemberReactivated
- CheckpointCommunicationQuiescing
- CheckpointCommunicationSessionClosed
- CheckpointSnapshotAccessRevoked
- CheckpointCloseoutRecorded
- CheckpointReturnPacketCreated
- ClaimRevisionRecorded
- CheckpointClosed

Interaction:
- InteractionRequested
- InteractionPresented
- InteractionAnswered
- InteractionBecameStale
- InteractionCancelled

Model/tool/environment:
- BudgetPolicyApproved
- BudgetReservationCreated
- BudgetReservationSettled
- BudgetReservationOutcomeUnknown
- MemberPhaseBudgetExhausted
- MemberRecoveryAttempted
- MemberBlocked
- SandboxQuiesced
- SandboxResourceReleaseConfirmed
- BridgeExecutionEpochRevoked
- ResourceAdmissionDenied
- MemberSandboxResourcePressureDetected (a meaningful 80%/90% policy state transition, not every sample)
- MemberSandboxOOMObserved
- MemberResourceMonitoringUnavailable (stale/unavailable monitor state affecting safe admissions)
- MemberResourceMonitoringRestored
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

PauseRun or a system safety condition stops new ordinary admissions and enters run **activity** QUIESCING_FOR_PAUSE while lifecycle remains ACTIVE. ACTIVE -> PAUSED occurs only when the required durable member suspension, revoked bridge authority, and backend-confirmed resource release have been recorded. In-flight unknown external operations remain separately recorded and are not implicitly cancelled. The PAUSED state is recoverable, not terminal.

PAUSED -> ACTIVE through ResumeRun only after approved contract, permissions, phase budget/reservations, host resources, model credentials, sandbox checker, execution epochs, and affected uncertain-operation dependencies pass. If guards fail remain PAUSED with explicit reasons.

ACTIVE/PAUSED -> STOPPING through StopRun, which fences old execution epochs, prohibits new ordinary work, requests only supported cancellations, and records unresolved effects. STOP does not imply project/user candidate acceptance.

STOPPING -> CANCELLED when cancellation/cleanup completes, or -> FAILED / explicitly incomplete cleanup when required boundary safety cannot be established. Report unresolved provider billing/side effects and reservations honestly.

ACTIVE -> FINALIZING only when the Council protocol reaches its configured completion gate.

FINALIZING -> COMPLETED only after required final records and cleanup are durable.

No terminal state may return to ACTIVE.

### Step 7 operational events and phase invariants

All commands/events above use the existing typed envelope, idempotency, expected-version checks, Part 5 transactional event-clock ordering, and outbox. `BudgetReservationCreated` and its operation record must commit before any external request; `BudgetReservationSettled` cannot clear another caller's reserved amount. A timeout or disconnected provider produces an outcome-specific status, not a fictional cancellation or refund.

A member that exhausts its approved per-phase token/cost cap remains an **incomplete** required seat. The runtime may preserve and suspend it, but may not emit its `CHECKPOINT_READY` or `/done`. A new explicit user-approved budget policy can make it eligible to resume; the original checkpoint barrier remains intact. Recovery uses default three retries (5, 30, 120 seconds) and individual tool/provider safety timeouts; neither operates as a semantic reasoning deadline.

### 13.2 Council member

Member activity changes do not change logical identity. Session rollover preserves the member and branch.

A member cannot enter REVIEWING_PEER_WORK before the checkpoint runtime has verified authorized public publication of the frozen peer snapshot being reviewed.

A member cannot enter RESPONDING_TO_CHALLENGE for a challenge it is not authorized to see.

Checkpoint communication member states are AVAILABLE, WORKING, DONE, and DISCONNECTED. AVAILABLE may enter WORKING only through a bounded verification-only /work excursion. AVAILABLE may enter DONE only when required response obligations are satisfied, required messages are processed, accepted outbound delivery is settled, no verification work remains active, and the checkpoint generation/message frontier/obligation version in its completion certificate match current canonical state. A new required peer action moves DONE back to AVAILABLE. Unexpected connection loss moves the member to DISCONNECTED, never to DONE.

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


## 22. Checkpoint communication and peer-action contract

The authoritative communication architecture is defined in CHECKPOINT_COMMUNICATION_GATEWAY.md.

Agents do not receive a raw IRC channel/socket. They interact through a minimal Council-controlled local stream/client whose runtime-side bridge lives outside the agent-controlled execution environment.

Every accepted checkpoint message has:
- immutable server-assigned message_id;
- checkpoint_id;
- sender member identity;
- server timestamp;
- monotonically ordered checkpoint sequence;
- complete retained body;
- optional parent/reply message ID;
- delivery state.

Important communication may additionally be represented as a structured peer action. The structured representation is never a substitute for the original message body.

The originating Council member declares the action type explicitly through the Council communication command surface. The runtime tracks that declaration but does not intellectually classify ordinary messages using another model.

Large logical messages are transparently fragmented by the transport/runtime bridge and reassembled before acceptance. Fragmentation is not visible to the agent and does not create multiple Council messages. Partial/corrupt logical messages are not exposed as accepted communication.

Initial peer-action types:
- QUESTION
- CHALLENGE
- FINDING
- TEST_REQUEST
- TEST_RESULT
- PROPOSAL

A TEST_REQUEST asks the target peer to perform/consider a test but does not automatically create a task in that peer's branch. The peer may execute it, dispute it, defer it, or otherwise disposition it. The requester may independently test the target's checkpoint-visible repository in a separate disposable verification environment.

Every structured peer action retains or references:
- complete immutable full text;
- originating message_id;
- target member(s), if any;
- exact repo/commit/path/test/evidence references when supplied;
- response_required;
- current disposition;
- append-only addenda;
- reply/action relationships.

Initial dispositions:
- OPEN
- ACKNOWLEDGED
- RESOLVED
- DISPUTED
- DEFERRED
- WITHDRAWN
- NOT_APPLICABLE

Silence is never treated as resolution. Consensus is not required.

Ordinary messages may later be promoted into structured actions by immutable message ID. This lets agents converse naturally first and structure an important item afterward without losing any detail.

A /done request is not sufficient to hide an outstanding required action. The gateway must reject or warn on /done while required actions addressed to that member are OPEN or unacknowledged until the member explicitly responds/dispositions them. Informational actions need not block /done unless explicitly marked as requiring acknowledgement.

Reconnect/replay must restore both missed full messages and the member's current open-action queue.

Summaries, labels, embeddings, or model-generated descriptions are projections only. They are not authoritative replacements for original communication.

Checkpoint communication and execution are mutually exclusive **per Council member**, not globally. A member may leave AVAILABLE communication state for a bounded WORKING excursion using a command such as /work <action_id|reason>. While WORKING, that member cannot communicate live and does not receive interruptions. Other members may continue discussion; all messages/actions addressed to the working member are durably queued in sequence.

On work completion/failure/ceiling, the member returns to AVAILABLE and receives the complete queued logical messages plus its refreshed open-action queue before resuming discussion.

A work excursion is checkpoint-scoped, bounded, and verification-only. It runs against a frozen or disposable checkpoint snapshot and records the trigger, snapshot identity, timestamps, outcome, and temporary evidence. The authoritative candidate remains read-only during the excursion. Tests, reproduction, benchmarks, log inspection, existing-code execution, repository inspection, and output comparison are allowed. Candidate implementation resumes only after checkpoint communication closes. This prevents checkpoint discussion from turning into an endless live fix/review cycle. The runtime may enforce resource/time ceilings but does not decide whether the requested test is intellectually correct.

Initial checkpoint member activity states:
- AVAILABLE
- WORKING
- DONE
- DISCONNECTED

A new required action can move DONE -> AVAILABLE. Unexpected connection loss moves a member to DISCONNECTED, not DONE.


## 23. Checkpoint return packet contract

After checkpoint communication closes, each Council member receives a deterministic Checkpoint Return Packet for its next private phase.

The packet includes:
- checkpoint identity and milestone;
- the member's own frozen checkpoint snapshot;
- exact peer snapshots legitimately visible during the checkpoint;
- transcript index/reference rather than automatic full-transcript prompt injection;
- relevant structured peer actions and checkpoint dispositions;
- test results/findings/evidence produced during verification-only work;
- unresolved/disputed items;
- the member's own closeout statement.

The closeout statement is authored by the Council member, not generated by the runtime. It records what the member intends to carry forward, what evidence it accepts or disputes, and what it may investigate next.

Unresolved challenges and test results are revision inputs, not automatically created implementation tasks. They do not confer authority over another member's branch.

Peer snapshots legitimately seen at a checkpoint may remain available as frozen references/copies, but they never update after peer access closes.

The full checkpoint transcript remains durably retrievable. Default next-phase context should contain relevant actions, evidence, exact snapshot references, closeout, and transcript/message IDs; the full verbatim transcript is retrieved only when needed.

Structured peer actions retain their checkpoint history across later checkpoints without reopening the old communication session.


## 24. Final Part 4 closure registry

This section closes the remaining implementation-level ambiguity in Part 4 without specifying transaction-engine, queue, provider, container, retrieval, or frontend implementation internals that belong to later parts.

### 24.1 Actor/authority matrix

| Actor | May issue/perform | May not do |
| --- | --- | --- |
| User | approve/change/cancel project setup; answer interactions; pause/resume/stop runs; approve budget/permission expansion; accept/reject candidates | directly guide an individual Council branch during execution |
| Project Orchestrator | create/revise the canonical project contract; generate the project-specific checkpoint plan; process user clarifications | select winners, rank members, supervise solution reasoning |
| Council member | operate its own branch; delegate authorized workers; originate user questions; use checkpoint communication/peer actions; run verification-only checkpoint work; propose candidates | mutate another member's authoritative repo; bypass checkpoint boundaries |
| Worker | execute delegated work; return results; originate a user clarification when necessary | govern peers or canonical shared state |
| Runtime | enforce lifecycle/state/authorization; leases; checkpoint access; communication sessions; persistence; return packets | make intellectual judgments about solution quality |
| Auditor | verify protocol, authorization, isolation, and semantic fidelity | choose solutions or direct Council reasoning |

### 24.2 Schema/version rule

All command/event/interaction schemas carry `schema_version`. MVP begins at version `1`.

Unknown command types, missing required fields, invalid enum values, illegal transitions, stale target versions, and unauthorized actors are rejected before canonical mutation. A partially valid command never partially mutates canonical state.

### 24.3 Standard command result and error shape

Successful command result:

```text
CommandResult {
  command_id
  accepted = true
  target_id
  target_version?
  event_ids[]
  operation_id?
  data?
}
```

Rejected command result:

```text
CommandError {
  command_id
  accepted = false
  code
  message
  retryable
  current_target_version?
}
```

Canonical Part 4 error codes:

- AUTH_REQUIRED
- FORBIDDEN
- VALIDATION_FAILED
- UNKNOWN_COMMAND
- NOT_FOUND
- STALE_TARGET
- INVALID_TRANSITION
- IDEMPOTENCY_CONFLICT
- INTERACTION_CLOSED
- CHECKPOINT_NOT_ACTIVE
- MEMBER_NOT_AVAILABLE
- REQUIRED_ACTIONS_OPEN
- WORK_NOT_ALLOWED
- RESOURCE_LIMIT
- EXTERNAL_OUTCOME_UNKNOWN

Later parts may refine storage/retry implementation but must preserve these semantic distinctions.

### 24.4 Peer action semantics

The originating Council member explicitly chooses the semantic action type. Runtime does not use another model to classify ordinary conversation.

Required-response actions by default:
- QUESTION
- CHALLENGE
- TEST_REQUEST

Informational actions by default:
- FINDING
- TEST_RESULT
- PROPOSAL

A TEST_REQUEST is a request, not an automatically created task in another branch.

Action state and response obligation are separate. A target may fulfill its response obligation while the underlying action remains DISPUTED or otherwise intellectually unresolved. Consensus is never required merely to close a checkpoint.

### 24.5 Minimal peer command surface

The approved conceptual agent-visible commands are:

```text
/question
/challenge
/finding
/test-request
/test-result
/proposal
/reply
/dispute
/defer
/withdraw
/work
/done
/closeout
```

Exact local wire framing belongs to implementation. The semantic behavior above is authoritative.

### 24.6 Command -> event -> state/UI matrix

| Command / trigger | Durable event(s) | Canonical effect | Special UI effect |
| --- | --- | --- | --- |
| ApproveProjectContract | ProjectContractApproved; RunProvisioningStarted when immediate | approved revision becomes launch revision | approval interaction closes; provisioning visible |
| RequestProjectContractChanges | ProjectContractChangesRequested | Orchestrator returns to revision work | new revision later returns to approval |
| RejectProjectContractApproach | ProjectContractApproachRejected | current approach rejected, objective preserved | revision workflow |
| CancelProjectSetup | ProjectSetupCancelled | project CANCELLED | setup interactions close |
| PauseRun | RunPauseRequested | admissions stop; runtime quiesces controllable work | pausing state/banner, not yet PAUSED |
| confirmed durable pause boundary | RunPaused | run PAUSED | paused state/banner |
| ResumeRun | RunResumed | run ACTIVE | normal activity resumes |
| StopRun | RunStopRequested | run STOPPING | stop/cleanup status |
| TriggerCheckpoint | CheckpointTriggered | checkpoint TRIGGERED | checkpoint opening becomes visible |
| PublishCheckpointSnapshots | CheckpointSnapshotsAvailable | approved frozen local snapshot hashes and scoped read grants confirmed; source Git histories remain private | sealed-review UI available after opening guards |
| CreateCheckpointCommunicationSession | CheckpointCommunicationSessionCreated | checkpoint session initialized; shared communication remains gated during SEALED_REVIEW | independent-review controls only |
| SubmitIndependentCheckpointReview | IndependentCheckpointReviewSubmitted | immutable reviewer assessment recorded privately | own submission status |
| RevealCheckpointReviews | CheckpointPeerReviewsRevealed | all-five submissions revealed; SEALED_REVIEW -> REVIEWING | shared review controls active |
| SendCheckpointMessage | CheckpointMessageAccepted/Delivered | durable ordered transcript advances | message appears |
| CreatePeerAction | PeerActionCreated | peer action/obligation created | open-action queue updates |
| SetPeerActionDisposition | PeerActionDispositionChanged | obligation/action state changes | action state updates |
| StartCheckpointWorkExcursion | CheckpointWorkExcursionStarted | member AVAILABLE -> WORKING | member shown WORKING; messages queue |
| Complete/FailCheckpointWorkExcursion | CheckpointWorkExcursionCompleted/Failed | member WORKING -> AVAILABLE | queued messages/actions replay |
| MarkCheckpointCommunicationDone | CheckpointMemberMarkedDone | member AVAILABLE -> DONE | member shown DONE |
| new required action to DONE member | CheckpointMemberReactivated | DONE -> AVAILABLE | member active again |
| SubmitCheckpointCloseout | CheckpointCloseoutRecorded | immutable member closeout retained | closeout status visible |
| CloseCheckpointCommunicationSession | CheckpointCommunicationSessionClosed | no new live checkpoint communication | communication controls disappear |
| RevokeCheckpointSnapshotAccess | CheckpointSnapshotAccessRevoked | checkpoint read-grant/routes revoked and isolation verified; previously seen material cannot be made unknown | visibility status updated; new private work still waits for CLOSED |
| CreateCheckpointReturnPacket | CheckpointReturnPacketCreated | deterministic next-phase context created | no blocking UI |
| CloseCheckpoint | CheckpointClosed | checkpoint CLOSED; private revision resumes | checkpoint history finalized |
| CreateInteractionRequest | InteractionRequested | durable user gate/question created | Interaction Center + blocking surface when configured |
| RespondToInteraction | InteractionAnswered | interaction resolves and domain action proceeds | decision surface closes |
| MarkCandidateReadyForReview | CandidateReadyForReview | candidate enters configured review gate | final-review surface when applicable |
| AcceptCandidate | CandidateAccepted | user accepts candidate | finalization begins |
| RequestCandidateRevisions | CandidateRevisionRequested | candidate returns to revision | revision state |
| RejectCandidate | CandidateRejected | candidate rejected | review state updates |

All other commands/events use normal lifecycle/activity/history projection without requiring bespoke UI behavior.

### 24.7 State Contract simplification

Part 4 does not require a manually duplicated prose document for every ordinary activity code.

Implementation uses:
1. common State Contract defaults;
2. the transition rules and matrices in this document;
3. explicit overrides only for states that block the user, expose peer information, perform external side effects, or require special recovery.

Ordinary activities inherit:
- no blocking UI unless an interaction request exists;
- runtime-owned canonical state;
- explicit failure recording;
- parent-scope pause/cancel behavior where safe;
- resumability according to the operation safety contract.

### 24.8 Part 4 completion boundary

The original Part 4 baseline specified the following boundaries. The October 13 state/command refinements required reconciliation; **Section 26 now supplies the missing typed registry, actor/guard and state contracts**, so Part 4 is DESIGNED as a specification (not an implemented registry or passing test suite):
- who may issue an action;
- whether it is legal in the current state;
- what durable event follows;
- what canonical state change follows;
- whether a user interaction is required;
- how stale/idempotent requests are treated;
- how uncertain external outcomes are represented;
- how checkpoint communication, verification work, closeout, and return behave.

Transaction mechanics, conflict algorithms, queue internals, provider behavior, environment technology, graph implementation, retrieval, and API/frontend implementation details remain intentionally delegated to Parts 5+.

## 25. October 13 required state-contract refinements

Communication completion, verification coverage, candidate readiness, and user acceptance are separate records. DISPUTED or DEFERRED can satisfy a response obligation without resolving the underlying risk or passing an acceptance criterion. Required checks remain NOT_RUN, BLOCKED, FAILED, or PASSED with evidence; an explicit policy waiver is recorded separately and is never a test pass. Forced closure records incomplete review and outstanding obligations.

MarkCheckpointCommunicationDone carries checkpoint_generation, processed_message_sequence, and expected_obligation_version. Under the same checkpoint lock/version guard used to accept messages/actions and close the checkpoint, reject stale declarations, unanswered required obligations, unprocessed required messages, or active verification work. A relevant accepted message or new required action invalidates the affected DONE certificate and reactivates that member. Delivery to a socket is not evidence of processing. Internal bookkeeping alone must not endlessly invalidate completion. Close atomically only after current certificates cover the current review/obligation frontier; record ceiling-forced closure distinctly.

The UI and final review expose communication_closed, verification_coverage, candidate_readiness, and acceptance_decision independently. An incomplete candidate may be presented for an informed user decision where the existing contract allows it; presentation or acceptance does not alter failed/unperformed verification.

Checkpoint milestones specify outcomes/evidence to review, not a preferred sequence of solution components unless the user required those components. For example, require a reproducible baseline and measured failure modes rather than requiring every retrieval design to add reranking and fusion.

Processed clarifications retain links to source user statements, scope, semantic strength (preference, requirement, permission, prohibition, or unresolved ambiguity), and the exact contract revision. Raw answers remain retained for authorized audit/user confirmation, not delivered directly to agents. Material ambiguity and consequential changes to permissions, spending, publication, or requirements require the appropriate explicit confirmation. Ordinary faithful rewording does not add an Auditor bottleneck.

Branch-local clarification context stays branch-local in the Orchestrator's memory, retrieval, caches, and later normalization, not just in outgoing messages. Only approved project-wide revisions enter shared clarification context. The Orchestrator still has no solution-selection or intellectual supervisory authority.

Additional contract payloads:

- SubmitIndependentCheckpointReview: checkpoint_id/generation, reviewer identity, frozen candidate references, immutable assessment/evidence, idempotency key. Legal only in SEALED_REVIEW for the submitting member; it emits IndependentCheckpointReviewSubmitted without peer delivery.
- RevealCheckpointReviews: expected checkpoint generation and required submission IDs/hashes. Runtime-only, all-five guard, atomic visibility/delivery activation plus CheckpointPeerReviewsRevealed. No model selects which reviews to reveal.
- MarkCheckpointCommunicationDone: processed_message_sequence and expected_obligation_version as well as checkpoint generation. A stale frontier returns STALE_TARGET or REQUIRED_ACTIONS_OPEN, never successful DONE.
- PublishCheckpointSnapshots / RevokeCheckpointSnapshotAccess: customer-approved local snapshot manifest, repository commit/tree hashes, selected files/artifacts, recipient grants/revocation operations, exact desired and observed access state. A requested transition is not its completion event.
- PauseRun first stops new ordinary admissions and quiesces; RunPaused is emitted only once the required pause boundary is actually reached. Unknown external requests remain separately recorded. StopRun does not claim external cancellation merely from local revocation.

Command/result schemas, registry wiring, UI mappings, and deterministic tests for these additions remain pending implementation. No new completion status is asserted by this amendment.

### Pause-request contract refinement

QUIESCING_FOR_PAUSE is runtime-owned activity entered by an authorized PauseRun or recorded safety trigger. It immediately closes ordinary work admission; fencing, safe persistence, reconciliation, and cleanup remain allowed. The UI shows pausing with affected members/operations and StopRun available, without a new blocking dialog. Repeated pause requests deduplicate. RunPaused is emitted only after the required controllable execution boundaries have quiesced and durable state is recorded; unknown provider outcomes remain visible independently. StopRun supersedes pending pause with STOPPING. Quiescence failure/ceiling records a blocked or failed pause operation rather than falsely declaring PAUSED; scope-specific recovery is governed by Part 7. ResumeRun is available only after PAUSED and current safety/authority/budget guards pass. No runtime implementation or test completion is implied.


## 26. October 14 Part 4 design closure — typed protocol and state/authority matrix

**Part 4 is DESIGNED as a typed behavior specification only.** The October 13 state refinements and Step 7 integration above are authoritative; this section specifies missing payloads, actors, guards, events, transitions and interaction behavior without implementing the agent loop (Step 8), provider adapters (Step 9), sandboxes (Step 10) or frontend transport (Step 12). No runtime or state-machine tests have been run.

### 26.1 Common envelope, result, and error policy

The canonical command envelope in Sections 5 and 24.3 is v1 and must carry `command_id`, `command_type`, `schema_version`, `actor_type/id`, `project_id`, `run_id` when relevant, `branch_id`/seat scope when relevant, `target_type/id`, expected version/hash for mutable or revision-pinned targets, `idempotency_key`, correlation/causation IDs, and typed payload. Typed errors preserve AUTH_REQUIRED, FORBIDDEN, VALIDATION_FAILED, STALE_TARGET, INVALID_TRANSITION, IDEMPOTENCY_CONFLICT, REQUIRED_ACTIONS_OPEN, EXTERNAL_OUTCOME_UNKNOWN and RESOURCE_LIMIT, with additional precise errors `BUDGET_EXHAUSTED`, `STALE_EXECUTION_EPOCH`, `PUBLICATION_UNSAFE`, `PUBLICATION_NOT_VERIFIED`, `SEALED_REVIEWS_INCOMPLETE`, and `ARCHIVE_VALIDATION_INCOMPLETE` where appropriate.

- Only the **user** may approve/revise permissions, Project Contract, phase/run budgets, separately requested optional external-publication exposure and final acceptance; the **Orchestrator** prepares contract revisions and neutral semantic milestones; the **member** alone authors intellectual readiness, original review, challenges and closeout; the **trusted runtime** verifies mechanical state, delivers events, reconciles effects and performs authorized transitions. Auditor flags protocol/semantic-fidelity violations, not solution quality.
- A command requests an operation. `*Requested`/`*Started` records and desired external status are distinct from `*Succeeded`/`*Published`/`*Private` verification events. The runtime cannot emit success from an API timeout or requested transition.
- Activity code, lifecycle, operation state, member checkpoint communication state, independent-review status, verification coverage, budget exhaustion and user acceptance remain **different concepts**. No activity label alone grants capability, publishes data or opens a user dialog; only a durable `interaction_request` invokes blocking user input.

### 26.2 Typed command -> guarded effect -> event matrix

The following is the normative completion of the existing catalog. Payloads and their target versions are mandatory when listed; named transition events are emitted only on the recorded guard being satisfied. Internal adapter commands may be split by endpoint but retain the same semantic contract.

| Command / owner | Required payload + guard | Canonical event and state effect |
| --- | --- | --- |
| `ApproveProjectContract` / user | exact contract revision/hash, live PROJECT_CONTRACT_APPROVAL request, explicit accepted run/budget/permission/semantic-phase configuration | `ProjectContractApproved`; creates/activates approved revision and (when immediate) PROVISIONING run atomically with the resolved interaction; later external setup via durable operations |
| `ApproveRunBudgetPolicy` / user | exact run/contract revision, prior policy version, run ceiling, **approved** development/review/finalization pools and member/phase token+cost caps; optional suggested 70/25/5 is not authority | `BudgetPolicyApproved`; append immutable budget policy revision; revalidate all outstanding reservations before reallocation; no automatic top-up |
| `RecordMemberCheckpointReady` / member-originated, trusted gateway | member/seat, current phase/checkpoint generation, authored readiness outcome, candidate frozen repo SHA/snapshot/evidence refs; mechanical metadata valid and correct owner | `MemberCheckpointReady`; immutable per-generation arrival; never runtime-assigned intellectual completion; fifth valid distinct arrival makes checkpoint eligible to trigger but does not publish it |
| `RecordMemberPhaseBudgetExhaustion` / runtime | approved phase policy, available/settled/reserved usage, exhausted scope and unfinished member state | `MemberPhaseBudgetExhausted`; member remains BUDGET_EXHAUSTED / INCOMPLETE and must not satisfy a checkpoint/accepted-candidate barrier |
| `ReserveModelCallAllowance` / trusted runtime | operation identity, requester/parent, model/profile/phase, fixed-precision token+cost bound, all pool/member/run caps and resource ceiling checks | `BudgetReservationCreated` + requested operation/outbox in one transaction; call dispatched only after commit; uncertain dispatched liability retained |
| `RecordBudgetReservationSettlement` / trusted runtime | original operation/attempt, current authorization epoch for effects, actual usage or explicit unknown/reconciliation evidence | `BudgetReservationSettled` or `BudgetReservationOutcomeUnknown`; balances updated atomically, never refund unknown dispatched use |
| `PublishCheckpointSnapshots` / trusted runtime with exact user approval | five arrivals, frozen snapshot SHAs, approved local read-only snapshot manifest/hash and intended recipients, passed scope/sensitivity checks | first schedules local snapshot export/grant operations; **only observed verified export hashes and scoped read access** emit `CheckpointSnapshotsAvailable`, enables SEALED_REVIEW; partial/unknown leaves OPENING guarded |
| `SubmitIndependentCheckpointReview` / each member | SEALED_REVIEW, current generation, exact frozen peer candidate set, own authored assessment and evidence hash | `IndependentCheckpointReviewSubmitted`, immutable and visible only to own reviewer/trusted runtime before reveal |
| `RevealCheckpointReviews` / runtime | all five distinct valid current-generation sealed submissions; consistent pinned candidate set; no leakage | one `CheckpointPeerReviewsRevealed` atomic visibility/delivery activation; SEALED_REVIEW -> REVIEWING; missing reviewer stays blocked/aborted explicitly |
| `SendCheckpointMessage` / available member | active REVIEWING session and execution bridge/epoch, complete verified logical message; optional target refs | `CheckpointMessageAccepted`; one immutable full body/sequence, no delivery guaranteed merely by acceptance |
| `CreatePeerAction` / member | explicit action type and original message reference, targets, response requirement, full body/evidence | `PeerActionCreated` + recipient obligations; TEST_REQUEST never auto-creates target branch work; delivered/processed frontiers advance separately |
| `MarkCheckpointCommunicationDone` / member | checkpoint/generation, processed message sequence, obligation version, accepted-outbound delivery frontier, no active verification work | `CheckpointMemberMarkedDone`; version-bound DONE certificate; stale frontier or unaddressed required obligations reject |
| `ReopenCheckpointCommunicationMember` / runtime | new accepted required message/action for DONE member under checkpoint lock | `CheckpointMemberReactivated`; invalidate affected DONE certificate, schedule same member for re-entry, preserve prior discussion history |
| `RevokeCheckpointSnapshotAccess` / runtime | CLOSING, verified revoke operations for all selected checkpoint peer snapshot grants/routes and removed temporary gateway authority | `CheckpointSnapshotAccessRevoked` only after verified grant/route revocation; previously received material cannot be unlearned; failure blocks private work |
| `CloseCheckpoint` / runtime | current DONE frontiers or explicitly recorded forced-incomplete closure, persisted closeouts, complete transcript reference, verifier finish/ceiling, checkpoint snapshot grant/route revocation confirmation, created return packets | `CheckpointClosed` and CLOSED only after local and external preconditions are confirmed; private phase can resume. Forced incomplete close cannot masquerade as passed verification |
| `RequestUserInput` / member or worker via runtime | scoped clarification, request text, parent agent/branch, question ID, blocked dependency | `InteractionRequested`; user RAW response retained, Orchestrator processes within **approved requesting-branch** and global context, and only PROCESSED answer delivered; consequential scope changes require confirmation |
| `PauseRun` / user or safety trigger | ACTIVE run, exact run version; closes new ordinary admissions immediately | `RunPauseRequested`, ACTIVE with QUIESCING_FOR_PAUSE activity; only verified durable quiescence produces `RunPaused`/PAUSED |
| `ResumeRun` / user | PAUSED, approved contract/budgets/permissions, provider credentials, sandbox checks, current epoch and affected unknown operations reconciled or safely gated | `RunResumed`, ACTIVE with fresh scoped bridges, otherwise stays PAUSED |
| `StopRun` / user | ACTIVE/PAUSED, versioned stop request and authority | `RunStopRequested`, STOPPING; clean confirmed teardown -> `RunCancelled`, unsafe/incomplete cleanup -> `RunFailed` with unresolved effects listed |
| `AcceptCandidate` / user | live FINAL_CANDIDATE_REVIEW interaction bound to exact candidate SHA, limits/verification disclosures and authorized retention decisions | `CandidateAccepted`; schedules separate verifiable archival/teardown operations; NOT equivalent to StopRun and not completed finalization merely on acceptance |
| `FinalizeCandidate` / runtime | accepted candidate, exported Git/evidence manifest and fresh-checkout reference closure validated, unresolved consequential obligations handled, explicit repo retention/visibility authorization, Council runtime cleanup verified | `CandidateFinalized`, `RunCompleted`; cleanup failures remain FINALIZING/FAILED as appropriate, never fictitious completion |

### 26.3 Independent review and version-bound communication closure

- `CHECKPOINT_READY` is authored per member for the **Orchestrator-proposed, user-approved outcome phase**, not generated by an optimizer, runtime or /done. The five-arrival barrier is separate from entering OPENING, verified customer-local snapshot grants, SEALED_REVIEW and REVIEWING.
- SEALED_REVIEW is a **strict privacy barrier**: peer assessments and the shared debate stream stay unavailable across DB queries, graph/RAG, caches, SSE, Git and UI until all five reviewers submit and one atomic RevealCheckpointReviews succeeds. Read-only candidate snapshots alone are not permission to reveal sealed review text.
- All messages carry a server-assigned checkpoint-local ordered sequence. Every peer action retains its original complete message; typed action is an attributed *member declaration*. Required responses may be ACKNOWLEDGED, DISPUTED, DEFERRED, etc., without marking underlying test coverage PASSED or consensus reached.
- DONE is **checkpoint communication state only**. Under one checkpoint generation/frontier lock, it requires no undelivered outbound accepted messages, no unprocessed required messages, no outstanding required response obligations, no active `/work`, and current expected obligation version. A new relevant accepted required action invalidates the certificate and returns DONE -> AVAILABLE. Mere keepalives/internal bookkeeping do not invalidate it. `/work` uses a separate disposable verifier, never modifies authoritative candidate.
- Normal CLOSING requires current DONE certificates for all five and no pending communications/verification work, plus member-authored closeouts, durable message/action index and verified closure of temporary snapshot access. An explicitly bounded forced close records who/what is incomplete and never pretends five DONE messages or passing tests existed.

### 26.4 Clarification, budget, retention and SSE state guards

- A structurally valid user question raised by member/worker must not receive an Orchestrator **intellectual veto**. Persist RAW answer separately, process faithfully with locators/semantic strength/scope, and create a new versioned Project Contract approval gate for consequential changes. Branch-private Orchestrator clarification cache and derived retrieval artifacts follow requesting-branch scope.
- Permission expansion, optional external-publication authorization, local snapshot scope approval, budget policy change and candidate acceptance are independent, explicit **user decisions** tied to exact target revisions/hashes. Browser dismissals and SSE replay do not count as decisions. Same actor/scope/idempotency key/hash returns the original result before stale-version checks; key/hash disagreement returns IDEMPOTENCY_CONFLICT.
- A budget-reserve failure produces `RESOURCE_LIMIT` / `BUDGET_EXHAUSTED` with current remaining/reserved and an optional durable user budget-expansion interaction. Users may approve different limits; neither Orchestrator nor agent grants money. BYOK credits/wallet billing is not an MVP domain action.
- An execution bridge epoch revocation blocks **new authorization**, not proof that an external provider call was cancelled or free. Unknown effects are stateful Part 5 operations; only applicable dependents block. Activity/coverage/verification/candidate acceptance are reported separately.
- SSE clients first obtain a canonical scope-filtered snapshot and its committed event watermark from one database snapshot, then subscribe/replay **after** that position; duplicate/out-of-order events are deduped and replayed from canonical history. Private/hidden events cannot leak by position gaps or change-event payloads. A UI cannot optimistically mark external PUBLIC/PRIVATE, archive, or acceptance events successful before canonical observation.

### 26.5 Required deterministic tests (not run)

- Idempotent replay of a successful contract approval returns the saved response despite later run state; conflicting same-key payload rejects; no duplicate run or checkpoint snapshot export/grant.
- Five valid member readiness records are required; BUDGET_EXHAUSTED or FAILED members cannot advance the arrival barrier, sealed review reveal, or final acceptance.
- Simultaneous fifth sealed submission/reveal cannot emit partial assessment disclosure or a duplicate reveal; branch-local/private caches and Git never leak sealed reviews early.
- Message acceptance, new required action and /done race under the same guard: no lost obligation, invalid DONE certificate, false checkpoint closure or stale reactivation.
- Unknown provider/local snapshot grant-revoke/optional external Git/host operation never emits a successful observation event. Stop/Resume/Pause recovery behaves according to the true state, not the last UI projection.
- All four user Project Contract decisions and budget/permission/candidate decisions are target-version pinned and reconnect-safe. No raw answer delivered directly to a member; local clarifications cannot appear in other members' contexts.
- A report shows verification NOT_RUN/BLOCKED/FAILED independently of DISPUTED/DEFERRED communication and user acceptance. Forced checkpoint close remains explicit incomplete.
- Event snapshot/SSE replay is committed-order safe, authorization-filtered and independent of transport reconnects.

### 26.6 Completion boundary

This captures the previously DESIGNED Step 4 baseline. **ADR-17 reopens the repository/snapshot command, grant, consent and closure integration**, while existing actor, idempotency and peer-review semantics remain specified. No part is IMPLEMENTED or VERIFIED. The precise endpoint framing, generated DTO code, tests, model adapters, checkpoint gateway implementation and user interface remain future work. The current Part 4 registry is a specification, not a deployed service.


## 27. Accepted Step 8.2 resource-monitor and worker-authority refinement (design only)

**Step 4 remains DESIGNED** as the authority/state specification. The owner-approved Step 8.2 policy clarifies that ordinary subprocesses and AI subagents created **inside** an authorized Council-member sandbox are not automatically new centrally scheduled Worker entities or Docker containers; there is **no Council-fixed internal worker count or delegation-depth cap**. `CreateWorker` remains the typed command for workers that need Council-canonical task identity/operation attribution, not an interception requirement for every `fork`/local subprocess.

The trusted runtime, not the member model, monitors aggregate sandbox resource use via Docker Engine's stats/oom/die interface and optional host/VM/disk/GPU adapters. New authoritative resource event families (added to the catalog) are:

- `MemberSandboxResourcePressureDetected`: trusted policy-level transition SOFT (~80% assigned memory cap) or HIGH (~90%), measured/limit values and incident ID, configuration version, timestamp and affected **whole sandbox**. A raw telemetry sample alone does not emit a canonical event.
- `MemberSandboxOOMObserved`: actual backend OOM/die event with sandbox/epoch, last known measurement and recoverability; it never means CHECKPOINT_READY, cancellation of pending provider calls or safe resource release.
- `MemberResourceMonitoringUnavailable` / `MemberResourceMonitoringRestored`: stale/available observation boundary; affected **new** heavyweight broker admissions are gated while measurements are unsafe, without falsely marking an existing logical member complete/failed.
- Existing `ResourceAdmissionDenied`, `SandboxQuiesced`, `SandboxResourceReleaseConfirmed`, `MemberRecoveryAttempted`, `MemberBlocked` and bridge fencing events govern actual interventions/recovery. Merely crossing 80% does not authorize killing a member.

**State/UI rule:** the Council dashboard may display measured aggregate usage, limits, freshness, pressure and actions; show missing metrics as unknown rather than zero. Warnings are informative unless a genuine user decision (new permission/budget/host authorization) is required. The runtime may throttle **trusted gateway/broker operations**, initiate safe whole-sandbox quiescence or block a new member admission, but cannot claim to micromanage every internal worker fork. External Docker resource release needs observed backend evidence under Part 5; incomplete safe quiescence remains explicitly unresolved.

**Security rule:** no agent-controlled sandbox or worker receives raw Docker Engine socket/API credentials. Optional isolated child containers require a separately authorized trusted broker and count against the parent's aggregate resource vector; child workers cannot expand parent spending, visibility or reviewer authority.

**Verification boundary:** typed DTO/handler generation, external Docker metrics/oom integration, Windows Docker Desktop WSL2/host checks, supported GPU accounting and actual pressure/OOM/lease tests are **NOT STARTED / NOT RUN**. These new events are a specification update, not executable implementation.

## October 15 Step 4 architecture integration — unified trust, OpenAI Moderation and command-only artifacts (approved direction; design only)

See [deployable design](STEPS_3_TO_5_DEPLOYABLE_ARCHITECTURE_2026_10_15.md). The owner selected a **unified logical trusted control plane** with separate privileged service boundaries, a customer-hosted **OpenAI Moderation API** classification layer for semantic boundary content, and **typed-command-only member exchange**. This is not permission to let an LLM model issue file transfers, judge outcomes, receive secrets, or bypass deterministic identity, recipient, checkpoint, authorization and egress guards.

Member-visible peer command surface is limited to text-only SendCheckpointMessage, server-issued ListCheckpointObjects and RequestCheckpointContent on approved immutable checkpoint manifests, and existing member-authored review/action/WORK/DONE commands. No SendFile, arbitrary recipient attachment/upload, member-chosen raw host path transfer, direct peer socket, or writable Git mount. A trusted server resolves/returns only approved objects and ranges; file/artifact responses never contain or automatically trigger chat messages. Any subsequent peer discussion is a distinct authorized chat command. A narrow semantic question remains whether the owner meant a stronger temporal ban on later messages; do not silently invent one.

For semantically significant inputs/outputs, record deterministic authority check followed by guard policy classification and actual enforcement disposition (ALLOW/BLOCK/REVIEW/UNAVAILABLE), pinned to model/policy revision, content or command hash, epoch, contract and checkpoint generation. Guard ALLOW is not proof of safe code/files or successful external operations. Failures stop new affected guarded operations and preserve explicit exceptions/reconciliation, while maintaining valid old canonical history. Preserve five sealed reviews, exact candidate set, obligation frontier, /work verification-only and contextual dissent.

**STATUS:** accepted architecture direction, exact wire DTOs, prompts/policy taxonomy, artifact transfer result/framing and semantic guard admission **IN DESIGN**. No implementation or tests requested/performed.

## October 15 approved Step 8.3 and Orchestrator library interfaces (no implementation)

**Step 8.3 approved design direction:** reuse `RecordMemberCheckpointReady`, `MarkCandidateReadyForReview`, existing escalation/blocked states, and `RecordMemberPhaseBudgetExhaustion` under current actor/epoch, phase/version and idempotency guards. Store **member-authored readiness intent** separately from **observed mechanically verified frozen candidate/evidence + whole-member safe suspension**; only the latter is a valid five-seat checkpoint arrival. A worker or trusted runtime cannot author intellectual readiness. New distinct **CONCLUDED_NO_VIABLE_CANDIDATE** outcome is evidence-scoped and honest, neither a passing implementation nor an automatic skip of required checkpoint/final-review participation. The exact typed event/result schema and final Step 8.4 intake remain IN DESIGN. Existing /done communication certificate is not readiness/acceptance.

**Orchestrator approved planning-input extension:** versioned permitted development-pattern library entries may inform the neutral semantic checkpoint plan. The library's IDs/content hashes and applicability/provenance belong in the **existing Project Contract/checkpoint-plan versioning**, not a new approval authority. When there is no usable match, Orchestrator still creates a requirements-derived plan for user approval. A template never controls candidate algorithms or implementation stack. Preserve the same five-member autonomy, formal approval and typed project revision semantics.

See [Step 8.3](STEP_8_3_MEMBER_PHASE_COMPLETION_AND_READINESS.md) and [planning library](ORCHESTRATOR_DEVELOPMENT_PATTERN_LIBRARY.md). **Architecture only, no commands generated or tests run.**

## 27. Local-first checkpoint interaction amendment (ADR-17/18; design integration open)

**New authoritative gateway contract:** [LOCAL_REPOSITORY_AND_KNOWLEDGE_RETENTION.md](LOCAL_REPOSITORY_AND_KNOWLEDGE_RETENTION.md). The MVP checkpoint publication is now a **customer-local selected frozen read-only snapshot**, not a GitHub PUBLIC transition. `PublishCheckpointSnapshots` requests export/hash verification and explicitly scoped recipient read grants, with confirmed `CheckpointSnapshotsAvailable` only after externally verified safe access. `RevokeCheckpointSnapshotAccess` requests local permission/mount/route teardown; only observed closure emits `CheckpointSnapshotAccessRevoked`. Desired action != confirmed physical access. Optional externally public publication remains a *different* separately authorized action/operation and is absent by default. Old public-GitHub event meanings are legacy/superseded, not renamed external proofs.

User gates for **retention/share** are separate from checkpoint peer-grants: customer-specific archive retention is policy-bound, and customer-derived general knowledge release outside the tenant needs its own specific informed approval, content/access scope, privacy/IP/license review and idempotent decision record. Approved scoped local snapshots are not consent to vendor access or cross-customer lesson export.

**Step 11 retrieval behavior (design direction):** authorized memory search presents context-relevant working approaches first; prior failures are `FAILED_IN_CONTEXT` observations and test ideas, never automatic universal blacklist verdicts. Agent intellectual discretion and independent hypothesis testing remain intact. Ranking and enforcement implementation/tests are pending.

**Step 4 integration status:** REOPENED IN DESIGN only for these affected typed operations and user sharing/consent semantics; no production gateways, DTOs, or runtime tests have been executed.


**October 15 ADR-22 correction (authoritative):** The owner's intended safeguard is the **hosted OpenAI Moderation API** (`omni-moderation-latest`) called over HTTPS from the trusted backend, **not** any local/open-weight GPT-OSS model. It is free for API users but requires API credentials, internet and allowance for rate limits. Submitted content leaves the customer environment: require separately approved provider/data-category egress BEFORE the call, including for company source or customer records. The endpoint classifies supported **text/images** and returns moderation categories/flags; it is **not** an arbitrary custom-policy, prompt-injection, exfiltration, binary/malware or deterministic authorization engine. Local read grants, sandbox isolation, content hashes, and customer permissions remain mandatory. No silent fail-open on moderation refusal/outage, no silent upload without customer authorization. See [ADR-22 correction](OPENAI_MODERATION_API_CORRECTION.md). Specification direction only; no implementation or tests.
