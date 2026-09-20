# Component-by-component implementation review

**Status:** active design review; Parts 1-2 approved, Part 3 next.  
**Baseline:** [CODE_IMPLEMENTATION_PLAN.md](CODE_IMPLEMENTATION_PLAN.md) preserves the approved code-level proposal. [APP_DESIGN.md](APP_DESIGN.md) remains the complete product specification.  
**Working branch:** `design/code-level-implementation`. Keep changes on this branch unless the owner authorizes another target or a merge.

## Review method

Review one part at a time rather than rewriting the entire architecture repeatedly. For each part, identify:

1. The behavior it must deliver and its responsibilities versus neighboring modules.
2. Its concrete files, interfaces, records, and execution flow.
3. Failure cases, concurrency concerns, permissions, and recovery behavior.
4. Tests and an observable completion condition.
5. Remaining decisions and alternatives, with reasons for the preferred option.

The owner approved the overall code-level proposal. Component refinements become approved only when explicitly agreed and recorded. Discussion notes are not evidence that code exists or tests pass.

## Review order

| Part | Focus | Review state |
|---|---|---|
| 1 | Runtime architecture, processes, event-driven waits, concurrency/resource boundaries, branch-environment/sandbox separation, HDD constraint | **Approved** — [final design](reviews/PART_01_RUNTIME_ARCHITECTURE.md) |
| 2 | Repository layout, agent/application/environment boundaries, and enforceable import/dependency rules | **Approved** — [final design](reviews/PART_02_REPOSITORY_BOUNDARIES.md) |
| 3 | Database schema, identities, immutable versions, constraints, migrations | **Next** |
| 4 | Typed commands, validation, actor attribution, error contracts | Pending |
| 5 | Transactions, idempotency, concurrent revisions, event/outbox consistency | Pending |
| 6 | Dependency tracing, claim history, shared-evidence lineage, graph correctness | Pending |
| 7 | Task/job distinction, leases, fencing, reconciliation, budgets and exact fairness/resource-admission algorithm | Pending |
| 8 | Agent loop, council phases, publication barriers, worker delegation | Pending |
| 9 | Provider contracts, scripted provider, DeepSeek integration, model migration | Pending |
| 10 | Tool gateway, authorization, source access, untrusted evidence | Pending |
| 11 | Context assembly, mandatory state, graph/search retrieval, rollovers | Pending |
| 12 | API contracts, frontend state, graph inspection, SSE event schema and reconnect behavior | Pending |
| 13 | Review tasks, premortem, claim-bound reports, finalization | Pending |
| 14 | Unit/integration/contract tests, model evaluations, failure injection | Pending |
| 15 | End-to-end build slices and verified milestone acceptance | Pending |

## Approved Part 1 boundary

Part 1 is finalized in [reviews/PART_01_RUNTIME_ARCHITECTURE.md](reviews/PART_01_RUNTIME_ARCHITECTURE.md).

It establishes the following runtime-level decisions:

- logical agents, model sessions, tasks, trusted executors, and sandbox containers are distinct concepts;
- FastAPI accepts durable commands but does not own the lifetime of investigations;
- dependencies are persisted as waiting state rather than implemented as repeated polling or long-held model/API calls;
- PostgreSQL state is authoritative and `LISTEN/NOTIFY` may be used as a wake-up signal;
- browser live updates use SSE, while internal agent synchronization remains database/event driven;
- independent ready work runs concurrently when its relevant resource pool has capacity;
- remote model capacity and local sandbox compute are accounted separately;
- scheduling under contention is operational/fairness based, never an intellectual ranking of hypotheses;
- trusted executor processes must be separate from untrusted Docker sandboxes;
- CPU pressure is handled primarily through sharing/limits; memory pressure uses admission control and resumable termination where necessary;
- HDD-backed PostgreSQL/application storage is a hard supported initial constraint; no SSD availability may be assumed;
- the local development machine may be used aggressively, but a protection margin must preserve the OS/database/API/control plane so work can still be recorded and recovered.

Part 1 intentionally does not finalize detailed queue leases, schema, SSE payloads, provider wire formats, database tuning, or exact resource/fairness algorithms. Those remain assigned to later parts.

## Next discussion boundary — Part 3

Part 2 is finalized in [reviews/PART_02_REPOSITORY_BOUNDARIES.md](reviews/PART_02_REPOSITORY_BOUNDARIES.md). It locks the domain/application/agents/environment split, exact import matrix, typed command boundary, declarative environment policy, execution-relevant branch environments, Docker as only one execution mechanism, shared-versus-branch-local record classes, environment-adapter contract, candidate/selection/promotion separation, and automated architecture enforcement.

Part 3 will now define the concrete persistence model: identities, immutable versions, branch visibility, canonical versus branch-local records, candidate/promotion history, source/evidence versions, constraints, indexes, and migrations.

No application implementation, pull-request merge, deployment, or live provider execution is authorized by this documentation publication alone.
