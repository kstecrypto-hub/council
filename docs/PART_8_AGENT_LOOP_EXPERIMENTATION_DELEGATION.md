# Part 8 - Agent loop, structured experimentation, and delegation

**Design status:** IN DESIGN. **Decisions 8.1 (nested Karpathy-style experimentation) and 8.2 policy (sandbox-local autonomous workers + external resource monitoring): ACCEPTED, October 14, 2026.** Precise worker recovery/result handoff, complete action protocol, final-phase/failure transitions, and full Step 8 closure remain to be designed.

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
  -> approved public frozen snapshot / sealed independent reviews
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

The **parent member** decides what to integrate, whether to repeat or challenge a test and when its own phase is ready. A worker cannot claim the parent's CHECKPOINT_READY, publish another peer's private work, alter protected acceptance definitions, or obtain additional permission/budget from its own initiative. Under accepted Step 8.2, the member—not Council's control plane—chooses worker count, nesting, processes, local models, experiments and internal scheduling; parent budgets and sandbox resource limits apply to the **aggregate**. Durable worker result/recovery semantics still require further Step 8 design.

## 4.1 Accepted Step 8.2 policy — internal workers are member autonomy, not Council seats

The five Council members each own **one security/resource-isolated working environment**. A worker is an AI subagent, task, process or recursive delegated operation *inside its parent's authorized sandbox*. It is **not automatically a separate Docker container**, one of the five Council seats, or a separately scheduled global job.

- A member can create, stop, nest and coordinate any number of sandbox-local workers and ordinary subprocesses. **No Council-imposed fixed worker count, parallel-worker count, delegation-depth limit, or time-sliced internal worker scheduler.** There is no requirement that workers all be tracked by an external scheduling system. Their work decomposition and intellectual methods remain the member's decisions.
- Every process spawned within the sandbox shares the **sandbox's aggregate** CPU, memory, process/PID, storage and approved device permissions. Multiple local inference jobs and worker processes do not enlarge that sandbox's resource allotment. The member must work within existing resource and user budget ceilings; it is not entitled to new host capacity just because it spawned children.
- **All** member/worker remote inference calls go through the trusted BYOK model gateway with the parent branch/phase's user-approved cost and token reservations. A child cannot use extra provider credentials, create privileged network paths, access another Council member, or escape the sandbox. The no-limit policy concerns *count/hierarchy*, not privilege, spend or host resources.
- Standard worker parallelism is implemented as processes/agent tasks **inside** the member sandbox, not by giving agents the Docker daemon socket. If a project needs separately isolated child containers, they must be provisioned only through a later authorized **trusted broker**, count against the same aggregate member/host claims and maintain the same isolation; unmediated Docker-in-Docker or privileged sibling-container creation is not authorized.
- The member owns internal worker decisions and integration. Ordinary worker scratch state may remain internal; consequential model/tool calls, evidence-bearing experiment results, unresolved effects, and checkpoint/finalization provenance must be durably recorded in the normal Council control-plane records where already required by Parts 3–6. The exact worker-result return, cancellation and resumed-parent integration wire protocol remains to design.
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

## 5. Checkpoint integration and safety

- During private work, experiments may make authorized changes in the member's own branch/candidate. All five members independently emit CHECKPOINT_READY against the Orchestrator's approved phase criteria; runtime checks required frozen SHAs/evidence references **mechanically**, without intellectually scoring readiness.
- At a checkpoint, repositories are frozen to approved pinned SHAs and made internet-public only after separate user-approved publication/safety checks. All five members submit **sealed** independent assessments before shared debate; experiments/records must not leak peer-private or sealed review data into Git/public snapshots.
- During checkpoint `/work`, an experiment can only **verify**, test/reproduce or compare pinned snapshots in a **separate disposable verifier**. The authoritative candidate and protected acceptance harness are read-only; no candidate commits, fixes or pushes. Revisions of private candidates resume only after verified checkpoint closure.
- Experiment IDs/results and objections become evidence and optional next-private-phase revision inputs, **not** automatic obligations imposed by one Council peer on another. Preserve disputed, inconclusive and failed evidence for peer challenge.

## 6. Budget, context and crash boundaries

There is **no forced general reasoning deadline, fixed number of model cycles or required number of experiments**. Individual provider/tool/experiment *operations* have reasonable safety/resource timeouts. All model/tool/worker experiment spending debits the authorized parent/run/phase budgets under Step 7's pre-dispatch reservation and unknown-effect reconciliation contracts. When phase budget is exhausted the member remains `BUDGET_EXHAUSTED / INCOMPLETE`, not checkpoint-ready.

Member identity, experiment operation IDs, baseline versions, evidence and dispositions persist across context rollover and container reconstruction. An interrupted/UNKNOWN external experiment call is reconciled before possible consequential replay. Step 11 handles which bounded records enter a new model session; lost context does not erase canonical evidence or turn one logical member into new independent reviewers.

## 7. MVP versus deferred scope

**MVP design intent:** one agent-directed optional experiment protocol using existing ACT/tool records, persisted traceable experiment/attempt history, honest before/after evidence, member-authored retain/revise/discard/inconclusive decisions, parent-scoped worker participation, and checkpoint-safe review.

**Deferred:** autonomous experiment schedulers; hard-coded numerical optimization targets; additional experiment-only LLM supervisors; automated global winner scoring; elaborate experiment search trees, cross-member shared private experiments and heavy experiment-data infrastructure before measured need.

## 8. Remaining Step 8 design questions

- 8.2 pending implementation detail: accepted **no fixed worker count/depth or internal scheduler** and trusted Docker/cgroups monitoring boundary; still design worker result handoff/merge provenance, paused/crashed child recovery, and the precise action/observation protocol.
- 8.3: member private phases, self-declared final candidate readiness, transition/blocked/recovery behavior, incomplete outcomes without intellectual supervision.
- 8.4: integration of the agent loop with sealed review, checkpoint member `/work` and `/done`, final premortem and explicit termination/completion gates.
- 8.5: precise acceptance scenarios and interfaces for Step 9 providers, Step 10 tools and Step 11 context rollover.

**Step 8 remains IN DESIGN.** Decision 8.1 and the Step 8.2 worker-autonomy/resource-monitoring policy are approved and documented. Detailed result/recovery and remaining Step 8 phases are open; application code and runtime tests remain NOT STARTED / NOT RUN.
