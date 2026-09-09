# Part 1 of 15 — Runtime Architecture & Execution Boundaries

**Status:** approved component design; not yet implemented.  
**Branch:** `design/code-level-implementation`.  
**Approved scope:** runtime/process structure, event-driven waiting, concurrency model, local compute boundaries, and failure behavior.  
**Authority:** this document refines Part 1 of [CODE_IMPLEMENTATION_PLAN.md](../CODE_IMPLEMENTATION_PLAN.md) after discussion. It does not replace the complete product requirements in [APP_DESIGN.md](../APP_DESIGN.md). Later explicit owner instructions take precedence.

## 1. Decision summary

Council will use a modular-monolith backend with separate runtime processes and durable PostgreSQL state.

The implementation must distinguish:

- a **logical agent** — persistent council member or worker identity;
- a **model session** — one bounded LLM conversation for that logical agent;
- a **task** — an investigation objective or deliverable;
- a **trusted executor process** — software that temporarily advances eligible agent work;
- an **untrusted sandbox container** — isolated local execution for generated code, calculations, or other heavier local tools.

The application will run logically ready work concurrently whenever the relevant resource pool has capacity. It will not assign intellectual priority to one council member's hypothesis over another.

Waiting work is event-driven. A task waiting for another member, worker, source, approval, or other dependency becomes durable `WAITING` state rather than holding an LLM request or HTTP request open.

PostgreSQL is the durable source of truth. PostgreSQL notifications may wake executors, but notifications are not the authoritative state themselves.

The browser receives live application updates over Server-Sent Events (SSE). Internal agent dependencies do not use browser-style long polling or long-lived HTTP requests between agents.

DeepSeek/model API concurrency is treated as a separate resource pool from local sandbox compute. The architecture must support high parallel model use without forcing an unnecessarily small global concurrency limit.

Local storage on HDD is a hard deployment constraint for the initial machine. The implementation must not assume that application data, PostgreSQL, Docker state, or artifacts can be placed on SSD.

## 2. Initial process topology

One backend codebase supplies several process entry points:

| Process/component | Responsibility | Must not become |
|---|---|---|
| FastAPI API process | Authentication, commands, queries, run control, SSE delivery | Owner of an investigation's lifetime |
| Trusted executor pool | Model calls, approved tool calls, agent-session advancement | Permanent home of an agent's identity or untrusted code execution environment |
| Maintenance/recovery process | Expired lease detection, reconciliation, projection/index maintenance | Research planner or intellectual supervisor |
| PostgreSQL | Durable tasks, sessions, evidence metadata, claims, operations, events, queue state | Disposable cache |
| Artifact storage | Original documents, retained outputs, large artifacts | Only source of task or claim state |
| Docker sandbox pool | Isolated generated-code/calculation execution | Holder of DB/provider credentials or council memory |

The API, executor, and maintenance processes can run on the same physical machine initially. This is process separation, not high availability.

If the machine is offline, work stops. When services return, durable state must allow controlled continuation.

## 3. Logical agents are independent of operating-system processes

A council member persists across executor restarts, context rollovers, and model changes.

An executor process may run a turn for Council Member A, later run a worker for Member C, and later continue Member A again. It must load the correct session, permissions, task state, and context references each time.

No global mutable `current_agent` state may be shared across concurrent work.

An agent waiting for a dependency consumes no model-call slot and should not occupy an execution slot merely to remain alive.

A new model session for the same logical agent is a continuation, not a new independent reviewer.

## 4. Start-run behavior

Starting an investigation must be a short durable command, not an HTTP request that stays open until the council finishes.

Expected flow:

```text
User starts run
    -> API authenticates user
    -> validate run configuration and permissions
    -> persist run + initial branch/task records
    -> persist initial runnable work
    -> COMMIT
    -> return accepted run identifier
```

The accepted response means the run was durably recorded. It does not claim every model call has already started successfully.

Closing the browser must not stop a run.

Restarting the API must not erase logical agents, sessions, tasks, or executor progress that was already committed.

## 5. Event-driven dependency waiting

### 5.1 Durable dependency state

If task A requires a publication or result from task B, task A transitions to durable waiting state.

Example:

```text
Task A-42
state = WAITING
requires = Publication B-17
```

The model turn ends. No LLM request remains open while waiting.

When B-17 is committed, application logic marks dependent work eligible.

### 5.2 PostgreSQL LISTEN/NOTIFY is a wake-up mechanism

The implementation may use PostgreSQL `LISTEN/NOTIFY` to wake executor processes after committed state changes.

Pattern:

```text
B publishes result
      |
      v
persist publication + satisfy dependency
      |
    COMMIT
      |
      v
NOTIFY work_available
      |
      v
executor wakes and queries durable ready work
```

The notification payload should be small. The executor always re-queries authoritative state.

If an executor misses a notification because it was offline, no work is lost; normal ready-work scanning on startup/recovery finds it.

The system therefore does not depend on notification delivery for correctness.

### 5.3 Browser live updates use SSE

SSE is the initial browser live-update mechanism.

```text
Committed application events
        -> API SSE stream
        -> browser
```

The stream is for user visibility, not internal council synchronization.

Reconnect behavior and event schema belong primarily to Part 12.

## 6. Concurrency model

### 6.1 Parallel by default

The runtime rule is:

> Start logically eligible work whenever the resource pool required by that work has capacity and policy permits it.

Tasks should not be serialized simply because they belong to different council members.

The scheduler does not rank hypotheses by perceived scientific value.

### 6.2 Separate resource pools

At minimum, capacity must be tracked separately for:

1. remote model/provider calls;
2. local sandbox execution;
3. trusted application/control-plane resources;
4. configured financial/budget limits.

A model call waiting on DeepSeek must not reserve a sandbox slot.

A sandbox calculation must not consume an LLM concurrency permit after the model request has ended.

### 6.3 Model API capacity

The initial system is not expected to approach DeepSeek's published account-level concurrency limits. We therefore do not need an elaborate model-call priority system for the first implementation.

The provider gateway still needs:

- in-flight request accounting by the correct quota group;
- retry/backoff handling for provider throttling;
- configurable application-side concurrency ceilings;
- cost/budget accounting;
- explicit provider/model attribution.

Different API keys are not assumed to create independent provider capacity unless the provider's actual quota model confirms that they do.

The implementation must permit future higher-capacity providers/models without changing council semantics.

## 7. Fairness under contention

When capacity exists, all eligible work may run.

When a shared pool is full, selection is operational rather than intellectual.

The initial policy should provide fair access between active council branches while allowing unused capacity to be borrowed by branches that have additional eligible work.

Example principle:

- do not reserve idle slots permanently for an inactive branch;
- do not allow one branch with a very large queue to starve all others;
- do not suppress a job because the scheduler disagrees with its hypothesis;
- consider resource fit and safe resumability when local contention requires delaying or interrupting work.

The exact fairness algorithm belongs to Part 7.

## 8. Trusted executors vs Docker sandboxes

### 8.1 Trusted executor

The trusted executor may:

- read permitted application state;
- call the selected LLM provider;
- invoke approved application tools;
- submit typed commands through application services;
- persist model/tool operation records;
- request creation of a sandbox job.

It may hold controlled references to provider/database credentials required for those trusted operations.

### 8.2 Untrusted sandbox

Generated code, calculations, scripts, or other locally executable workloads run in a separate disposable/restartable Docker sandbox.

A sandbox must not receive:

- PostgreSQL credentials;
- DeepSeek/provider API keys;
- unrestricted access to other agents' files;
- Docker daemon/socket access;
- unrestricted host filesystem access;
- unrestricted network access by default.

Sandbox inputs should be explicit mounted/copied artifacts. Outputs return as bounded result/artifact records.

Network access is opt-in for tools that genuinely require it.

The sandbox manager records resource requests, lifecycle, outputs, failures, and whether a job can resume or must restart.

## 9. Local-machine resource policy

### 9.1 Initial hardware constraint

The initial development machine has limited local resources and uses HDD storage for application data. SSD storage is not available as a practical application-data target.

Therefore:

- the implementation must run correctly with PostgreSQL and active application storage on HDD;
- Docker/sandbox design must not assume SSD latency;
- performance tuning must be measured on the real machine rather than designed around an unavailable SSD;
- correctness and recoverability take precedence over high local IOPS.

Database/index/storage tuning is deferred to Part 3 and deployment hardening rather than silently fixed here.

### 9.2 High utilization is allowed, but protect the control plane

The local PC is intended to be used aggressively for development and sandbox work.

However, sandboxes must not be allowed to starve PostgreSQL, the API, the operating system, or executor control processes to the point that state cannot be recorded or recovered.

The sandbox pool therefore uses configurable CPU and memory limits plus a small protected margin for the control plane.

No arbitrary low sandbox count is an architectural requirement. If the machine can safely run more jobs, the runtime may admit more.

### 9.3 CPU pressure

High CPU utilization alone is not a reason to kill work.

Use OS/Docker CPU sharing/limits. Parallel jobs may continue when the system remains responsive and control-plane services have adequate capacity.

### 9.4 Memory pressure

Memory requires stronger admission control.

Do not wait for system-wide memory exhaustion before reacting.

Before starting a new sandbox, check the configured sandbox-pool memory allowance and the job's requested/estimated resources.

If memory pressure becomes critical:

1. stop admitting additional memory-heavy work;
2. prefer checkpointing/terminating explicitly resumable sandbox jobs;
3. preserve PostgreSQL/API/control-plane operation;
4. resume/restart deferred work after capacity returns.

Pausing a container is not treated as equivalent to releasing its memory.

A sandbox that cannot resume from a checkpoint must have an explicit safe-restart or reconciliation policy.

## 10. HDD storage implications

HDD use is mandatory in the initial environment, so it is a supported deployment mode rather than an exception.

Operational consequences to account for later include:

- slower random I/O;
- slower container-layer and database-heavy workloads;
- greater benefit from batching and avoiding unnecessary writes;
- need to keep large artifacts out of frequently scanned relational rows;
- need to benchmark indexes, checkpoints, artifact reads, and sandbox filesystem behavior on HDD.

Part 1 does not choose PostgreSQL WAL/checkpoint settings, Docker storage-driver tuning, or artifact placement between D:/E:. Those decisions belong to later implementation/deployment reviews.

The architecture must simply avoid making SSD availability a requirement.

## 11. Executor work unit

Trusted executors advance work in bounded recoverable units:

```text
claim eligible work
    -> verify permissions, dependency state, budget, resource permits
    -> load logical agent/session references
    -> construct permitted context
    -> perform next model/tool operation
    -> persist operation outcome
    -> transition task to READY, WAITING, PAUSED, FINISHED, FAILED, or UNKNOWN-OUTCOME as appropriate
    -> release execution capacity
```

A bounded unit may contain multiple local application steps, but it must have an identifiable recovery boundary.

Do not hold a database transaction open while waiting for an LLM/provider response or long-running sandbox process.

## 12. Failure behavior

| Failure | Required behavior |
|---|---|
| Browser disconnects | Run continues; UI later catches up from durable events/state. |
| API restarts | Executors and durable investigation records remain valid. |
| Executor dies | Leased/in-progress work enters controlled recovery; no blind duplicate assumptions. |
| Missed PostgreSQL notification | Startup/periodic ready-work scan recovers because queue state is durable. |
| Provider call outcome uncertain | Preserve `UNKNOWN_OUTCOME`/equivalent state and reconcile rather than pretending failure or success. |
| Sandbox dies | Apply job-specific resume/restart/reconcile policy. |
| PostgreSQL unavailable | Stop creating new consequential work that cannot be durably recorded; do not claim uncommitted progress as durable. |
| Artifact missing/unreadable | Mark evidence unavailable and surface the limitation; do not silently substitute a summary. |
| Local CPU spike | Continue under configured sharing/limits if control plane remains healthy. |
| Local memory pressure | Stop admission first; checkpoint/terminate resumable sandbox work if release is necessary. |

## 13. Startup and shutdown

### Startup

The deployment sequence should conceptually be:

```text
validate configuration
    -> apply migrations exactly once through deployment/startup tooling
    -> verify PostgreSQL/artifact access
    -> start API, executor, and maintenance processes
    -> scan durable ready/recoverable work
    -> begin LISTEN/NOTIFY wake-up handling
```

Each process initializes only its own local resources.

Missing provider credentials may block runs requiring that provider without necessarily preventing the management UI or deterministic test provider from starting.

### Graceful shutdown

Executors stop claiming new work, persist/checkpoint what they safely can, and release/relinquish leases according to the Part 7 design.

Correctness cannot rely on graceful shutdown always occurring. Abrupt process death must remain recoverable from durable state.

## 14. What Part 1 intentionally does not finalize

The following are explicitly deferred:

- exact repository import/dependency enforcement — Part 2;
- detailed PostgreSQL tables/indexes/migration schema — Part 3;
- typed command contracts — Part 4;
- transaction/idempotency/outbox details — Part 5;
- KG schema and three graph-query algorithms — Part 6;
- exact durable queue, leases, fencing, fairness algorithm, sandbox resource estimator, and retry policy — Part 7;
- council phase state machine and model-session loop — Part 8;
- provider adapter wire formats/model identifiers — Part 9;
- tool authorization details — Part 10;
- context packet and rollover algorithms — Part 11;
- exact SSE event schema/API/frontend recovery behavior — Part 12;
- premortem/report finalization implementation — Part 13;
- test suite implementation — Part 14;
- final build slices — Part 15.

Touching these concepts in Part 1 establishes boundaries only.

## 15. Part 1 acceptance conditions

When implemented later, Part 1 is considered operationally correct only if tests demonstrate at least:

1. Starting a run commits durable work and returns without executing the full investigation inside the HTTP request.
2. Closing/reconnecting the browser does not stop or corrupt a run.
3. Restarting FastAPI does not erase or recreate logical agents/tasks.
4. An agent waiting for another member becomes `WAITING` and consumes no ongoing LLM request solely for that wait.
5. A committed dependency result wakes or is subsequently discovered by executors even if a PostgreSQL notification is missed.
6. Two agents using the same executor pool never receive one another's private session/context state.
7. Remote model calls and local sandbox jobs can proceed concurrently using separate capacity accounting.
8. Untrusted sandbox code cannot read provider/database credentials or unrestricted host resources.
9. A sandbox resource spike cannot silently starve the durable control plane without admission/limit safeguards.
10. Executor death and uncertain provider/tool outcomes remain explicitly recoverable rather than silently duplicated or marked successful.
11. The application remains functionally correct when active storage is hosted on HDD.

## Approved Part 1 architecture

```text
                            USER
                              |
                      React Dashboard
                              |
                    HTTP commands + SSE
                              |
                       FastAPI API
                              |
                        PostgreSQL
                 durable state + events
                    /               \
          LISTEN/NOTIFY             artifacts
                |                       |
                v                       v
       Trusted Executor Pool       Artifact Store
          /       |       \
     Member A  Member B  Member C
        |          |         |
     LLM API    LLM API   LLM API
        |
  local execution needed
        v
      Sandbox Manager
       /     |      \
  Docker  Docker  Docker
  sandbox sandbox sandbox
```

Final Part 1 rule:

> **Run all logically ready work concurrently when its required resource pool has capacity. Persist dependency waits instead of holding requests open. Keep trusted orchestration separate from untrusted sandbox execution. Use PostgreSQL as durable truth and notifications/SSE only as delivery mechanisms. Support HDD-backed local operation as an explicit initial constraint.**
