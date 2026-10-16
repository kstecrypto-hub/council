# Part 8 - Agent loop, structured experimentation, and delegation

**Design status:** IN DESIGN. **Decisions 8.1 (nested Karpathy-style experimentation), 8.2 (sandbox-local worker autonomy/resource monitoring), and 8.2a (Docker-volume persistence without a central worker-recovery manager): ACCEPTED, October 14, 2026.** Complete action protocol, final-phase/failure transitions and full Step 8 closure remain to be designed.

**Implementation:** NOT STARTED. **Runtime/evaluation tests:** NOT RUN.

## 1. Purpose and authority

This is a **general-purpose** Council-member loop, not a coding-only optimization agent. The user approves a versioned Project Contract and a neutral, outcome-based semantic phase/checkpoint plan prepared by the Project Orchestrator. The five equal Council members independently own their reasoning and private branch/candidate work; neither Orchestrator, runtime nor Auditor intellectually judges their solution quality or forces CHECKPOINT_READY.

The trusted Council runtime mechanically validates permissions, operation identity, safe resource/budget admission, evidence provenance and checkpoint metadata. The user controls budgets, authority changes and final acceptance. Step 7 owns member-environment scheduling and phase token/cost ceilings; Step 9 adapts providers and local models; Step 10 implements isolated tools; Step 11 owns fresh-session continuation and context selection.

## 2. Accepted nested loops

```text
OUTER COUNCIL LOOP
  user-approved semantic phases
  -> five members independently investigate
  -> all five member-declared checkpoint arrivals
  -> approved customer-local frozen read-only snapshot / sealed independent reviews
  -> shared peer challenge and verification-only /work
  -> closeout and next private revision phase
  -> final candidate review / user acceptance

  MEMBER AGENTIC LOOP (one persistent logical member)
    load approved objective, current phase, own branch, permissions and remaining budget
    -> reason and select authorized action
    -> ACT | DELEGATE | ASK_USER | CONTINUE | CHECKPOINT_READY | BLOCKED
    -> observe tool/worker/input result, store attributable evidence/progress
    -> repeat as decided by that member

    OPTIONAL KARPATHY-STYLE EXPERIMENT CYCLE under ACT
      HYPOTHESIS -> CHANGE/ALTERNATIVE -> TEST/CHECK -> OBSERVE
      -> KEEP | REVISE | DISCARD | INCONCLUSIVE -> RECORD
      -> return to the member agentic loop
```

The experimental loop is an **optional workflow inside the existing ACT/control and durable-operation system**, not an independent AI supervisor, mandatory step after every action, second scheduler, or external framework. The member chooses whether an experiment is meaningful and how many to attempt. Some tasks require source comparison or qualitative counterexample checks, others reproducible code experiments; some tasks require no structured experiments at all.

The Karpathy autoresearch pattern informs **controlled change, evaluation, observation, decision and experiment logging**. It does not impose its original fixed-duration experiment, single numerical objective, coding-only file restriction or indefinite repeat policy on Council.

## 3. Experiment lifecycle, measurement and attribution

An experiment is a branch-private, scoped child of a member phase (or a delegated worker task) with the following **design-level record contract**:

- Identity/ownership: run, member, parent worker/task if applicable, current semantic phase, experiment ID, author and creation time.
- Rationale: question or hypothesis, planned change/alternative, baseline and relevant assumptions; the member explicitly states what evidence could support or weaken its hypothesis.
- Inputs/reproducibility: exact own repo/commit and environment version where applicable, source/data/test IDs and versions, tool commands/configuration, comparison setup, authorization and execution epoch.
- Execution: durable tool/model operation IDs, any delegated worker IDs, start/end and actual outputs/artifact hashes; `NOT_RUN`, `BLOCKED`, `FAILED` and `PASSED` checks are distinguished, not collapsed into an optimistic result.
- Observation: measured metrics **with units, sample/test conditions and uncertainty** when available, or attributed qualitative evidence, counterexamples and limitations where a numerical metric is inappropriate. Protect original sources and preserve before/after context.
- Member disposition: `KEEP`, `REVISE`, `DISCARD` or `INCONCLUSIVE`, explicitly authored by the member with reasons. Never automatically call the highest scalar score the intellectual winner. Decisions are revisions of hypotheses/approaches, not proofs of general validity.
- Durable evidence: immutable attempt/experiment history and links to the canonical Step 6 claims, assumptions, tests, findings and failures. A failed or discarded experiment's **record** remains available even if the failed code changes are reverted; retain disposable artifacts only under authorized storage/retention policy.

A test run is evidence that a specified procedure was executed on specified inputs. It is not automatically proof that the experiment design was adequate. Keep exploratory tests supplied/edited by members distinguishable from protected acceptance/verification harnesses that members cannot silently weaken or replace. Report missing baselines, incomparable test conditions, failures and regressions rather than selecting a flattering number.

Experiments may use nonnumeric criteria or explicit `INCONCLUSIVE`; no universal metric, arbitrary confidence score, forced hypothesis/experiment requirement, automatic code promotion, or separate intellectual judge is added.

## 4. Optional worker-led experiments

A member may `DELEGATE` a bounded experiment or evidence check to an authorized worker. The worker operates in its delegated **branch-scoped** environment/capabilities, consumes the parent's authorized phase budget and returns observed results, method, artifacts and limitations to the **parent**. Worker research remains private to that member until an approved checkpoint publication.

The **parent member** decides what to integrate, whether to repeat or challenge a test and when its own phase is ready. A worker cannot claim the parent's CHECKPOINT_READY, publish another peer's private work, alter protected acceptance definitions, or obtain additional permission/budget from its own initiative. Under accepted Step 8.2, the member—not Council's control plane—chooses worker count, nesting, processes, local models, experiments and internal scheduling; parent budgets and sandbox resource limits apply to the **aggregate**. Worker-owned process/task recovery uses the sandbox's ordinary Docker-mounted persistent workspace, **not** a separate Council worker supervisor. The parent member handles what to resume when the container is started again.

## 4.1 Accepted Step 8.2 policy — internal workers are member autonomy, not Council seats

The five Council members each own **one security/resource-isolated working environment**. A worker is an AI subagent, task, process or recursive delegated operation *inside its parent's authorized sandbox*. It is **not automatically a separate Docker container**, one of the five Council seats, or a separately scheduled global job.

- A member can create, stop, nest and coordinate any number of sandbox-local workers and ordinary subprocesses. **No Council-imposed fixed worker count, parallel-worker count, delegation-depth limit, or time-sliced internal worker scheduler.** There is no requirement that workers all be tracked by an external scheduling system. Their work decomposition and intellectual methods remain the member's decisions.
- Every process spawned within the sandbox shares the **sandbox's aggregate** CPU, memory, process/PID, storage and approved device permissions. Multiple local inference jobs and worker processes do not enlarge that sandbox's resource allotment. The member must work within existing resource and user budget ceilings; it is not entitled to new host capacity just because it spawned children.
- **All** member/worker remote inference calls go through the trusted BYOK model gateway with the parent branch/phase's user-approved cost and token reservations. A child cannot use extra provider credentials, create privileged network paths, access another Council member, or escape the sandbox. The no-limit policy concerns *count/hierarchy*, not privilege, spend or host resources.
- Standard worker parallelism is implemented as processes/agent tasks **inside** the member sandbox, not by giving agents the Docker daemon socket. If a project needs separately isolated child containers, they must be provisioned only through a later authorized **trusted broker**, count against the same aggregate member/host claims and maintain the same isolation; unmediated Docker-in-Docker or privileged sibling-container creation is not authorized.
- The member owns internal worker decisions and integration. Ordinary worker scratch, to-do files, task results, logs and reproducible project definitions persist in the sandbox's **dedicated persistent Docker volume or authorized bind mount** when needed. Consequential model/tool calls, evidence-bearing experiment results, unresolved effects and checkpoint/finalization provenance are still recorded under existing Parts 3–6 obligations. Council does **not** mirror every local worker task, process, fork/join, restart decision or result in an independent worker-recovery service.
- A waiting subagent may release its **internal** compute demand, but the host scheduler only reclaims a whole Council-member execution slot after trusted sandbox quiescence and verified resource release. Internal delegation never creates an extra independent Council-member admission slot.

## 4.2 Accepted Step 8.2 resource monitoring boundary

The monitor is a **trusted Council control-plane component outside every agent-controlled sandbox**, not Windows Resource Monitor and not a container-running worker. For the MVP, it consumes Docker Engine container stats (`GET /containers/{id}/stats`, the underlying data for `docker stats`) and Docker lifecycle/OOM events. It observes **aggregate sandbox metrics**, including all descendant workers. Docker Engine/cgroups enforce configured CPU, memory and PIDs limits; the monitor uses telemetry to protect the host *before* hard limits are hit, while acknowledging that an OOM kill is still possible. CPU saturation typically throttles/slows work; it does not imply completed or unsafe intellectual work.

**Initial configurable monitor policy:**

- Sample running member containers roughly **every 2–5 seconds**, with timestamp/freshness status, backend capability detection and event-driven OOM/crash detection. Sampling is not instantaneous protection against sharp spikes; the hard cgroup limit is the final boundary. Account for Docker CLI versus raw API memory/cache reporting differences.
- Around **80% of the configured sandbox RAM limit**: warning and reduced/advisory admission of *additional heavy operations through trusted gateways/brokers*. Around **90%**: stop granting new heavy brokered work, preferentially quiesce active work at a safe boundary if pressure continues, and notify the member. These percentages are tunable starting heuristics, not a guarantee of no crash and not a ban on arbitrary sandbox-local process creation (which the runtime cannot selectively observe/prevent without invasive controls).
- Keep Step 7's adjustable **~20% physical-host RAM headroom** (increase as required by observed host + OS + trusted control plane). Watch host/WSL2 VM capacity **separately from each container** on Docker Desktop for Windows; a healthy container limit alone does not guarantee host safety. Monitor disk/volume growth and free host space separately; `docker stats` reports block I/O, **not** a complete free-disk or volume-quota service.
- GPU/VRAM telemetry is an **optional separate adapter**, e.g. NVIDIA NVML/`nvidia-smi` when supported; ordinary Docker stats does not promise VRAM accounting or hard per-container VRAM enforcement. If safe shared-GPU capacity/isolation cannot be measured or enforced, use a conservative approved exclusive-device allocation or deny unsafe concurrent GPU use rather than inventing a VRAM cap.
- Monitor/control-plane access to the Docker Engine belongs only to a **trusted, narrowly scoped host-side service**. Never mount `/var/run/docker.sock` or any equivalent unrestricted Engine API endpoint into agent-controlled containers. On stale/unavailable telemetry, fail closed for **new heavyweight admissions** while retaining truthful existing work/UNKNOWN outcomes; reconcile externally observed state before reclaiming capacity.
- Under continued pressure: stop admitting heavy brokered work -> throttle where supported -> durable safe quiescence/suspension of the **whole member** -> backend-confirmed resource release -> same-logical-member restart/recovery. Do not imply the runtime can individually micromanage any agent-created worker; do not mislabel an OOM crash, a timeout or a safety suspension as `CHECKPOINT_READY`.

This is a **design choice**, not a claim that Docker monitoring or thresholds have been implemented or tested. See Part 7, Step 10, and Docker/NVIDIA official documentation referenced in `REFERENCES.md`.

## 4.3 Accepted Step 8.2a — Docker-backed persistence, no worker recovery manager

**Worker persistence is the member's sandbox filesystem responsibility, using Docker's native container storage lifecycle, not a Council-managed worker scheduler/supervisor.**

- Each logical member has an owned, stable, isolation-scoped **named Docker volume** (or explicitly authorized persistent bind mount) containing its private repository/workspace, worker-written progress files/results, locally chosen plans, notes, logs and reproducible environment definitions. Recreate/restart the **same logical member** by mounting the **same authorized storage** after runtime security, checkpoint, execution-epoch, budget and host-admission guards pass. Never mount one member's private volume into another member. Make provisioned volume identity, ownership, backup/retention and mount scope reproducible rather than depending on a transient container ID.
- Docker's **container writable layer is not enough** for state that must survive deletion/recreation. Files on named volumes or durable bind mounts persist through container shutdown/recreation **provided they were durably written and the volume/mount is retained**. `tmpfs`, unflushed buffers and unwritten model/process memory do not survive. If an agent wants interrupted worker context, it must persist that state as files or use its own recoverable task/tool mechanism in its authorized sandbox.
- **Docker restart does not checkpoint live subagent execution.** After exit, crash, OOM or deliberate stop, active worker processes and their in-memory stacks are gone; starting the member container starts its entrypoint anew. The member reads saved work and decides locally which worker steps to resume/re-run. Without saved progress, a worker may need to start again; Council **must not promise instruction-level recovery** or rebuild an entire per-worker task graph on the member's behalf.
- Intentionally **stopped checkpoint-ready, paused or budget-exhausted member sandboxes stay stopped** until Council's whole-member admission schedule authorizes the next run. Do **not** configure indiscriminate Docker `restart: always`/`unless-stopped` or an uncontrolled automatic restart that bypasses Council's five-member resource queue, phase barrier, host headroom, revoked execution bridge, or paused state. The trusted whole-member lifecycle controller uses explicit Docker start/stop/recreation and existing bounded infrastructure retries; the Docker restart facility may be used **only** if it demonstrably obeys those guards.
- The **member** may choose conventions for writing internal worker notes/results and resolving unfinished subtasks. Council does not require a canonical record for every local subprocess. It must still preserve already-required canonical operation IDs, spend reservations, checkpoints, evidence/provenance, immutable reviewer inputs and consequential external effects. Recovering files **does not authorize** blind external API/tool retries: UNKNOWN effects are reconciled under Part 5 before duplicate side effects, with fresh bridge epochs/capabilities and current budgets.
- During a checkpoint, authoritative candidate/volume writes remain frozen and verifier `/work` uses a separate disposable read-only view. Stopping a sandbox for slot reuse **does not delete its owned volume**. Only explicit, verified run-finalization/cleanup and retention policy can remove temporary member volumes; accepted product artifacts and archive reference closure remain under the Part 3/5 archival gates.

**MVP implementation boundary:** use Docker named volumes or controlled persistent bind mounts and coarse **whole-member** start/stop/recreate. No Council per-worker resurrection daemon, process snapshotting/CRIU requirement, new subagent database, or extra worker-level schedule. Persistence/restore, mount isolation, intentional stopped-state, OOM and UNKNOWN effect tests remain **NOT RUN**; no runtime system is built by this design.

## 5. Checkpoint integration and safety

- During private work, experiments may make authorized changes in the member's own branch/candidate. All five members independently emit CHECKPOINT_READY against the Orchestrator's approved phase criteria; runtime checks required frozen SHAs/evidence references **mechanically**, without intellectually scoring readiness.
- At a checkpoint, the trusted **customer-local Git gateway** exports selected, pinned, immutable read-only tree snapshots under approved scope. No public GitHub exposure is the default. All five members submit **sealed** independent assessments before shared debate; experiments/records must not leak other peers' unpublished work or sealed-review data into shared snapshots, caches or retrieval.
- During checkpoint `/work`, an experiment can only **verify**, test/reproduce or compare pinned snapshots in a **separate disposable verifier**. The authoritative candidate and protected acceptance harness are read-only; no candidate commits, fixes or pushes. Revisions of private candidates resume only after verified checkpoint closure.
- Experiment IDs/results and objections become evidence and optional next-private-phase revision inputs, **not** automatic obligations imposed by one Council peer on another. Preserve disputed, inconclusive and failed evidence for peer challenge.

## 6. Budget, context and crash boundaries

There is **no forced general reasoning deadline, fixed number of model cycles or required number of experiments**. Individual provider/tool/experiment *operations* have reasonable safety/resource timeouts. All model/tool/worker experiment spending debits the authorized parent/run/phase budgets under Step 7's pre-dispatch reservation and unknown-effect reconciliation contracts. When phase budget is exhausted the member remains `BUDGET_EXHAUSTED / INCOMPLETE`, not checkpoint-ready.

Member identity, experiment operation IDs, baseline versions, evidence and dispositions persist across context rollover and container reconstruction. An interrupted/UNKNOWN external experiment call is reconciled before possible consequential replay. Step 11 handles which bounded records enter a new model session; lost context does not erase canonical evidence or turn one logical member into new independent reviewers.

## 7. MVP versus deferred scope

**MVP design intent:** one agent-directed optional experiment protocol using existing ACT/tool records, persisted traceable experiment/attempt history, honest before/after evidence, member-authored retain/revise/discard/inconclusive decisions, parent-scoped worker participation, and checkpoint-safe review.

**Deferred:** autonomous experiment schedulers; hard-coded numerical optimization targets; additional experiment-only LLM supervisors; automated global winner scoring; elaborate experiment search trees, cross-member shared private experiments and heavy experiment-data infrastructure before measured need.

## 7.1 Owner-approved Step 8.3 — phase/final candidate readiness (October 15)

**Step 8.3 policy decisions APPROVED; exact Step 4/5 DTOs and Step 8.4 integration IN DESIGN.** [Detailed Step 8.3 policy and deployable boundary](STEP_8_3_MEMBER_PHASE_COMPLETION_AND_READINESS.md).

- Record a **member-authored readiness intent** separately from the trusted runtime's **observed, mechanically verified** Git/evidence pin, whole-member quiescence and resource release. Only the second counts toward an ordinary five-member checkpoint arrival; runtime does **not** judge whether the member's proposed solution is good.
- Preserve an explicit **CONCLUDED_NO_VIABLE_CANDIDATE** member-authored investigation outcome with evidence and limitations. Never claim an implemented working candidate, nor silently satisfy an implementation-required five-member barrier. A feasibility investigation may validly conclude negatively if that is its approved outcome. Step 8.4 must decide final review intake while retaining five real reviewers.
- Unproductive-operation repetition uses existing idempotency, denial, infrastructure retry/timeouts, approved budgets and observable warnings—not a sixth intellectual supervisor, fixed iteration quota, mandatory completion deadline or forced CHECKPOINT_READY.
- Reuse the existing parent-only member readiness, candidate, blocker, lifecycle, event and Step 7 scheduling infrastructure; no new service or agent-worker recovery manager. Awaiting the other members never allows an early-ready member to enter the next private revision phase.

The owner's newly approved [Orchestrator development-pattern library](ORCHESTRATOR_DEVELOPMENT_PATTERN_LIBRARY.md) informs **only the prior, user-approved semantic milestone plan** with relevant development-method examples; no library match still yields a plan. It does not alter member self-declared readiness or determine implementation strategies.

**Step 8 remains IN DESIGN** for full 8.4/8.5. Implementation NOT STARTED, tests NOT RUN.

## 7.2 Owner-approved Step 8.4 — collective synthesis and integrated output (October 16)

**Step 8.4 core direction APPROVED; precise DTO/DDL/revision gates still IN DESIGN.** Read [full domain-agnostic integration design](STEP_8_4_COLLECTIVE_SYNTHESIS_AND_FINAL_INTEGRATION.md).

- Council is **not** primarily a five-version winner-selection workflow. Five private members independently investigate/build; the final checkpoint compares **which aspects of each approach are best supported, why, and whether they combine**.
- The five-member discussion produces an attributable, versioned **Integration/Synthesis Blueprint** containing relevant source and evidence versions, favored complementary components/methods, compatibility constraints, rejected/contested decisions, and outstanding risks; **not** a mandatory contribution from every member or unsupported majority verdict.
- A **dedicated non-voting Final Integration/Synthesis LLM** then builds **one coherent final deliverable** using a separate customer-controlled authorized workspace and existing trusted model/tool/resource/budget infrastructure. Software results are integrated code/products; research results are one evidence-grounded report/analysis/protocol; other domain outputs follow the Project Contract. Do not force five production-complete apps or software-style Git for non-code work.
- **The same five original members independently review the actual frozen integrated deliverable again**, using sealed assessments, real evidence and the existing checkpoint/verification-only rules. New integration revisions need appropriate new version-bound verification; old tests are not silently transferred to new code/output.
- The existing future-failure **six-month-plus premortem** examines the actual integrated result and provisional report, not only the blueprint, before user acceptance; retain dissent, limitations and honest inconclusive results.
- Existing project/user authority, domain-neutral Orchestrator, private local Git and snapshot grants, typed command-only peer exchange, Part 5/7 safeguards and explicit acceptance/archive remain mandatory. **A dedicated integration budget requires user-approved allocation; the earlier suggested 70/25/5 budget is not presumed sufficient for integration.**
- Step 8.3 `CONCLUDED_NO_VIABLE_CANDIDATE` means truthful completed investigation, not a fabricated working build: it can contribute evidence and a real fifth reviewer to this **distinct final investigation submission barrier**, never silently satisfy an earlier ordinary implementation checkpoint.
- Integration Agent is an **execution/synthesis role, not a sixth Council seat, hidden solution judge, or substitute peer reviewer**.

**No implementation, migrations or runtime tests.** Step 8.4 exact integration commands and Step 8.5 closure sequencing still IN DESIGN.

## 7.3 Owner-approved Step 8.5A — structured decisions and verified Blueprint handoff (October 16)

[ADR-30/31 Step 8.5A design contract](STEP_8_5_STRUCTURED_COUNCIL_BLUEPRINT_HANDOFF.md) specifies: five original members author material positions, objections, changes and recommendations through the **existing checkpoint's authenticated structured actions**; trusted backend records complete attribution into the versioned Council Decision Register/Blueprint and cannot manufacture post-hoc consensus from conversation. A Blueprint draft is not execution authority. Its exact source/contract/evidence version must be **mechanically frozen**, then an **executable handoff** requires all five genuine current frontier /done/closeout/obligation gates and **independently observed checkpoint grant/route revocation**, followed by a *separately authorized* Integrator admission. No unanimous technical vote required; supported DISPUTED/DEFERRED items remain honestly disclosed, while missing/failing/incomplete procedural closure blocks execution.

**Only these two Step 8.5A policies are approved.** Full command DTO, exact DDL and physical-operation recovery still IN DESIGN. Implementation NOT STARTED, tests NOT RUN.

## 8. Remaining Step 8 design questions

- 8.2 accepted: no fixed worker count/depth or worker scheduler, trusted Docker/cgroups resource monitoring, and **Docker-mounted persistent workspace with member-owned local worker resume**; no separate Council worker-recovery service. Remaining Step 8 work is the **member action/observation protocol**, externally significant result/provenance boundaries, phase transitions and checkpoint/finalization integration.
- 8.3: member private phases, self-declared final candidate readiness, transition/blocked/recovery behavior, incomplete outcomes without intellectual supervision.
- 8.4: integration of the agent loop with sealed review, checkpoint member `/work` and `/done`, final premortem and explicit termination/completion gates.
- 8.5: precise acceptance scenarios and interfaces for Step 9 providers, Step 10 tools and Step 11 context rollover.

**Step 8 remains IN DESIGN.** Decisions 8.1, 8.2 and the Docker-backed 8.2a persistence policy are approved. No central worker-recovery design remains open; member action protocol, phase/final readiness and checkpoint/finalization integration still require design. Application code and runtime tests remain NOT STARTED / NOT RUN.

## ADR-17/18 local-first checkpoints and conditional experiment reuse (October 14)

Step 8's member autonomy and Karpathy-style optional hypothesis/test loop are unchanged. The previous PUBLIC GitHub checkpoint pathway is **superseded**: ordinary peer evidence comes from customer-controlled immutable selected read-only local Git snapshots granted through a trusted gateway. The member still has unrestricted local-worker autonomy inside its resource-defined sandbox, but no peer obtains raw other-repo credentials or editable persistent volumes. Checkpoint `/work` remains verification-only.

**Success-first memory reuse:** the next member may see an applicable earlier successful experiment/recipe first, but a prior FAILED or INCONCLUSIVE result is a **conditional finding** with versions, environment and failure mechanism; it is *never* an automatically suppressed strategy for a similar task. A member may re-run an earlier failed approach under changed requirements/conditions. Keep parent member's intellectual control and explicit checked evidence. Customer-specific experiments/memory stay in their permitted tenant; generalized cross-customer technique sharing needs informed opt-in and review. Step 11 will define exact ranking/indexing; this is not a completed runtime feature.
