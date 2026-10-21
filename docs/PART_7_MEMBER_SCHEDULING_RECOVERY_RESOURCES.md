# Part 7 - member execution scheduling, recovery, and resource controls

**Design status:** DESIGNED (specification approved October 14, 2026).
**Scope:** runtime scheduling of Council-member execution environments, checkpoint barriers, resource limits, recovery, pause/stop, and budget controls.  
**Implementation status:** NOT STARTED. **Runtime acceptance tests:** NOT RUN.
**Boundary:** Defaults below are configurable recommendations; provider/runtime-specific adapters and enforcement tests belong to implementation and Step 9/10. This specification does not claim any working scheduler.
**Decision record:** [ARCHITECTURE_DECISIONS.md](ARCHITECTURE_DECISIONS.md). Part 7 is **DESIGNED as a specification**; approved requirements below do not mark its resource monitor, scheduler or runtime tests implemented or verified.

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

The Project Orchestrator prepares a versioned, outcome-based semantic phase/checkpoint plan as part of the approved Project Contract. Each of the five equal members independently runs its own agentic loop until it declares CHECKPOINT_READY for that phase, becomes externally blocked, is paused/stopped, or its **current operator/user-authorized run/account/protected-pool exposure or expressly configured optional member/phase cap** is exhausted. ADR-53 supersedes mandatory fixed per-member/per-phase token budgets.

**No general reasoning deadline, artificial model-call count, or mandatory private-work time slice establishes completion.** Runtime never emits CHECKPOINT_READY for a member, grades intellectual completeness, or advances the checkpoint because an allowance elapsed.

On actual approved spending/resource/token-limit exhaustion, mark the member **BUDGET_EXHAUSTED / INCOMPLETE**, preserve workspace/continuation and exact remaining checkpoint obligations, revoke/suspend the execution bridge safely, and release its sandbox slot. The authorized funding owner may approve an increased funded ceiling or appropriate approved pool revision; ordinary member/phase planning forecasts do not require a top-up. A budget-exhausted member never satisfies the all-five arrival or review barrier.

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
6. approved **customer-local pinned read-only snapshots** become visible only to authorized checkpoint reviewers; sealed independent review precedes shared discussion;
7. communication closes, temporary snapshot grants/routes are revoked and isolation is verified;
8. each member receives its deterministic return packet and may enter the next private phase as capacity becomes available.

A faster member cannot gain an extra private phase merely by reaching the barrier first. Checkpoint-scoped snapshot read access is not permission to modify frozen candidates, access unpublished peer work or publish source outside the customer's trust boundary.

## 5. Separation from Part 5 task leasing

Part 5 durable operations, leases, retries, and reconciliation govern **trusted runtime work** such as provisioning, external effects, local snapshot export/grant/revocation, optional explicitly authorized external Git publication, accounting, and lifecycle operations.

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

### 7.1 Docker storage and process-restart policy (approved Step 8.2a)

- Persistent member-private files, Git workspaces and agent-written worker notes/results live on **member-scoped named Docker volumes** (or authorized persistent bind mounts) with stable volume identities independent of transient container IDs. Recreated containers must mount the **same authorized** private storage; Docker's container writable layer, process RAM and `tmpfs` are not sufficient for recreation persistence.
- Stopping and restarting a container **does not preserve running worker processes or their execution stacks**. On restart, the container entrypoint starts again and the Council member chooses how to resume its own workers from saved workspace artifacts. Council does **not** maintain a per-worker resurrection table, autonomous worker scheduler, or process-memory snapshot/CRIU requirement. If the worker did not save progress, it may have to repeat local work.
- Deliberately stopped, checkpoint-ready, paused and budget-exhausted sandboxes **must not restart themselves** outside the Step 7 whole-member admission schedule. Docker restart policies such as unconditional `always`/`unless-stopped` cannot bypass budget/permission, barrier, host headroom and security checks. Start/recreate is authorized only after the existing epoch-fencing, unknown-effect reconciliation, sandbox checker, stable volume identity and resource admission guards.
- Agent-owned local worker resumption does not override canonical member continuation, evidence/provenance or consequential external-operation records. Before retrying external API/write/tool operations, reconcile their existing operation IDs/UNKNOWN outcomes under Parts 3–5, then issue new authority only for allowed work.
- Intentional suspension preserves volumes and provenance; verified final teardown follows the accepted-project archive/retention gates. Do not casually `docker volume prune` member data or use a removal option that implicitly deletes the **only** retained workspace. Check restored filesystem identity, contents and ownership from a fresh container during Step 10 validation.

This is a **specification**. Container/volume recovery and security tests remain NOT RUN, and no worker-specific recovery service is required.

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

- The approved Project Contract defines semantic phase objectives and checkpoint criteria. Under ADR-53 members **share their authorized development pool adaptively** without mandatory hard token/currency allocations per phase or member; explicitly selected tighter member/phase limits remain enforceable **optional** controls. Five protected funded scopes and aggregate run/account ceilings still bound dispatch. Chargeable member calls, workers, retries, rollovers, reviews and orchestration use their exact authorized spend scopes.
- A member itself decides semantic readiness and emits CHECKPOINT_READY. If the **real funded pool/run/account ceiling or an explicitly configured optional phase/member limit** blocks the next call, record BUDGET_EXHAUSTED / INCOMPLETE, preserve the work and permit authorized increase or stop. A planning estimate being exceeded is **not** exhaustion. Never infer CHECKPOINT_READY, /done, acceptance, or agreement from limits.
- Token metering records input and output tokens (and cached/reasoning tokens when available) by model/provider/runtime with explicit units. Remote providers may apply different pricing; local inference uses bounded model-request context/output and host resource controls, but no mandatory hard member/phase token allocation. Tokens are not interchangeable measures of reasoning capability.
- **Optional estimates are planning forecasts, not approved quotas or guarantees.** Before approval, Council may display a rough *range* for the overall project and for each phase/member (with an associated indicative cost range by selected model), along with uncertainty/assumptions and whether the estimate is based on comparable historical runs or a weak heuristic. If evidence is too sparse, show 'insufficient data' rather than a fabricated number.
- Estimates may have a very wide error margin, should be calibrated/revised against actual usage over time, and must never automatically change **authorized run/account/protected-pool exposure**. Internal planning shares may adapt within an already approved pool, without new paid authority or user prompts for merely exceeding a forecast. Display estimated vs. authorized vs. reserved/settled/uncertain usage separately. Approval of additional funded spending belongs to the operator for operator-funded calls or to the user for BYOK calls, not to the estimator.

### MVP funding and API-key ownership

- **ADR-53 MVP pilot: Council/operator-funded API credentials by default, optional user BYOK, and compatible local inference.** The selected operator or user provider-account reference is resolved and authorized before each call; a worker never inherits a broader credential. Credentials never enter sandboxes/repos. User BYOK is optional, not compulsory.
- The external provider bills the **actual account owner**: operator for `OPERATOR_FUNDED`, or user directly for `USER_BYOK`. No prepaid wallet, resale of tokens or Council-operated merchant billing engine is introduced by operator paying its own pilot model API bills. A future customer-facing subscription/payments product is a separately authorized business decision.
- The **appropriate funding owner** authorizes aggregate run/account exposure and five protected pool ceilings; **per-member/per-phase hard limits are optional**, not an automatic consequence of a nonbinding forecast. Council conservatively reserves permitted calls before dispatch and records provider prices/usage; these bounds restrict **Council-authorized requests**, not the final provider invoice. Uncertain/dispatched calls and billing delays can affect actual charges; use provider-side limits where available.
- **Operator-owned and user BYOK credentials** both stay encrypted in trusted runtime-managed storage outside agent sandboxes, model prompts, Git, regular logs and browser persistence. Use an n8n-inspired **design pattern** (separate master and rotating data-encryption keys), not unreviewed n8n source code; rotate/revoke and isolate by provider owner/user/deployment. Only the scoped model bridge resolves secrets with current epoch/grants.
- **Deferred commercial option (NOT MVP):** charging users for operator-funded tokens, prepaid user inference credits/wallet, reseller markup, refund/chargeback/tax/compliance/payment infrastructure. **Operator paying the provider directly for its own pilot key is approved now** and does **not** create a reseller wallet.

## 13. Pause, stop, and unknown outcomes

Pause stops new ordinary admissions, reaches durable boundaries, and suspends members. Safety work such as fencing, reconciliation, and cleanup remains permitted within its existing scope. Do not claim all processes paused while they are still quiescing.

Stop prevents new ordinary work, fences epochs, requests supported cancellation, records pending external effects, and cleans controllable resources. It does not undo completed effects or assert that unknown provider calls were cancelled.

The run remains STOPPING or enters an explicitly failed/incomplete cleanup outcome while required boundary safety is unresolved. A user-visible stop report states known effects, unresolved operations/reservations, cleanup performed, and remaining constraints. Never hide uncertain consequential writes behind a success label.

Resume rechecks the current contract, permissions, budgets/reservations, resource availability, operation dependencies, and isolation. Restored framework state is continuation only; canonical Council operation and authorization records take precedence.

## 14. Approved MVP defaults and validation

The following are **default proposals accepted for the architecture**, not immutable pricing, time limits on reasoning, or statements of measured capacity. They are shown to the user and can be overridden subject to validation. User-approved budgets and permissions are versioned and authoritative; no estimator can silently alter them.

### 14.1 User budget and phase allowances

- Funded run/account **spending exposure and five protected scopes** are approved by the relevant provider-credential funding owner (**operator-funded pilot** or **BYOK user**) under the Project Contract. The user still approves the project scope and source/egress requirements. Provider bills the actual account owner, and Council does not collect a prepaid wallet deposit.
- **ADR-27:** propose five distinct project-specific protected, user-approved spend scopes for member development, checkpoint review, final integration, post-integration original-five validation/premortem and overhead. No default universal percentage.
- Each member's monetary and token allocation must reflect approved project/model needs; no mandatory equal 14% monetary shares.
- Member/phase budget **shares are adaptive within the already approved development pool**. Model-specific token caps can be **optional** tighter controls if chosen; they're not mandatory or derived from cost estimates as guaranteed reasoning quotas. If per-request cost cannot be conservatively bounded, deny that dispatch or require a newly approved bounded metering method without silently spending past authority.
- The total budget must cover all chargeable member, worker, Orchestrator, checkpoint, verification and finalization requests. Allocate the associated request to exactly one spend pool and the relevant parent/run scopes; do not double-count the protected reserve. Local inference consumes approved token/resource allowances but normally no third-party inference API cost.
- `BUDGET_EXHAUSTED / INCOMPLETE` preserves the same logical agent and unfinished phase when a **real** run/account/pool cap (or configured optional tighter cap) blocks admission. Within-pool reallocation does **not** require a new spending approval; raising paid exposure or transferring money **across protected pools** requires an authorized funding-owner revision. Rejecting a top-up never marks a member ready or consumes another pool.
- Show `estimated range`, `approved ceiling`, `reserved`, `settled actual`, and `unknown pending reconciliation` separately. Forecasts remain optional and may say `insufficient data`.

### October 16 ADR-27 — superseding integration-aware budget planning default

**Owner-approved refinement:** For the now-required single integrated final deliverable, the former **70% independent development / 25% checkpoint review / 5% orchestration-finalization** recommendation above is a **historical superseded default** and must not remain the product's current initial allocation. The new setup proposes **five protected, project-specific categories**—(1) independent member development, (2) checkpoint reviews/comparison, (3) single Final Integrator/Synthesizer implementation, (4) five-member *post-integration* review/revision checking plus sealed six-month-plus premortem, and (5) orchestration/report/export overhead. The authorized provider-credential funding owner approves aggregate run/account and five protected pool spending ceilings; optional tighter token/phase caps may be configured; **no universal replacement percentage was approved**. Any suggested example (45/15/20/15/5 or otherwise) is non-authoritative, project-dependent and editable, with honest estimation uncertainty.

A separate Final Integrator execution authority must be admitted only after **its own protected pool** is approved and a **protected five-member validation/premortem allowance** exists with enough room for the minimum required next operations. Budget reservations retain existing run/phase/member/parent/worker/operation idempotency and UNKNOWN liability protections. Each chargeable operation is attributed to **exactly one** pool while respecting total-run/parent limits. Member development/review cannot silently consume integration/re-review funds; an integrator cannot borrow a review allowance. Only **cross-protected-pool transfer or increased funded run/account/pool exposure** requires a new explicit versioned funding-owner authorization. Internal member/phase planning shares can change automatically within their existing approved pool; chosen optional hard member/phase caps still apply. An insufficient or exhausted pool remains blocked/incomplete, never a declaration of readiness or verified review. Local models still need token/resource ceilings.

This is an **approved architecture specification only**. Neither budgets nor schedulers have been implemented/tested. [Detailed Step 8.4 §9](STEP_8_4_COLLECTIVE_SYNTHESIS_AND_FINAL_INTEGRATION.md).

### October 16 Step 8.5B — stable Integrator identity, whole-agent admission and protected review reserve

The **one non-voting Final Integrator** is a stable logical execution identity in the trusted run, with isolated durable customer-owned workspace/artifact namespace across model calls and authorized whole-agent Docker container restart/recreation. **No in-memory process or worker stack is restored** on recreation. The existing Step 7 whole-agent resource-vector scheduler may run/suspend/recover it, but not convert it to a sixth Council reviewer or install a per-worker central resurrection manager. Its internal work/worker calls charge its **separate user-approved integration pool** and inherit its current epoch/permissions. Before admitting integration/revision, verify the exact executable frozen Blueprint, new source grants, user-approved model/egress/sandbox permissions, cost limits and **protected post-integration five-member review/premortem allowance**. Host-resource pressure, incomplete suspension, unsafe restart and unknown effects block admission conservatively.

Integrator-authored output intent yields **no** resource-release or review-ready proof by itself. The trusted runtime externally verifies quiescence, exact immutable candidate/artifact hash, outstanding effect reconciliation and whole-agent resource release before the actual reviewed output is eligible. Crashes safely preserve its workspace, stable identity and action history, fence old epochs, and require Step 5 operation-class reconciliation before retrying consequential effects. Running out of money yields **INCOMPLETE**, not ready or borrowed reviewer funds. [Full Step 8.5B](STEP_8_5B_FINAL_INTEGRATOR_EXECUTION_AND_RECOVERY.md). Design only; no scheduler, migration or tests implemented.

### 14.2 Inference concurrency and resource admission

- Remote API inference starts at **up to two concurrent requests per provider**, reduced further by actual provider/account limits, request-token and output-token budgets, rate-limit headers, and retry-after signals. Concurrency may increase only after measured/verified capacity and user configuration. Different providers may have different caps.
- Local inference starts at **one active inference job**; increase only after a concrete model + quantization + runtime/context profile passes Step 9 compatibility tests and measured memory/compute admission. A model whose tool-loop compatibility or resource fit is unknown is not silently considered Council-seat compatible.
- The one-job cap describes the **trusted shared local-inference gateway**, not a fixed number of subagent processes permitted inside a member sandbox. Workers and recursively spawned subagents are unrestricted in count/depth within the sandbox but remain bounded by its aggregate cgroups/resources and the parent's token/cost budget. Do not introduce another Council worker scheduler.
- Continue the **same fixed seat-order member queue** 1 -> 2 -> 3 -> 4 -> 5 when slots free. Local-model inference jobs and remote-provider requests consume independently metered gateway resources; they do not form a second intellectual scheduler. No periodic private-work time quantum is required.
- Initial host RAM headroom target is **about 20% of total physical RAM**, adjusted upward if observed OS + trusted Council runtime + database/recovery usage requires more. GPU VRAM is measured separately for each local model; do not apply the RAM percentage blindly to VRAM. Keep an explicit disk/workspace reserve and avoid uncontrolled oversubscription; unmeasurable capacity is not assumed free.
- On resource pressure: stop admitting new heavy operations first; then throttle concurrency; then safely quiesce/suspend an active member if necessary. Preserve durable state. If host safety or isolation cannot be restored, mark the affected member blocked / run paused with an actionable reason. Release a slot **only after the backend confirms container/resource release**.

### 14.3 Timeouts and bounded infrastructure recovery (not reasoning deadlines)

- Default automatic **three infrastructure-recovery retries** after a failed attempt with increasing delays **5s / 30s / 120s**, configurable by operation/backend. Enforce a finite retry ceiling and record all attempts. Exhaustion leaves the required member `BLOCKED`, preserving its identity, data, outstanding operations and the five-seat barrier.
- Use **operation-class safety timeouts**, not a universal model reasoning deadline. Suggested initial profiles: network connect 15 seconds; ordinary read-only HTTP/tool operation up to 120 seconds; single provider inference request up to 20 minutes with an independent configurable no-progress/stream-idle threshold; ordinary local command up to 10 minutes. Declared long-running operations may receive an approved larger bounded limit. Provider-specific contracts and measured runtime behavior may override these *per-operation* settings.
- Timeout means `request timed out`, **not** `provider did not charge` or `external effect did not happen`. Cancel where supported, revoke stale epochs, and preserve UNKNOWN outcomes/reservations until reconciliation. Repeated failure never fabricates completion.

### 14.4 Approved trusted Docker resource monitor (Step 8.2 amendment, October 14)

This monitoring mechanism is part of Step 7's resource-admission **design**, with Step 10 responsible for actual implementation and sandbox safety tests. Each Council-member sandbox may run arbitrary internal subagents, recursive workers and subprocesses, but its **aggregate** resource limit remains authoritative; worker count/depth is not a Council-level scheduling variable.

**Monitoring source and deployment**

- A trusted, host-side/deployment-control-plane **Resource Monitor** outside agent-owned Docker containers consumes Docker Engine `GET /containers/{id}/stats` (the source behind `docker stats`) for aggregate container CPU, memory, PIDs/threads, network and block I/O. It also consumes Engine container lifecycle and `oom`/`die` events for prompt incident detection. Detect Docker API version and measurement availability; raw memory stats and the CLI differ in cache-adjusted presentation.
- Sample approximately **every 2–5 seconds** as a configurable initial target; record monotonic observation/freshness times, backend ID and metric source. Short spikes can occur between samples; monitoring **cannot guarantee** that a sandbox never crashes.
- Container hard CPU quota/period, memory, PIDs and other **supported** cgroups/Engine limits enforce the sandbox boundary. Memory-limit exceedance can cause Linux OOM kills; a soft alert is not a kernel-enforced process-creation ban.
- Monitor host RAM/free disk and Docker/WSL2 VM capacity in addition to per-container usage. In Windows Docker Desktop with WSL2 backend, WSL2 VM memory/swap limits and host OS headroom are separate from container limits. The approved initial **~20% host RAM headroom** remains tunable. Network/block I/O counters are not remaining disk space; inspect relevant writable layers, volumes/bind mounts, log growth and free space/quota through trusted host/runtime facilities as supported.
- For permitted NVIDIA GPU workloads, use a **separate** NVML/`nvidia-smi` GPU/VRAM observer, checking device and virtualization support. Normal Docker container stats does not provide guaranteed VRAM use or enforce hard per-container VRAM caps. When precise GPU attribution/enforcement is unavailable, be conservative about concurrent GPU allocation; do not invent assurances or silently oversubscribe. GPU restrictions never permit agent Docker socket access.
- Engine API/daemon/socket access is restricted to the trusted monitor/broker only, ideally through a least-privilege internal interface; agents and ordinary child processes **never** receive the Docker socket, daemon credentials, host PID namespace or administrative privilege. Standard subagents run inside their parent's container. Any separately isolated child Docker environment must be provisioned through an approved trusted broker, counted against the parent's aggregate resource claim, not spawned through an agent-exposed Docker API.

**Initial configurable pressure response**

| Observed resource | Suggested policy (not a safety guarantee) |
| --- | --- |
| Container memory below 80% of assigned cap | Normal internal work; maintain host-admission and operation limits |
| Container memory reaches ~80% | Warn and stop/slow **new broker-mediated heavy work** when practical; member remains free to choose its internal workflow |
| Container memory reaches ~90% or keeps increasing | Deny new heavy admissions; if pressure persists, initiate durable safe quiescence of the whole member environment, preserving the same logical member |
| Host/WSL VM RAM, disk, GPU or monitor health unsafe | First close new admissions, then throttle brokered operations, then safely suspend affected whole sandboxes; if safe conditions unknown, do not assume spare capacity |
| Backend OOM/crash/hard-limit exceeded | Record the actual failure and metrics/attempt identity, fence old bridge epoch, retain outstanding UNKNOWN operations, apply the Step 7 bounded recovery protocol; never emit member readiness |

- Council does **not** intercept or individually schedule arbitrary local `fork`/`spawn` calls. No fixed worker count/depth is imposed. Thus the 80/90% gates can restrict future **trusted gateway/broker admissions**, but they cannot promise to prevent an agent from internally spawning a process and hitting OOM. Hard sandbox isolation is the final safety boundary.
- Telemetry loss/staleness fails closed for **new resource-heavy admissions**, not by automatically labeling healthy running members `FAILED` or falsely releasing slots. Existing in-flight effects are reconciled; slot reuse requires trusted backend-confirmed resource release.
- Fast sampling should use bounded overhead and limited retention; record important OOM/resource incidents and threshold actions durably through existing events/operations. Raw high-frequency resource samples can be disposable monitoring data, not permanent Git lessons.

**Implementation and validation pending:** test real Docker Desktop/WSL2 and Linux host behavior, cgroups availability, Engine version, GPU/VRAM adapters, disk/volume limits, threshold actions, stale telemetry, host pressure, OOM, restart and resource-release evidence. Prometheus/Grafana/Windows Resource Monitor are not required in the MVP. This amendment refines the already-DESIGNED Step 7 specification; implementation NOT STARTED, tests NOT RUN.

## 15. Atomic budget and resource admission contract

This is the **canonical design interface** to be integrated into the Part 3/4/5 records; no SQL migrations or model adapter are claimed implemented.

### 15.1 Required canonical records

- `budget_policy_version`: approving **funding owner** (operator or BYOK user), provider-credential funding account/scope, contract/run revision, fixed-precision currency/units, provider pricing-version assumptions, authorized **run/account and five protected pool ceilings**, any optional hard phase/member caps, and effective revision.
- `budget_account`: `run_id`, spend pool (development/review/finalization), optional `member_id` and `phase_id`, token-unit scope, `approved_ceiling`, `settled`, `reserved_unsettled`, `row_version`. Each debit has one assigned pool plus aggregate constraints.
- `usage_reservation`: durable idempotent `operation_id` / attempt, parent worker/member, provider/model/pricing version or local-metering profile, pool, token/cost pre-dispatch upper bounds, status, dispatch epoch, actual returned usage, and reconciliation state. A reservation is not a prepaid wallet/charge.
- `resource_admission`: member execution epoch, seat, sandbox instance, CPU/RAM/VRAM/disk/slot/concurrency claims, admission status, confirmed release, and machine capability snapshot.
- `recovery_attempt`: source failure/operation, attempt count and retry-not-before, sandbox/bridge epoch, observed cleanup and resulting BLOCKED/PAUSED/resumable state. Optional forecasts have **separate** versioned records and cannot authorize dispatch.

### 15.2 Authorize, reserve, dispatch, settle

1. Verify the current approved Project Contract, selected **operator-owned or user BYOK** credential capability (or local model runtime), current credential/funding-owner account and egress scope, model compatibility, spend policy/version, caller/worker authority, phase/checkpoint scope and resource capacity.
2. In **one PostgreSQL transaction**, lock the deployment transactional event clock **first**, then the approved run/account and five protected pool balances and **any configured optional member/phase accounts** in deterministic order. Check applicable monetary/token/request caps with settled plus reserved (including UNKNOWN) spending, respecting protected review funds; deduplicate by operation/attempt idempotency key.
3. Atomically insert the operation, reservation, resource-admission claim, canonical event(s), outbox and idempotent result. **Commit before making any external model/tool request**. Concurrent dispatchers cannot reserve the same money/tokens/slot twice.
4. The trusted model/tool bridge marks `DISPATCHED` durably before handing off the external request, with epoch fencing. If the attempt dies near that boundary and non-dispatch cannot be proven, treat outcome/usage as uncertain; do not blindly refund or replay.
5. On a definite response, settle the actual usage atomically and release only the unused reserved part. A proven no-dispatch/known non-effect may release its reservation. A dispatched or UNKNOWN attempt retains conservative liability until provider-specific reconciliation or an explicitly approved conservative settlement. Retries require a new authorized reservation unless provider semantics prove the same charged operation is reused.
6. Cost/usage arriving late cannot revive an old execution epoch or change semantic completion. All settlements and budget revisions carry versioned canonical events and are exposed to UI projections through the committed outbox.

**No Council-enforced ceiling is a guarantee against the external provider's final bill or the cost of solving a problem.** Operator-funded and BYOK accounting limits Council-authorized outgoing calls; neither mode certifies the final external invoice or a completed problem.

## 16. Pause, stop, recovery, and host-pressure state contract

The existing Part 4 canonical run lifecycle stays authoritative; do not invent a competing state machine.

| Command or cause | Durable status and effect | Completion guard |
|---|---|---|
| `PauseRun` or host safety pressure | `ACTIVE` + activity `QUIESCING_FOR_PAUSE` while bridge admissions close and containers reach durable boundaries | Transition to `PAUSED` only when required suspension/fencing and confirmed resource release have been recorded; unresolved calls remain visible separately |
| `ResumeRun` | `PAUSED` remains until contract, permissions, budgets, obligations, provider capabilities, resources, sandbox checker, and uncertain dependencies pass | Then `ACTIVE` with fresh bridge epoch; otherwise stay `PAUSED` with a reason |
| `StopRun` | `ACTIVE/PAUSED -> STOPPING`; reject new ordinary work, fence epochs, request supported cancellations, record known/unknown effects and tear down controllable resources | `CANCELLED` only after sufficient cleanup/reconciliation, else explicit `FAILED` / incomplete cleanup; never report cancellation as a successful candidate |
| Final user `AcceptCandidate` and gated finalization | User acceptance is separate from `StopRun`, with archive/export and teardown prerequisites | `FINALIZING -> COMPLETED` only after accepted project + Git archive and cleanup are verified |
| Infrastructure recovery failure | Preserve required logical member and durable state as `BLOCKED`; no fifth seat is silently substituted | User can approve repaired continuation, budget expansion, or stop; barrier never crosses |
| Unexpected resource exhaustion | Stop new admissions, reconcile in-flight work, attempt safe quiescence; if unable, fence/contain and expose FAILED/PAUSED as appropriate | No claimed release without backend evidence |

Typed events needed alongside the existing Part 4 catalog: `MemberPhaseBudgetExhausted`, `BudgetPolicyApproved`, `BudgetReservationCreated`, `BudgetReservationSettled`, `BudgetReservationOutcomeUnknown`, `MemberRecoveryAttempted`, `MemberBlocked`, `SandboxQuiesced`, `SandboxResourceReleaseConfirmed`, `BridgeExecutionEpochRevoked`, and `ResourceAdmissionDenied`. Their common envelope, idempotency, outbox ordering, and authorization rules are inherited from Parts 4 and 5. The event records **what occurred**, not that the agent was intellectually finished.

## 17. Design completion boundary and implementation dependencies

**PART 7 DESIGN: DESIGNED.** Configurable defaults, user-budget model, resource admission, atomic reservation ordering, recovery ceilings, and pause/stop behaviors are now specified. The Step 7 design is complete at the architecture level, **not implemented or verified**.

Implementation and measured adapter values remain pending and must not be marked completed: actual provider token/rate-limit adapters and pricing; Step 9 local-model/tool-call profiles; Step 10 Docker backend enforcement, volumes, checker and verified resource release; Part 3 migrations and Part 4/5 state/transaction wiring; and all forced-failure/concurrency/integration acceptance tests. Optional historically calibrated token estimation is deferred until real evidence exists, not required to consider Part 7 designed.

## 18. Required acceptance evidence (all pending)

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
- [ ] Five protected project-specific budget scopes are explicitly user approved with no 70/25/5 default or mandatory equal per-seat share; protect review/integration funds.
- [ ] Provider concurrency respects the lower of the initial two-call cap and actual provider limits; local inference defaults to one until proven safe and admission honors RAM/VRAM/CPU/device headroom.
- [ ] Budget reserve, dispatch, settle, late billing and simultaneous member/worker calls follow event-clock-first lock ordering and never overspend a shared account or incorrectly refund dispatched unknown liability.
- [ ] Three default infrastructure recovery retries apply backoff 5s/30s/120s; a fourth is not silently attempted. Exhaustion retains the same BLOCKED logical member and cannot advance a checkpoint.
- [ ] Individual operation safety timeouts can fence hung provider/tool calls without imposing a semantic reasoning deadline or forcing CHECKPOINT_READY.
- [ ] Pause remains QUIESCING_FOR_PAUSE until suspension and release are verified; Resume revalidates guards; Stop cannot report CANCELLED while required boundary cleanup is unresolved, and acceptance is not inferred from Stop.
- [ ] Operator-owned and optional BYOK secrets stay encrypted outside agent containers. No Council token-wallet requirement, hidden cross-funding-owner fallback, invoice guarantee or promised fixed-price result.
- [ ] Docker Engine API stats and lifecycle/OOM events are collected **outside** agent sandboxes and cover child process resource consumption; no agent can reach the Docker daemon socket or bypass cgroup/resource/tenant permissions.
- [ ] Configurable 2–5-second telemetry, soft 80%/90% sandbox-memory warnings and broker-admission/quiescence guards, real host/WSL2 memory pressure and OOM incidents are correctly reported without pretending to prevent every crash.
- [ ] GPU/VRAM monitoring is explicitly separate and unsupported capabilities fail conservatively; disk/volume/free-space monitoring is separate from Docker block-I/O counters.
- [ ] Unbounded in-sandbox worker hierarchies do not create new member slots, unauthorized budgets, or special host capacity; suspended/crashed sandbox restarts only after durable recovery and trusted resource-release verification.
- [ ] A member's named volume survives stop and container deletion/recreation with exact files and permissions; another member cannot mount it, and Docker writable-layer/tmpfs-only progress is not falsely assumed persistent.
- [ ] A container restart begins a fresh process, not a reconstructed in-memory worker; saved worker artifacts are available to the member, no per-worker Council resurrection occurs, and stopped checkpoint/PAUSED/BUDGET_EXHAUSTED members cannot auto-restart past admission guards.
- [ ] External pending/UNKNOWN operations and user budgets remain authoritative after Docker-backed workspace restart; no duplicate provider/write calls are emitted from restored local files alone.


## Local-first checkpoint amendment (ADR-17, October 14)

The checkpoint admission/suspension, five-member barrier, protected review budget, recovery/slot scheduling and no mandatory work-slice rules remain unchanged. **The older requirement to make GitHub repositories public at checkpoints is superseded**. Step 7 now triggers a customer-local immutable selected read-only snapshot export/grant from the trusted gateway. Actual verified recipient access permits SEALED_REVIEW; actual verified grant/route revocation permits private revisions. The member's own sandbox Git remains under its control and does not gain other branches' unpublished source. See [LOCAL_REPOSITORY_AND_KNOWLEDGE_RETENTION.md](LOCAL_REPOSITORY_AND_KNOWLEDGE_RETENTION.md). Storage/adapters and failure-injection tests are not implemented.

## October 19 — budget planning reconciliation (design-only)

ADR-27 and [Steps 2–8 reconciliation R5](STEPS_2_TO_8_CROSS_STEP_RECONCILIATION_2026_10_19.md) supersede every historical Step 7 70/25/5 **setup default** and assumption of automatically equal member funding. Propose five distinct project-specific, user-approved protected spending scopes with independent-member, checkpoint comparison, Integrator, five-member integrated-review/premortem, and orchestration/report/archive budgets. Existing whole-agent resource queue, capacity limits, budget transaction locks and uncertainty reservations remain. Historical mandatory BYOK and rigid member-phase budget assumptions are superseded by ADR-53. Do not introduce a distinct keyed internal API submission queue. No new runnable scheduler, backend implementation or tests are asserted.


## October 20 ADR-48 — transient MCP tool cooldown distinct from infrastructure recovery

[Approved Step 9 tool-error/agent recovery policy](STEP_9_ADR48_AUTONOMOUS_TOOL_ERROR_FEEDBACK_AND_COOLDOWN.md) directs the existing model gateway and Step 5 operation ledger to apply an initial **180–420-second transient MCP overload/network/rate-limit cooldown** per relevant service/account/connection, honoring longer provider instructions and increasing backoff. The agent may attempt further **safe authorized tool recovery without an arbitrary retry count limit**, within existing resource and protected spend budgets; unrelated members or healthy tools need not stop. This is **not** the same as the **finite container/host restart infrastructure retry policy** already defined in this Step 7 specification, which is preserved. No forced user approval requests for ordinary tool retries, no auto-top-up or privilege expansion, no blind retry of UNKNOWN writes, no new tool scheduler, global queue or watchdog. **Design clarification only, implementation NOT STARTED, runtime tests NOT RUN.**


## October 21 — ADR-53 operator credentials, MCP egress and adaptive protected spending

[Owner-approved Step 9/7 amendment](STEP_9_ADR53_OPERATOR_BYOK_CREDENTIALS_MCP_EGRESS_ADAPTIVE_SPENDING.md) is **normative wherever older Step 7 prose conflicts**: operator API keys for pilot by default, BYOK optional, operator or user account charged appropriately, encrypted credential material outside all agent containers (n8n-inspired design, not copied unreviewed code), and **adaptive same-pool spending across members/phases** without mandatory phase/member hard token ceilings. Preserve project/run/account spending exposure, all **five protected scopes**, local resource/operation safety caps, exact attribution, Step 5 atomic reservation/UNKNOWN reconciliation and BUDGET_EXHAUSTED/INCOMPLETE (never forced readiness). Only optional configured member/phase hard limits are enforced; forecasts are not spending authorization and never guarantee completion. No unauthorized cross-pool borrowing/top-up. Agent-initiated external tools route through approved MCP and outbound Docker networking must prevent direct bypass, while native provider inference and trusted internal Council administration remain separate. **Step 7's scheduling architecture remains DESIGN APPROVED AS AMENDED; runtime/migration/provider/container tests NOT STARTED / NOT RUN.**
