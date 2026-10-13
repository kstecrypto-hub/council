# Part 5 - transactions, idempotency, and conflict handling

**October 13, 2026 amendment:** [decision/status index](ARCHITECTURE_DECISIONS.md). Requirements below are specifications; application implementation is NOT STARTED and runtime tests are NOT RUN.

**Status:** DESIGN AMENDED; transaction integration and runtime verification remain pending.
**Scope:** consistency and retry semantics for active Council deployments.  
**Implementation status:** specification only.

## 1. Core rule

PostgreSQL is the canonical source of truth for an active Council project.

> Local canonical changes are atomic. Commands are idempotent. Mutable writes prove which version they acted on. External effects are durable operations. Unknown external outcomes are reconciled rather than guessed.

This part deliberately does not introduce distributed transactions, CRDTs, Kafka, a generalized saga engine, or automatic semantic conflict merging.

## 2. Canonical transaction boundary

A command whose authoritative effects are entirely inside Council PostgreSQL executes in one transaction:

```text
BEGIN
  authenticate / authorize
  validate schema
  check expected target version
  check idempotency
  mutate canonical state
  write durable event(s)
  write outbox row(s)
  persist command result
COMMIT
```

Any failure before commit rolls back the complete canonical change.

Important atomic groups include:

- user response + interaction resolution + corresponding domain decision;
- Project Contract approval + launch revision activation + run creation/provisioning + events;
- project-wide contract revision activation + intended branch delivery records;
- checkpoint opening + frozen repository SHAs + access/session records + events;
- checkpoint closing + closeouts + access/session closure + return-packet records + events;
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

- GitHub repository public/private visibility changes and scoped content operations;
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
Council -> GitHub: make an approved member repository public
GitHub may complete it
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

Unknown outcomes have operation-specific dependency gates. Read-only retrieval/inference may allow safe independent progress after fencing and isolation checks, while stale results remain quarantined and uncertain usage remains reserved. Consequential writes must be reconciled before replay and block work dependent on their outcome. Authority, public/private visibility, and isolation mutations fail closed for the affected boundary until safe state is verified. Unknown does not mean successful, failed, cancelled, free, or that the entire run must stay blocked forever.

Reserve spending transactionally before dispatch across run, branch, parent/worker, and protected review/finalization allowances. Include member, worker, retry, Orchestrator, verifier, and finalization use. Reserve a conservative bound using explicit pricing/units and input/output limits; unknown pricing cannot pass a cost ceiling as zero. Pre-dispatch expiry may release a reservation; dispatched/unknown requests retain it until reconciliation or conservative settlement. A retry needs independently authorized allowance unless the provider contract proves reuse of the same charged operation. Protected review funds are not ordinary development balance. Fixed-precision accounting and consistent lock ordering are required; concrete provider adapters and tests remain pending.

Repository visibility remains an external operation: requested/public/private state and verified publication/closure are separate commits. A SQL transaction must never pretend to atomically toggle GitHub visibility. All listed runtime acceptance tests remain NOT RUN.
