# Component-by-component implementation review

**Status:** discussion agenda, not implemented functionality.  
**Baseline:** [CODE_IMPLEMENTATION_PLAN.md](CODE_IMPLEMENTATION_PLAN.md) preserves the approved code-level proposal. [APP_DESIGN.md](APP_DESIGN.md) remains the complete product specification.  
**Working branch:** `design/code-level-implementation`. Keep changes on this branch unless the owner authorizes another target or a merge.

## Review method

Review one part at a time rather than rewriting the entire architecture repeatedly. For each part, identify:

1. The behavior it must deliver and its responsibilities versus neighboring modules.
2. Its concrete files, interfaces, records, and execution flow.
3. Failure cases, concurrency concerns, permissions, and recovery behavior.
4. Tests and an observable completion condition.
5. Remaining decisions and alternatives, with reasons for the preferred option.

The owner approved the overall code-level proposal, not every new refinement that may be proposed during this review. Label new conclusions as proposed until agreed. Discussion notes are not evidence that code exists or tests pass. Do not silently promote a review suggestion into the authoritative design.

## Review order

| Part | Focus | Initial review state |
|---|---|---|
| 1 | Application structure: modular monolith, processes, responsibilities, startup/shutdown, failure boundaries | Current discussion topic |
| 2 | Repository layout and enforceable import/dependency rules | Pending |
| 3 | Database schema, identities, immutable versions, constraints, migrations | Pending |
| 4 | Typed commands, validation, actor attribution, error contracts | Pending |
| 5 | Transactions, idempotency, concurrent revisions, event/outbox consistency | Pending |
| 6 | Dependency tracing, claim history, shared-evidence lineage, graph correctness | Pending |
| 7 | Task/job distinction, leases, fencing, reconciliation, budgets | Pending |
| 8 | Agent loop, council phases, publication barriers, worker delegation | Pending |
| 9 | Provider contracts, scripted provider, DeepSeek integration, model migration | Pending |
| 10 | Tool gateway, authorization, source access, untrusted evidence | Pending |
| 11 | Context assembly, mandatory state, graph/search retrieval, rollovers | Pending |
| 12 | API contracts, frontend state, graph inspection, live updates | Pending |
| 13 | Review tasks, premortem, claim-bound reports, finalization | Pending |
| 14 | Unit/integration/contract tests, model evaluations, failure injection | Pending |
| 15 | End-to-end build slices and verified milestone acceptance | Pending |

## First discussion boundary

Start with Part 1: how one codebase runs an API, workers, and maintenance against durable state, without turning the software scheduler into an intellectual leader. Clarify the distinction between a logical agent, its model session, and a worker process. Discuss request acceptance, execution, record persistence, browser reconnection, and process failure.

Do not use Part 1 to silently finalize the detailed schema, deployment platform, secret-store implementation, dependency pins, exact scheduler fairness algorithm, or quantitative budget settings. Those remain part-specific decisions.

No application implementation, pull-request merge, deployment, or live provider execution is authorized by this documentation publication alone.
