# Part 5 - transactions, idempotency, and conflict handling

**Status:** DESIGNED.  
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

- GitHub access/grants/revocation;
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
Council -> GitHub: grant peer access
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

Part 5 is DESIGNED because implementation no longer needs a product-level decision to determine:

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
