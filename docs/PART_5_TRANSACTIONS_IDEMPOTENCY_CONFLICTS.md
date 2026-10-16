# Part 5 - transactions, idempotency, and conflict handling

**October 13, 2026 amendment:** [decision/status index](ARCHITECTURE_DECISIONS.md). Requirements below are specifications; application implementation is NOT STARTED and runtime tests are NOT RUN.

**Design status:** BASELINE DESIGNED; **ADR-17 local snapshot operations and retention REOPENED IN DESIGN**. Unchanged event-clock, spend, idempotency, UNKNOWN semantics remain specified.  
**Scope:** consistency and retry semantics for active Council deployments.  
**Implementation:** NOT STARTED. **Concurrent/recovery/runtime tests:** NOT RUN.

## 1. Core rule

PostgreSQL is the canonical source of truth for an active Council project.

> Local canonical changes are atomic. Commands are idempotent. Mutable writes prove which version they acted on. External effects are durable operations. Unknown external outcomes are reconciled rather than guessed.

This part deliberately does not introduce distributed transactions, CRDTs, Kafka, a generalized saga engine, or automatic semantic conflict merging.

## 2. Canonical transaction boundary

A command whose authoritative effects are entirely inside Council PostgreSQL executes in one transaction:

```text
authenticate actor / authorize scope, validate schema and canonical request hash

BEGIN
  lock deployment event-clock row first (before aggregate/budget locks)
  find scoped idempotency receipt under unique-key serialization
  if same key/hash: return original authorized receipt without re-execution
  if same key/different hash: return IDEMPOTENCY_CONFLICT
  for new command: check expected target version and transition guards
  lock/update affected aggregates and budget/resource scopes in deterministic order
  mutate canonical state / persist external-operation INTENT where needed
  allocate ordered event position(s) from the locked transactional event clock
  append immutable durable event(s), outbox entry/entries and command receipt/result
COMMIT

perform external effects only from committed durable operation records

```

Any failure before commit rolls back the complete canonical change.

Important atomic groups include:

- user response + interaction resolution + corresponding domain decision;
- Project Contract approval + launch revision activation + run creation/provisioning + events;
- project-wide contract revision activation + intended branch delivery records;
- checkpoint opening INTENT + five frozen **local Git** tree/commit IDs + approved snapshot-export/recipient access manifests + durable operations/events; **SEALED_REVIEW follows only externally verified content-hashed read-only local snapshot grants**, never assumptions from the SQL intent;
- checkpoint closing INTENT + version-bound DONE/frontier guards + durable transcript/closeout references + local snapshot grant-revocation operations; **CLOSED/return packets require confirmed revocation and gateway isolation**, not merely a requested cleanup;
- candidate acceptance + accepted-candidate record + archival/teardown scheduling;
- claim revision + essential provenance relationships + event.

External side effects never occur inside the SQL transaction.

## 3. Idempotency

Every retryable command carries an `idempotency_key`.

Council stores, within the temporary project control database:

- actor/scope;
- command type;
- idempotency key;
- canonical request hash;
- resulting target/version where relevant;
- result payload;
- emitted event IDs;
- operation ID where applicable.

Rules:

```text
same key + same canonical request
-> return the original result
```

```text
same key + different canonical request
-> IDEMPOTENCY_CONFLICT
```

Idempotency applies at minimum to user decisions, task creation, worker creation where retryable, checkpoint lifecycle commands, model requests where the provider contract allows safe identity/reconciliation, sandbox/tool operations, repository-access operations, and other externally retryable commands.

Idempotency records exist only for the lifetime of the active Council project unless deliberately distilled into accepted-project learning.

## 4. Optimistic concurrency

Mutable canonical rows carry `row_version` or an equivalent expected-version field.

A mutable write is conditional:

```text
UPDATE target
SET ..., row_version = row_version + 1
WHERE id = :id
  AND row_version = :expected
```

If no row matches, return `STALE_TARGET` and reload canonical state. Do not silently overwrite.

Immutable/versioned records are appended rather than rewritten. Concurrent version creation uses a uniqueness constraint such as `UNIQUE(parent_id, version_no)`; on conflict, re-read the current version and retry only if the command remains valid.

MVP conflict outcomes are intentionally simple:

- no conflict -> commit;
- stale mutable state -> reject and reload;
- immutable/versioned evolution -> append a new version, never overwrite history.

No CRDTs or automatic semantic merges are required.

## 5. Durable external operations

Any action outside PostgreSQL is represented by a durable operation before execution.

Examples include:

- local frozen Git snapshot export, read-grant and revocation operations (plus optional separately authorized external Git/publication actions);
- model-provider requests;
- sandbox/container operations;
- privileged broker actions;
- external tools/APIs;
- filesystem effects outside the transactional database boundary.

Minimum operation state:

```text
PENDING
RUNNING
SUCCEEDED
FAILED
UNKNOWN_PENDING_RECONCILIATION
```

An operation records at minimum:

- operation_id;
- operation_type;
- operation_key;
- project/run/branch scope;
- target;
- canonical request hash;
- status;
- attempt_count;
- timestamps;
- latest known result/error;
- reconciliation metadata when applicable.

`operation_key` prevents accidental creation of multiple logical operations for one intended effect.

Individual attempts are append-only children of the logical operation so retry history is not lost.

## 6. Unknown external outcomes

A timeout or lost connection after an external request does not prove failure.

Example:

```text
Council -> trusted local snapshot gateway: grant Member 2 read access to approved frozen Member 1 snapshot
Gateway may have granted access
connection fails before response
```

Council records:

```text
UNKNOWN_PENDING_RECONCILIATION
```

Then reconciliation checks the external system where possible:

```text
effect already present -> SUCCEEDED
effect definitely absent -> safe retry if allowed
still unknowable -> remain UNKNOWN_PENDING_RECONCILIATION
```

Council must never convert an unknown external outcome into success merely because a retry was attempted.

Exactly-once execution is not claimed unless the external system itself provides a contract that makes that claim valid.

## 7. Task leasing and zombie-worker protection

Executable tasks use atomic leasing. PostgreSQL `FOR UPDATE SKIP LOCKED` is the initial mechanism.

A live lease contains at minimum:

- task_id;
- lease_owner;
- lease_token;
- leased_at;
- expires_at;
- heartbeat_at;
- attempt number.

Only one live lease may own an executable task at a time.

Task completion/failure must present the current lease token. If a lease expires and another worker receives a new lease, an old worker cannot later overwrite the newer result with its stale lease token.

Waiting tasks release scarce execution capacity.

## 8. Transactional outbox

Every canonical transaction that creates externally observable events writes the corresponding outbox rows in the same PostgreSQL transaction.

```text
canonical mutation
+ audit/domain event
+ outbox entry
= one commit
```

Publishing to SSE/workers happens after commit.

If Council crashes after the database commit but before publication, the unpublished outbox row remains and is delivered after restart.

Consumers must tolerate repeated delivery and use event/message identity for deduplication.

## 9. Projection consistency

Derived views may lag canonical state, including:

- UI projections;
- search indexes;
- graph projections;
- counters/analytics.

Each projection tracks a processed event position or equivalent watermark.

The system must not represent a projection as current beyond its processed position. If canonical state is at event 1050 and a graph projection is at 1046, consumers can distinguish that lag rather than assuming events 1047-1050 are already represented.

## 10. Council database lifetime

Each active Council deployment owns its isolated PostgreSQL control database inside the deployment's trusted sandbox boundary.

The database may persist across crashes/restarts while the project is active.

After user acceptance:

1. export and verify the accepted project;
2. export and verify the Git-backed reusable learning package;
3. ensure the accepted product no longer depends on Council control infrastructure;
4. destroy the Council control PostgreSQL volume and remaining runtime state.

A database that belongs to the accepted product itself is project data and is separate from Council's temporary control database.

## 11. Explicit non-goals

Part 5 does not require:

- distributed SQL transactions;
- cross-region consensus;
- Kafka;
- Redis;
- CRDTs;
- a generalized saga/orchestration engine;
- generic automatic merge/conflict-resolution logic;
- permanent retention of the Council control database.

These may be reconsidered only if measured requirements justify them.

## 12. Completion boundary

The baseline establishes the following design boundaries; the October 13 ordering, accounting, and recovery refinements must be integrated and tested before any implementation-complete claim:

- what must commit atomically;
- how retryable commands deduplicate;
- how stale concurrent writes are rejected;
- how immutable/versioned records avoid overwrite;
- how external side effects are represented;
- how unknown outcomes are reconciled;
- how task ownership prevents double execution;
- how committed events survive publication failure;
- how lagging projections expose their consistency position;
- when the temporary Council database is destroyed.

## 13. Commit ordering and framework recovery

Use one deployment-local transactional event-clock row for the initial single-PostgreSQL deployment. Every event-producing canonical transaction obtains that row lock before aggregate/budget locks, allocates its event positions by updating the row, and holds the lock through commit/rollback. Allocate all events of the transaction together. Do not use an ordinary sequence, SERIAL, or IDENTITY allocation as a committed-delivery watermark. This deliberately simple serialization trades throughput for clear ordering; measure before replacing it with a different recorded ordering design.

The clock, canonical mutation, events, idempotent result, and outbox entries commit together. No external call runs while holding that transaction. Rollback publishes nothing. Snapshot data and its committed event watermark come from one consistent database snapshot. Replay filters authorization and orders committed canonical events; visibility filtering must not turn hidden events into a spurious missing-data error.

Outbox workers claim unpublished rows, not just IDs greater than the last observed ID. A retry cannot skip an older unpublished row. Consumers deduplicate by event identity and advance projection offsets atomically with effects only across processed committed events. Out-of-order notification delivery triggers ordered canonical replay/buffering rather than falsely advancing a watermark. The snapshot/SSE race and the lower-number-transaction-commits-later scenario require integration tests.

LangGraph checkpoints are continuation projections, not a second authority over effects, permission, or completion. Bind continuation to logical member, execution epoch, contract/permission versions, and source event position. On restore, reconcile against canonical operations and obligations before executing a step. Replayed framework nodes must reuse logical operation identities and may not redispatch uncertain consequential effects. Runtime side-effect and accounting records prevail over an old checkpoint.

## 14. Uncertain effects and reservation transactions

Unknown outcomes have operation-specific dependency gates. Read-only retrieval/inference may allow safe independent progress after fencing and isolation checks, while stale results remain quarantined and uncertain usage remains reserved. Consequential writes must be reconciled before replay and block work dependent on their outcome. Authority, checkpoint snapshot read grants/revocations, optional external publication, and isolation mutations fail closed for the affected boundary until safe state is verified. Unknown does not mean successful, failed, cancelled, free, or that the entire run must stay blocked forever.

Reserve spending transactionally before dispatch across run, branch, parent/worker, and protected review/finalization allowances. Include member, worker, retry, Orchestrator, verifier, and finalization use. Reserve a conservative bound using explicit pricing/units and input/output limits; unknown pricing cannot pass a cost ceiling as zero. Pre-dispatch expiry may release a reservation; dispatched/unknown requests retain it until reconciliation or conservative settlement. A retry needs independently authorized allowance unless the provider contract proves reuse of the same charged operation. Protected review funds are not ordinary development balance. Fixed-precision accounting and consistent lock ordering are required; concrete provider adapters and tests remain pending.

Local snapshot export/grant/revoke remains an operation outside PostgreSQL: desired/granted/revoked states and verified physical access/closure require separate commits. A SQL transaction must not claim that a Git archive, controlled mount, access grant or route actually changed. Optional hosted/public publication remains a separately authorized adapter. All listed runtime acceptance tests remain NOT RUN.

## 15. Step 7 budget and resource reservation integration (October 14 specification)

The accepted Step 7 design establishes these additional **transaction contracts**; their implementation and concurrent failure-injection tests remain NOT STARTED / NOT RUN.

1. **Immutable user-approved policy:** retain the exact run/contract revision, policy version, currency, protected pool allocations (initial *proposed* 70% development / 25% review / 5% orchestration-finalization), per-member/phase token-cost ceilings, model-price assumptions, and user-authorization event. Unapproved suggestions, including speculative token estimates, are never authority to spend.
2. **Lock and check order:** for each event-producing authorization/settlement transaction, lock the deployment **transactional event-clock row first** (Part 5 Section 13), followed by budget scopes in deterministic **run -> pool -> member/phase** order and relevant resource-admission rows. Check settled + unsettled reserved token and fixed-precision currency amounts against **all** affected hard ceilings. Update versioned balances only under the locks. Consistent lock order prevents conflicting concurrent requests from both spending the same allowance.
3. **Commit before external call:** in one transaction write a durable logical operation, idempotency key/request hash, conservative usage reservation, resource admission claim, budget-account updates, canonical event(s), outbox record and idempotent response. Never call a provider while the transaction remains open. An uncertain handoff between `RESERVED` and `DISPATCHED` is treated as possibly dispatched unless proven otherwise.
4. **Settlement/recovery:** provider-reported input/output/cached usage and actual cost settle under the same locking/order rules. Known non-dispatch may release allowance. Dispatched/unknown outcomes keep liability until verified reconciliation or conservative settlement. Repeated request/worker/session rollover cannot erase usage, and retry needs another authorized reservation unless provider-specific idempotency proves the original charged operation is reused. A stale execution epoch cannot complete current work or issue new authority.
5. **Resource claims:** sandbox/memory/VRAM/remote concurrency admissions are independently recorded; a released slot cannot be rescheduled until trusted backend evidence confirms release. Host-pressure denial is a recorded operational reason, not an intellectual rejection. The fixed seat queue remains 1 -> 2 -> 3 -> 4 -> 5 when admission capacity becomes available.
6. **Lifecycle transitions:** `PauseRun` records `QUIESCING_FOR_PAUSE` activity before `PAUSED` after durable quiescence; `ResumeRun` validates the full permission/budget/resource/isolation/operation state. `StopRun` enters `STOPPING` and reaches `CANCELLED` only after adequate cleanup, otherwise `FAILED` / incomplete; acceptance/final archival is a separate path. Each transition plus its events/outbox is atomic inside Council PG; external Docker/provider results are separately reconciled.
7. **Phase exhaustion:** `BUDGET_EXHAUSTED_INCOMPLETE` is a member/phase operational result, not `CHECKPOINT_READY`, `/done`, or project acceptance. It durably preserves the phase/agent, blocked obligations, and five-seat barrier until user-approved top-up or cancellation.

**No additional Council billing ledger or prepaid wallet is introduced.** BYOK users are billed by external providers; Council-reserved allowances restrict Council-authorized dispatch and cannot guarantee the user's final external-provider bill. Per-provider pricing/metering and Docker sandbox enforcement belong to Step 9 and Step 10 implementations respectively.


## 16. October 14 Part 5 design closure — exact transaction and recovery boundaries

**Part 5 is DESIGNED as a transaction/idempotency/reconciliation contract.** The earlier sections are retained and this section resolves the October corrections. No SQL, queue, provider client, local snapshot gateway or Docker recovery logic or integration test has been executed by this specification update.

### 16.1 Database-local atomicity versus external truth

Council's per-deployment **temporary PostgreSQL** is the only active canonical state authority. Canonical commands use a single local transaction for the required aggregate mutation, immutable domain decision, related provenance, event(s), outbox record(s), and idempotency receipt. Do not put network/API/filesystem/Docker calls inside a transaction or claim two-phase/distributed atomicity with those systems.

External effects have two independently auditable facts:

1. **intent/dispatched**: a user-authorized operation is durably queued with exact target, scope/hash and retry/reconciliation policy;
2. **observed outcome**: external provider/customer-local snapshot gateway/optional Git/Docker evidence proves success, proves known non-effect/failure, or remains UNKNOWN_PENDING_RECONCILIATION.

A command response `accepted=true` means its canonical intent was committed, **not** that the outside action succeeded. Emit externally successful events (`CheckpointSnapshotsAvailable`, `CheckpointSnapshotAccessRevoked`, `SandboxResourceReleaseConfirmed`, `CleanRebuildPassed`) only on actual trusted evidence. A late response from an old bridge epoch may be used for reconciliation of the original attempt but never grant a new action, current identity, or unversioned state mutation.

### 16.2 Scoped idempotency and commit ordering

- Store a `command_receipt` with actor/scope, command type/schema version, user/target revision, `idempotency_key`, **canonical request hash**, original result/error and operation/event identities. Unique(scope, actor, command_type, key) is enforced by PostgreSQL. Repeat with same hash returns saved authorized result even when target is now at a later version; same key with altered request returns IDEMPOTENCY_CONFLICT. Authenticate/authorize before revealing the saved response; internal retrier identities are appropriately scoped. Do not rerun external effects.
- For a **new** command, hold the deployment event-clock row lock first, then lock mutable target aggregates/required checkpoint frontiers in canonical ID order, then budget rows in run -> pool -> member/phase order (where involved), then resource claims in stable ID order. A transaction touching both target and budgets must use the same global ordering; use a standardized helper instead of ad hoc competing lock sequences. Validate expected versions *under* those locks. Conflict => STALE_TARGET, never an overwrite.
- Allocate contiguous **committed** event positions by updating the locked event-clock row inside the same transaction. If transaction rolls back, its event clock increment rolls back. Do not substitute a PostgreSQL sequence/IDENTITY as a committed cursor. Event type/schema/actor, aggregate identity/version, command causation, visibility scope and correlation are immutable. Commit event+outbox+command receipt with the canonical mutation.
- All retryable durable effects use one logical operation key per intended effect, with append-only attempt IDs, idempotency support where providers offer it, current lease/epoch fencing, and a recorded `last_observed` outcome. A lease heartbeat/completion or delayed action needs the current `lease_token` and attempt, not merely a task ID. `FOR UPDATE SKIP LOCKED` is for trusted runtime jobs only, never the agent's self-directed internal work.

### 16.3 Canonical atomic groups and checkpoint staging

| Operation | Single PostgreSQL transaction | External/staged condition |
| --- | --- | --- |
| Project Contract approval | exact revision/hash, interaction response + decision, immediate run PROVISIONING intent, budget/permission policy identity, events/outbox + receipt | member repos, sandboxes and credentials provision afterward by durable operations; do not declare ACTIVE until verified prerequisites |
| Project-wide clarification/change | confirmed source-linked raw/processed answer, revision/permission scope and intended target deliveries, events/outbox | only approved processed/revision packages delivered to authorized branches; partial delivery remains visible and retryable |
| Member checkpoint readiness | member-authored READY, exact current phase/generation, frozen candidate SHA/environment/evidence, unique per seat, event/receipt | all five arrivals enable triggering; no automatic substantive readiness or bypass from BUDGET_EXHAUSTED |
| Checkpoint opening/local snapshot sharing | phase/generation freeze + five arrivals, user-approved selected local read-only tree snapshot manifests/hashes/recipients, intended export/grant operations, OPENING event | independently observe each immutable snapshot hash and scoped recipient read access; only after all current-generation exports/grants verified enter SEALED_REVIEW; partial/unknown stays guarded |
| Sealed-review submission | immutable reviewer/candidate-set/evidence hash, one per seat/generation, event scoped to submitting reviewer/trusted runtime | **not** published in Git repos, shared retrieval/SSE or peers prior to authorized reveal |
| Sealed-review reveal | under same checkpoint generation/frontier lock, verify all five distinct submissions; one reveal/recipient delivery set + event/outbox | all-five reveal is one canonical visibility change; zero partial peeks or skipped seats |
| Gateway message/action and DONE | complete hashed logical message + monotonic checkpoint sequence + action obligations/versions; DONE validates processed and outbound frontiers and work state under same checkpoint lock | socket delivery does not prove processed; new relevant required action atomically invalidates affected DONE certificate |
| Checkpoint closing | CLOSING guard + accepted transcript/closeout/return intent + gateway session and temporary snapshot grant revoke operation requests | wait for trusted proof that each peer grant/route is revoked, active verifier resolved and valid DONE or explicit forced-incomplete policy before CLOSED and authorized return packet delivery |
| Budget/phase model dispatch | versioned user-approved run/pool/member-phase token+cost caps, worst-case reserved usage, provider/local resources, operation/attempt, event/outbox/receipt | call only after COMMIT; unknown dispatched cost stays reserved, no automatic budget increase or claim of checkpoint readiness |
| Candidate acceptance | exact user-approved snapshot/interaction, immutable acceptance decision, export/retention manifest INTENT, archive/cleanup operations, event | fresh Git checkout/hashed evidence reference closure and product restore succeed **before** Council control DB teardown; acceptance itself is not completed archival |
| Claim revision | append new claim version, source/evidence relationships and attribution, challenge/revision justification, events/outbox | no automatic reinterpretation of support, universal truth score, or external effects |

### 16.4 Unknown outcome classes and safe progress

- **Read-only retrieval and inference:** if the provider or bridge loses contact, fence old epoch; quarantine stale result until reconciled. Safe *independent* work may continue with a fresh authorized request, but uncertain tokens/cost remain reserved and duplicates require their own allowance.
- **Consequential external writes:** query provider-side state/request ID/idempotency status before retry; dependent operations wait. A write being unobserved is not proof of no effect. Do not duplicate a publication, Git commit, payment, or host mutation blindly.
- **Authority / visibility / isolation mutations:** fail closed for the affected boundary until observed safe state is verified; a peer still able to access another's changing local workspace or an unapproved exported snapshot blocks new private work. Revocation cannot erase already-delivered knowledge; public exposure is possible only by separately approved external operation.
- **Container/resource cleanup:** a stop request or Docker exit code alone is not proof of all resource/route release. Only trusted backend checker evidence can free the reservation and permit reusing a scarce slot.
- **Billing:** Council's BYOK budget is an internal authorization constraint, not the user's exact invoice. A request handoff that cannot prove non-dispatch retains a conservative reservation; no timeout or process crash silently refunds it. Review reserve is protected from development charges. Reallocation/top-up requires explicit versioned user approval.
- **Stop and acceptance:** STOPPING -> CANCELLED only when required cleanup safety is verified, otherwise FAILED/incomplete record with outstanding consequences. AcceptCandidate is separate: export/validate retained project and Git lessons, then clean Council control DB. An explicitly approved retention/evidence limitation may downgrade an archive claim; it cannot silently fabricate proof.

### 16.5 Outbox, projections and SSE reconnect without lost events

- Outbox is a transactional representation of already **committed** canonical events. Publishers claim unpublished rows with leases/attempts and retry after process failure. A queued row whose ID is lower than the highest published ID still needs delivery; never rely exclusively on `id > last_published_id` to discover work.
- Consumer deduplication is by immutable `event_id`. A projection advances its processed committed position **only after** applying all relevant earlier events or explicitly accounting for authorization-filtered/skipped events in its own scope. Arrival order from workers/SSE is not committed order.
- A canonical UI snapshot and its event watermark must be read under **one consistent database snapshot**; clients then replay authorized events after that position. Filtering hidden branch-local events must not leak secret payloads or be rendered as a fake missing-event error. Authorization is checked at replay and at snapshot. An out-of-order or duplicate SSE notification triggers gap recovery from canonical committed history, not invented state.
- Evidence graph/retrieval indexes and UI counters may lag; expose a projection's last applied event position. Framework session checkpoints never override canonical operation, budget, permission, epoch or event history.

### 16.6 Failure-injection and deterministic acceptance cases (all NOT RUN)

1. Concurrent same-key/same-payload commands return **one** receipt/result and one external operation; same key/different payload fails with IDEMPOTENCY_CONFLICT; a successful approval retry after state advancement returns the original result.
2. Two transactions producing canonical events cannot commit in a different order than recorded event positions. Rollback emits no event/outbox data; outbox retry picks older unpublished records.
3. Two members/workers/Orchestrator calls cannot spend shared phase/run funds twice; partial/missing provider responses retain proper unknown liabilities, and no protected review funds leak to development.
4. Task lease expiry/regrant invalidates stale worker completion/heartbeat; sandbox epoch rollover invalidates forgotten bridge requests without assuming sent provider calls were cancelled.
5. A partial/unknown **local snapshot export, read grant or revocation** cannot move the checkpoint into SEALED_REVIEW/CLOSED; verify each pinned hash, approved scope and authorized recipient's actual access/no-access. Any optional external Git publication is separately consented and verified.
6. Five distinct sealed assessments must be committed before reveal. A simultaneous fifth submission and reveal never sends an unauthorized partial peer assessment.
7. DONE racing against a new required action/message or closing checkpoint preserves obligation and current processed frontier; /done stale retries do not fake completion.
8. Crash during STOPPING, archive export, fresh Git reference validation, or teardown can restart idempotently; missing retained evidence blocks deletion instead of erasing its only source.
9. A UI snapshot followed by ordered replay cannot lose, duplicate or leak canonical events even across reconnects, hidden-branch authorization filters or delayed outbox publications.

**Historical Part 5 baseline** was DESIGNED for the old public-GitHub workflow. ADR-17 **reopens local snapshot/grant/revoke and customer-private archive transactional integration**. Idempotency, committed-event ordering, conservative budget reservations and UNKNOWN reconciliation remain specified. No provider, local Git gateway, SQL or sandbox behavior has been implemented or tested.

## October 15 Step 5 architecture integration — safeguarded operations with trusted command-only file results (approved direction; design only)

See [deployable design](STEPS_3_TO_5_DEPLOYABLE_ARCHITECTURE_2026_10_15.md). Keep one project-local PostgreSQL as canonical state, transactional committed event-clock/outbox/receipt, and no external model/IRC/Docker/Git action inside an SQL transaction. The customer-approved **unified trust** application authenticates then checks deterministic actor/scope, policy and generation, invokes customer-hosted **OpenAI Moderation API** semantic classification for relevant textual ingress/egress, and records a bounded policy receipt before dispatch. The model classification must not grant authority otherwise denied by the deterministic rules. Guard UNAVAILABLE/BLOCK/REVIEW is an explicit guarded state, never a silent allow or unsupported claim that binary data was scanned.

Agent requests for peer files remain typed **read-only server-resolved manifest object operations**, separate from text-only chat. Any bounded content stream has original command receipt, exact generation/recipient, manifest/hash, source object/range, transfer epoch, status and observed result. File responses cannot include/automatically enqueue a chat message. The server alone resolves and sends content; members have no outbound SendFile or unrestricted file-path/directory access to other members.

On checkpoint close: **atomically fence new chat and artifact-read admission under the checkpoint state**, then independently stop in-flight transfers and revoke trusted snapshot grants/routes; reconcile partial/UNKNOWN effects with actual observed state before CLOSED or resuming private work. A gateway timeout cannot prove removal. Preserve legitimate already-received information without claiming erasure. Existing independent sealed-review atomic reveal, version-bound DONE races, budget reservation/UNKNOWN liability, stale-epoch fencing, source ownership and verified archive-before-teardown remain authoritative.

**STATUS:** approved direction; exact attempt/reconciliation DTOs, atomic guard receipt boundaries, content cache invalidation, transfer cancellation and physical access checks are **IN DESIGN**. No application code, migration, integration test, benchmark, evaluation or production claim.

## October 16 — Step 8.4 integration/synthesis effects (owner-approved policy; precise transactions IN DESIGN)

One verified all-five final investigation set -> normal sealed final-comparison checkpoint -> evidence/version-bound synthesis blueprint -> **observed closure and recipient read-revocation** -> separate trusted integration source grants -> one non-voting integrator produces one content-hashed customer-owned deliverable -> **five sealed post-integration member reviews** -> version-bound premortem/report -> explicit user acceptance -> verified customer archive/cleanup. Every phase is separate durable state/operation intent and observed effect. The integration agent is **not** a sixth member or authority to extend its source permissions, provider egress or spending.

Record each blueprint/artifact generation, exact source hashes, permissible integration read grants, associated provider/host operations, source-to-result provenance, post-integration sealed reviewer submissions, invalidation of obsolete tests/reviews when material revisions occur, and permitted standalone non-code final artifacts. The trusted worker may execute side effects **only after committed intent**, with idempotency, event clock, outbox, execution epochs, per-phase integration budget reservations and UNKNOWN reconciliation. Never copy snapshot grants from the earlier comparison checkpoint to integration by implication. No user acceptance or completed final archive can be inferred from generated source/document text or member votes.

See [owner-approved Step 8.4](STEP_8_4_COLLECTIVE_SYNTHESIS_AND_FINAL_INTEGRATION.md). Runtime migrations/transactions/tests NOT STARTED/NOT RUN.

## October 16 approved Step 8.4 bounded integrator and re-review transaction guards (ADR-26–29)

**Integrator discretion and versioning:** record source/evidence/contract/Blueprint-bound ordinary technical decisions and deviations as attributed intents/results. A substantive permission/scope/budget expansion is a separate **user-approved** versioned command, not a model-authored rationale. Identity scopes distinguish one non-voting integrator from the five independent reviewers; stale epochs cannot commit new reviews/blueprints.

**Five protected spend scopes:** allocate the Integrator's user-approved execution budget and the later five-member review/premortem reserve separately, alongside independent member work, checkpoint comparison and orchestration/report/archival overhead. The historical 70/25/5 is **not** the current default. Before dispatch, atomically reserve using the existing run/aggregate/budget lock order and exact chargeability scope; no protected pool borrowing, double counting, or assuming UNKNOWN provider calls were free. If integration capacity exists but required review capacity does not, do not admit work under an unreviewable plan without explicit policy revision.

**Integrated-result version and five-member reviews:** commit one immutable artifact/hash/version and separately record its content dependency/equivalence/impact classifications. Never atomically pretend to execute Git/provider/Docker effects inside SQL. For localized **substantive** changes, open a new scoped/delta sealed review generation requiring five genuine original-member submissions against the same exact target version; foundational/high-risk/unknown impact requires full review. Demonstrably equivalent non-substantive changes may retain only evidence-supported unchanged applicability. A late old-version review cannot count toward current five-member reveal; old passing tests are historical and affected checks become STALE until actually re-established.

**Five-person premortem:** a separate `SEALED_PREMORTEM` generation is locked to a single frozen integrated-output and provisional-report version pair. Only five real valid submissions permit atomic reveal; mixed-version/racing submissions cannot be accepted into the new version's cohort. Updated integrated output/report invalidates affected premortem applicability, requiring scope-appropriate five-member reassessment; indeterminate impact defaults broader. Keep already recorded hypothetical scenarios as historical interpretations, not observed future events.

Reconcile export/grant/revoke, client reconnect, provider spend, loss/crash and review-generation UNKNOWN outcomes through the existing outbox/idempotency/operation ledger. These are **approved policies** with exact transaction DTO and retry semantics still IN DESIGN; implementation/test evidence NOT STARTED/NOT RUN. [Step 8.4 §9](STEP_8_4_COLLECTIVE_SYNTHESIS_AND_FINAL_INTEGRATION.md).

## 17. ADR-17 local-source consent and checkpoint transactions (DESIGN REOPENED)

The new [local-first repository/knowledge design](LOCAL_REPOSITORY_AND_KNOWLEDGE_RETENTION.md) is authoritative over former PUBLIC GitHub semantics. `PublishCheckpointSnapshots` commits desired export/grant operation intent and outbox, then verifies local tree snapshot hashes, selected content and scoped read grants outside SQL. Only confirmed observations lead to `CheckpointSnapshotsAvailable`. `RevokeCheckpointSnapshotAccess` separately requests cleanup, and `CheckpointSnapshotAccessRevoked` requires verified scope/route closure. The same committed-event/idempotency/UNKNOWN controls remain. A local read grant does not imply customer permission to send source to remote AI providers or share learning outside the tenant.

Customer-owned long-term archive export and evidence-closure validation must honor the user's retention/deletion rules and remain independent of **optional, specifically approved** general-knowledge disclosure. Any cross-customer pattern export requires an independently idempotent authorization, content review/approved audience, minimal permitted evidence, and proof of *what* actually left the trust boundary. Rejected/unknown consent is never treated as permission. No automatic extraction or uploaded lesson from customer work.

Step 5 design was reopened only for these interfaces; execution/race/side-effect tests **NOT RUN**.


**October 15 ADR-22 correction (authoritative):** The owner's intended safeguard is the **hosted OpenAI Moderation API** (`omni-moderation-latest`) called over HTTPS from the trusted backend, **not** any local/open-weight GPT-OSS model. It is free for API users but requires API credentials, internet and allowance for rate limits. Submitted content leaves the customer environment: require separately approved provider/data-category egress BEFORE the call, including for company source or customer records. The endpoint classifies supported **text/images** and returns moderation categories/flags; it is **not** an arbitrary custom-policy, prompt-injection, exfiltration, binary/malware or deterministic authorization engine. Local read grants, sandbox isolation, content hashes, and customer permissions remain mandatory. No silent fail-open on moderation refusal/outage, no silent upload without customer authorization. See [ADR-22 correction](OPENAI_MODERATION_API_CORRECTION.md). Specification direction only; no implementation or tests.
