# Part 8 - Agent loop, structured experimentation, and delegation

**Design status:** IN DESIGN. **Decision 8.1 (nested Karpathy-style experimentation): ACCEPTED, October 14, 2026.** Worker delegation policy, complete action protocol, final-phase/failure transitions, and full Step 8 design closure remain to be decided.

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

The **parent member** decides what to integrate, whether to repeat or challenge a test and when its own phase is ready. A worker cannot claim the parent's CHECKPOINT_READY, publish another peer's private work, alter protected acceptance definitions, or obtain additional permission/budget from its own initiative. Exact worker/delegation depth, lifecycle and result-merge protocol are still pending Step 8.2; this decision authorizes the concept but does not finalize those details.

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

- 8.2: full action/observation protocol, worker creation, delegation depth/caps, merge/result ownership, crash and worker lifecycle.
- 8.3: member private phases, self-declared final candidate readiness, transition/blocked/recovery behavior, incomplete outcomes without intellectual supervision.
- 8.4: integration of the agent loop with sealed review, checkpoint member `/work` and `/done`, final premortem and explicit termination/completion gates.
- 8.5: precise acceptance scenarios and interfaces for Step 9 providers, Step 10 tools and Step 11 context rollover.

**Step 8 remains IN DESIGN.** Decision 8.1 is approved and documented; application code and runtime tests remain NOT STARTED / NOT RUN.
