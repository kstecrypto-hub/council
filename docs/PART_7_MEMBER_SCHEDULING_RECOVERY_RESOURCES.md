# Part 7 - member execution scheduling, recovery, and resource controls

**Status:** IN DESIGN; amended October 14, 2026.
**Scope:** runtime scheduling of Council-member execution environments, checkpoint barriers, resource limits, recovery, pause/stop, and budget controls.  
**Implementation status:** NOT STARTED. **Runtime acceptance tests:** NOT RUN.
**Decision record:** [ARCHITECTURE_DECISIONS.md](ARCHITECTURE_DECISIONS.md). Accepted requirements below do not mark Part 7 complete.

## 1. Schedule member environments, not their internal work

Each of five fixed Council members owns and controls its own private sandbox environment during private development.

The trusted Council runtime does **not** schedule or intellectually manage the member's internal tests, files, subtasks, worker decomposition, or development steps. Those remain inside the member's sandbox and branch authority.

Step 7 schedules coarse execution capacity around whole Council-member environments.

```text
Five logical Council members: A B C D E
Host allows N active work sandboxes: N may be 1, 2, 3, 4, or 5.
```

The number of logical Council members does not change with machine capacity. Only wall-clock parallelism changes.

## 2. Member execution slots and phase-budget-bounded private work

The Project Orchestrator prepares a versioned, outcome-based semantic phase/checkpoint plan as part of the approved Project Contract. Each of the five equal members independently runs its own agentic loop until it declares CHECKPOINT_READY for that phase, becomes externally blocked, is paused/stopped, or its authorized **per-member, per-phase token/cost allowance** is exhausted.

**No general reasoning deadline, artificial model-call count, or mandatory private-work time slice establishes completion.** Runtime never emits CHECKPOINT_READY for a member, grades intellectual completeness, or advances the checkpoint because an allowance elapsed.

On phase-budget exhaustion, mark the member **BUDGET_EXHAUSTED / INCOMPLETE**, preserve workspace/continuation and the exact remaining checkpoint obligations, revoke/suspend the execution bridge safely, and release its sandbox slot. The user may approve extra phase allowance or cancel/stop. A budget-exhausted member never satisfies the all-five arrival or review barrier.

With two active slots, Members 1 and 2 run while Members 3-5 wait. When an active member reaches its checkpoint, blocks, voluntarily yields for a durable wait, or exhausts its phase allowance, it releases the slot; the next eligible seat starts in fixed order. A one-slot deployment may wait for Member 1 to reach one of those conditions before Member 2 starts. That elapsed-time trade-off is explicit, not a reason to force a member to claim readiness.

Only **individual tool operations, provider calls, bridge leases, and infrastructure recovery** need enforceable safety timeouts/backoff and bounded cancellation; those are not semantic-work deadlines. A stalled tool cannot hold the host forever. Safe resumption follows the existing epoch fencing, persistence and reconciliation rules.

The runtime schedules **whole member environments**, not their internal reasoning choices or work decomposition.

## 3. Checkpoints are all-member barriers

Every planned semantic checkpoint is a barrier across all five required Council members.

A member can reach the checkpoint before others have started because host capacity forced staggered execution. The early member's repository SHA/state is frozen and it waits; its released slot is used by another member. It cannot begin the next private-development phase.

```text
A READY + B READY + C READY + D READY + E READY
    -> checkpoint opening is eligible
```

A failed, blocked, or disconnected member is not ready. The runtime never silently reduces Council membership or substitutes a new logical reviewer.

A blocked-member record identifies the reason, affected dependencies, attempted recovery, next eligible retry/condition, and consumed allowance. Transient infrastructure recovery uses finite attempts/backoff. Unaffected members may continue to the same barrier; they may not cross it.

When the configured recovery or phase-budget ceiling is exhausted, expose a paused/incomplete run with the missing member and outstanding work. The user may repair/resume or stop under the existing controls. A future explicit membership change would require a new versioned run/protocol decision and would not be reported as the original five-member experiment.

## 4. Barrier semantics

For checkpoint K:

1. each member privately develops toward the outcome-based semantic milestone;
2. on member-declared readiness, runtime records the repository SHA and required metadata;
3. that member may not enter post-checkpoint private revision;
4. its execution capacity is released while other members continue toward K;
5. runtime opens K only when all five required members are ready and publication guards pass;
6. approved member repositories become public; sealed independent review precedes shared discussion;
7. communication closes, repositories return to private, and isolation is verified;
8. each member receives its deterministic return packet and may enter the next private phase as capacity becomes available.

A faster member cannot gain an extra private phase merely by reaching the barrier first. Public visibility is not an approval to modify the frozen candidate or publish new private work.

## 5. Separation from Part 5 task leasing

Part 5 durable operations, leases, retries, and reconciliation govern **trusted runtime work** such as provisioning, external effects, repository visibility, publication, accounting, and lifecycle operations.

These records are not a central intellectual task scheduler for the member. Agent-internal development remains controlled by the member inside its sandbox.

## 6. Checkpoint participation is time-sliced too

All required members arrive before review opens, but their sandboxes need not execute simultaneously.

During sealed review, each member independently inspects frozen candidates; peer review submissions remain withheld. During shared discussion, active members receive/send checkpoint messages and structured actions and may use verification-only /work.

Inactive members retain their logical identities and durable state. The gateway queues ordered messages and actions. On resumption, the same member receives its accumulated messages, current obligations, and latest checkpoint generation before making a new completion decision.

A member may release its slot after /done, while durably awaiting an external dependency, or when its checkpoint/review allowance is exhausted. A member can voluntarily yield at a safe boundary with incomplete obligations preserved; the runtime does not manufacture /done. If a review allowance is exhausted with required actions still open, the checkpoint remains blocked/incomplete until authorized continuation. A member with a stale /done certificate or a new required action re-enters the normal rotation.

A one-slot deployment can execute all five members and revisit them as necessary. It never creates a lightweight replacement reviewer or permits private implementation while the checkpoint is open.

## 7. Durable suspension uses persistence plus container stop

Council does not require long-lived paused containers or process-memory checkpoint/restore for the MVP.

The trusted runtime quiesces the environment, persists reconstructible project state, records the suspension point, and stops the execution container to release compute.

```text
running
 -> stop new admissions
 -> finish/abort to an operation-safe boundary
 -> flush persistent filesystem/database state
 -> record repo SHA and environment version
 -> persist logical continuation and pending-operation references
 -> mark SUSPENDED or CHECKPOINT_READY, as appropriate
 -> revoke execution authority and stop container
 -> confirm resource release
```

Durable state includes, where applicable:

- private workspace, files, repository, and Git metadata;
- project-local databases/data;
- installed project dependencies and reproducible environment definitions;
- member-created configuration, tools, and scripts;
- intentionally retained build/test artifacts;
- logical-agent continuation/recovery state.

The logical sandbox identity persists; the container process/ID need not. Resume reconstructs a container around the preserved private state, validates its identity/environment, restores current canonical obligations, and reissues only authorized ephemeral capabilities.

Open sockets, in-memory processes, GPU state, and other ephemeral execution details are not durable memory. Unflushed or unrecoverable work is reported as lost/uncertain rather than invented in a handover.

Provider tokens, Git-administration credentials, checkpoint credentials, temporary routes, and privileged grants are not preserved inside the member filesystem. Persisting workspace state never persists authority.

## 8. Deterministic seat-order scheduling

Eligible members are admitted to available sandbox slots in stable ascending seat order:

```text
1 -> 2 -> 3 -> 4 -> 5 -> wrap
```

Skip members that need no execution or are blocked by a known dependency/resource condition. Record why a seat is skipped and reconsider it when eligibility changes.

Admission happens when a slot is actually freed by CHECKPOINT_READY, BLOCKED, phase-budget exhaustion, voluntary safe waiting/yield, pause/stop, or other lifecycle release; **there is no mandatory periodic private-work rotation**. A member becoming eligible later joins the current seat order rather than resetting priority to seat 1.

For multiple slots, keep a durable dispatch cursor and reserve seats atomically so concurrent schedulers cannot select the same member twice. Resource constraints may defer an otherwise eligible seat; do not silently prioritize a favored solution.

The finite phase allowance bounds Council-authorized inference spend, not an exact wall-clock duration. Delayed tool work is separately governed by operation timeouts and recovery. The one-slot model may take longer because it waits for the active member's phase result or exhaustion.

Seat number conveys no rank, seniority, intellectual authority, or model-quality preference. No fairness scorer or branch-importance model is required.

## 9. Step 7 / Step 8 execution boundary

Step 7 controls permission to execute and resource consumption. It may cap active sandboxes, remote-call concurrency/rate, local inference resources, spending, and pause/stop behavior.

It does not determine the member's intellectual loop, whether an approach is promising, or substantive completion. The repeated observe/reason/act/delegate/evaluate loop and member-emitted CHECKPOINT_READY, BLOCKED, and candidate readiness belong to Step 8.

Remote and local inference use the same logical loop. Remote requests consume provider calls/tokens/cost/rate allowance. Local inference consumes host resources such as CPU, RAM, GPU memory, and devices.

## 10. Crash recovery fences the old execution first

Each live execution has member_id, execution_epoch, and bridge_session_id. The bridge's authority is ephemeral to that epoch.

```text
detect dead/untrusted execution
 -> revoke old epoch and temporary routes/credentials
 -> request cancellation of known in-flight calls where supported
 -> retain uncertain effects as UNKNOWN_PENDING_RECONCILIATION
 -> reconstruct the member environment
 -> validate isolation/lifecycle boundaries externally
 -> apply operation-specific recovery and dependency gates
 -> issue a fresh epoch only for capabilities safe to resume
 -> restore canonical continuation and obligations
 -> resume the same logical member where safe
```

Old epochs stay invalid. Delayed requests cannot execute. Late results may be recorded only through explicit reconciliation tied to the original operation/attempt; they cannot directly advance the restarted member or duplicate an effect.

Revocation blocks future authorized traffic; it does **not** prove that a request already submitted to an external provider stopped. Cancellation requested, cancellation confirmed, and outcome unknown are different records.

Recovery policies:

| Operation class | Resume/retry rule |
|---|---|
| Read/retrieval/inference without external mutation | Independent work may resume after isolation checks; quarantine stale results, preserve uncertain usage/reservations, and repeat only under the adapter's explicit policy. |
| Consequential external write | Reconcile before repeating the effect; block dependent work while its outcome matters. Unrelated safe work need not stop. |
| Authority, visibility, or isolation mutation | Fail closed for the affected boundary until the safe state is confirmed. |

An operation may remain unknown without permanently stopping all unrelated work. Conversely, a newer session is not evidence that an old write failed.

Docker restart policy may restart a process, but it cannot reopen external authority before Council recovery guards pass. Intentional suspension remains stopped until scheduled; it must not be undone by an unconditional restart policy.

## 11. Sandbox checker and peer-verification boundary

A trusted component outside agent-controlled environments validates:

- logical member/sandbox identity;
- private workspace/volume attachment;
- absence of Docker-daemon/socket access;
- absence of unexpected host/peer mounts;
- network/capability routes and stale credential removal;
- resource limits and current execution mode;
- frozen snapshot identity when applicable.

It does not judge code quality or reject ordinary private code changes.

Check on create/reconstruct, crash restart, checkpoint transitions, and other security-sensitive lifecycle changes. A failure fences the affected environment and requires repair plus re-check.

Peer executable verification runs in a **separate disposable verifier**, not the reviewer's persistent candidate environment. It receives pinned inputs and isolated scratch storage, no writable member/continuation/control-plane mounts, no provider or repository-administration credentials, and only approved capabilities. Count its resource and spending use against the requesting branch and run.

The trusted runner records the actual candidate/environment/harness identities, invocation, exit state, and hashed outputs outside candidate control. Export only explicit evidence artifacts for interpretation. Successful execution does not establish that the test was adequate, and candidate-supplied tests are distinguished from protected acceptance checks.

The detailed containment implementation remains Step 10 work. Ordinary container use is not a claim of absolute protection against hostile workloads.

## 12. Resource admission and spending reservations

Admission uses a resource vector: sandbox slots, CPU limits, RAM, disk capacity/I/O limits where enforced, GPU memory, devices, and remote-call concurrency/rate. A single computer-power score is not sufficient. A simple conservative admission check is enough; an optimizer is not required.

Keep headroom for trusted runtime/database/recovery work. Host pressure stops new admissions, then quiesces eligible work safely if needed. Do not claim resources released until the backend confirms release. Unknown or unsupported capabilities remain unavailable rather than being guessed.

Spending is reserved **before dispatch** in an atomic transaction that checks run, branch, parent/worker, and applicable review allowances together. Concurrent calls must not all spend the same remaining balance.

```text
available development allowance
 = total ceiling
 - settled spend
 - outstanding reservations
 - uncommitted protected review/finalization reserve
```

Outstanding reservations include any review allowance already allocated to a request so that it is not subtracted twice. Use fixed-precision money/token accounting with explicit units and pricing version.

Reserve a conservative upper bound from the actual input and permitted output/call limits. Unknown prices do not mean free: block cost-capped dispatch until an approved bound is available, or use an explicitly approved alternative metering policy. This bounds Council-authorized dispatch, not arbitrary provider billing behavior outside its contract.

All calls count: members, workers, retries, Orchestrator, review, verification, and finalization. Children inherit narrower/equal permissions and consume parent allowance. Settled usage cannot be erased by retrying or changing sessions.

A reservation expires safely only before confirmed dispatch. For dispatched or uncertain calls, retain it until usage/effect reconciliation or conservative settlement; a missing response does not refund spend. Retry needs another authorized reservation unless the provider contract proves it reuses the original charged operation.

Protected review/finalization allowance cannot be consumed by ordinary development. Reallocation requires the recorded budget policy/user authorization; it cannot happen silently to keep an agent running. Exhaustion produces blocked/partial outcomes, not forced agreement.

### Per-phase budgets and non-binding token forecasts

- The approved Project Contract defines semantic phase objectives and checkpoint criteria. Each member receives a configurable **hard token allowance for each phase**, plus the applicable cost ceiling. A dedicated protected allowance covers checkpoint review, required communication, and finalization. The budget boundary must include member calls, child workers, retries, model-session rollovers and any chargeable orchestration work using explicit accounting scopes.
- A member itself decides semantic readiness and emits CHECKPOINT_READY. If phase tokens or allowed spending run out first, record BUDGET_EXHAUSTED / INCOMPLETE, preserve the work, and ask the user to extend the affected allowance or stop. Never infer CHECKPOINT_READY, /done, acceptance, or agreement from budget exhaustion.
- Token metering records input and output tokens (and cached-token accounting when available) by model/provider/runtime with explicit units. Remote providers may apply different pricing; local inference still uses a token allowance although there may be no provider fee. Do not pretend token counts are equivalent measures of capability across models.
- **Optional estimates are planning forecasts, not approved quotas or guarantees.** Before approval, Council may display a rough *range* for the overall project and for each phase/member (with an associated indicative cost range by selected model), along with uncertainty/assumptions and whether the estimate is based on comparable historical runs or a weak heuristic. If evidence is too sparse, show 'insufficient data' rather than a fabricated number.
- Estimates may have a very wide error margin, should be calibrated/revised against actual usage over time, and must never automatically expand, shrink, or substitute for user-approved hard phase/run budgets. Display estimated vs. authorized vs. actually spent values separately. Approval of a budget is a decision by the user, not by the estimation algorithm.

## 13. Pause, stop, and unknown outcomes

Pause stops new ordinary admissions, reaches durable boundaries, and suspends members. Safety work such as fencing, reconciliation, and cleanup remains permitted within its existing scope. Do not claim all processes paused while they are still quiescing.

Stop prevents new ordinary work, fences epochs, requests supported cancellation, records pending external effects, and cleans controllable resources. It does not undo completed effects or assert that unknown provider calls were cancelled.

The run remains STOPPING or enters an explicitly failed/incomplete cleanup outcome while required boundary safety is unresolved. A user-visible stop report states known effects, unresolved operations/reservations, cleanup performed, and remaining constraints. Never hide uncertain consequential writes behind a success label.

Resume rechecks the current contract, permissions, budgets/reservations, resource availability, operation dependencies, and isolation. Restored framework state is continuation only; canonical Council operation and authorization records take precedence.

## 14. Still to design before Part 7 is marked DESIGNED

The accepted behavior above is not a completed scheduler. Open work includes:

- concrete validation/default proposals for per-member/per-phase token budgets, cost ceilings, protected review allowances, tool-call timeouts, recovery retry/backoff ceilings, and host headroom (without semantic-work time limits);
- provider-specific token metering and cost accounting, local-model sizing/compatibility measurements and remote concurrency/rate contracts;
- exact reservation/accounting schema, lock ordering, dispatch/settlement transactions, and review-reserve allocation;
- precise pause/stop state/event wiring with Part 4 and provider-specific cancellation behavior;
- backend-specific enforcement, crash-safe environment persistence, and proof of resource release;
- optional historically calibrated token-usage estimation with uncertainty disclosures (not a prerequisite for agent readiness);
- full failure-injection and deterministic acceptance tests.

These choices must be resolved without weakening the accepted boundaries. Application implementation and runtime tests remain NOT STARTED / NOT RUN.

## 15. Required acceptance evidence (all pending)

- [ ] A one-slot run admits the next eligible member after the active member reaches its milestone, blocks, safely yields, or exhausts its phase allowance; no forced readiness is inferred.
- [ ] A member that exhausts its phase token/cost ceiling remains INCOMPLETE with recoverable state; no checkpoint/review barrier crosses and no implicit top-up occurs.
- [ ] The approved phase budget, uncertain planning estimates, and metered actual usage are distinguished; unknown dispatched operations retain conservative reservations.
- [ ] Concurrent dispatchers do not double-schedule a member or oversubscribe resources.
- [ ] A failed/blocked member cannot silently shrink Council or open the arrival barrier.
- [ ] Time-sliced sealed review and discussion retain independent reviews and all message obligations.
- [ ] Unknown inference permits safe unrelated progress while retaining usage reservations.
- [ ] Unknown external writes are not replayed blindly; unknown visibility/isolation fails closed.
- [ ] Stale epochs and delayed completions cannot authorize new actions or overwrite current state.
- [ ] Concurrent member/worker/Orchestrator requests cannot overspend one balance or consume protected review funds.
- [ ] Peer test code cannot alter a reviewer's candidate, continuation, or trusted acceptance definition.
- [ ] Pause/stop/restart under active calls preserves actual effects, resources, reservations, and honest status.
