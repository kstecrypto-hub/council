# Step 8 — Karpathy-first evidence-feedback loop (ADR-43)

**Owner direction approved October 19, 2026. Status: POLICY APPROVED / OPERATIONAL RECONCILIATION IN DESIGN. Council implementation NOT STARTED; runtime/model tests NOT RUN.**

This policy **supersedes only ADR-14's word "optional" for the core evidence-feedback cycle**. It does **not** supersede the user's approved Council architecture, the five independent member seats, their autonomy, sealed checkpoint communication, Step 7 resource limits, protected Step 8.5 integration and five-member re-review, or the original optionality of *specific executable experiments*. Read [Part 8](PART_8_AGENT_LOOP_EXPERIMENTATION_DELEGATION.md), [Step 8 exact action and finalization contracts](STEP_8_ACTION_AND_FINALIZATION_CONTRACT_V1.md), and the [Step 9 discussion draft](STEP_9_PROVIDER_ADAPTER_AND_SHARED_MCP_CONTRACT_V1.md) together.

## 1. Binding intellectual workflow

**Council reasoning agents run on the Karpathy-style evidence-feedback cycle PLUS the Council-specific governance and execution specifications.** The Karpathy loop is no longer an optional branch hidden under `ACT`: it is the **normal parent cycle for substantive investigation, development, analysis, and integration**.

```text
ONE ORIGINAL COUNCIL MEMBER (same logical agent across sessions)
  approved Project Contract, own evidence/workspace and semantic phase
     |
     v
  FORM HYPOTHESIS / CHOOSE APPROACH / STATE EXPECTED OBSERVATION
     |
     v
  ACT / INVESTIGATE / CONSTRUCT / DELEGATE within approved authority
     |
     v
  TEST / CHECK / CHALLENGE with domain-appropriate available evidence
     |
     v
  OBSERVE actual result or honestly record NOT_RUN / BLOCKED / UNKNOWN
     |
     v
  MEMBER'S OWN DISPOSITION: KEEP | REVISE | DISCARD | INCONCLUSIVE
     |
     v
  RECORD rationale, exact source/test/environment versions and provenance
     |
     +----> next hypothesis / revision / action as member chooses
     +----> ask the user where required; wait/block honestly
     +----> member-authored CHECKPOINT_READY or concluded investigation,
             subject to the existing trusted mechanical admission gates
```

The loop is **mandatory as the standard process for each materially advanced approach or conclusion**, not mandatory as a newly logged experiment after every model token, message, trivial filesystem operation, or context-summary step. A single cycle may span many existing `REASON`, `ACT`, `DELEGATE` and `RECORD_FINDING` commands. Where practical no execution/test is possible, the agent must **record the specific limitation**, attempt appropriate alternative corroboration or counterexample analysis when available, classify the observation accurately (`NOT_RUN`, `BLOCKED` or `INCONCLUSIVE`), and avoid claiming the result was verified.

The agent—not the Orchestrator, Auditor, Integrator-as-supervisor, gateway or a universal numeric evaluator—chooses hypotheses, alternatives, meaningful tests and dispositions. The existing customer-approved Contract defines requirements and evidence expectations. No fixed iteration count, mandatory experimental program, automatic scalar winner selection, forced time-box, or model-authored false PASS/READY is introduced.

## 2. Who uses this cycle?

- **Each of the five original members:** independently applies the feedback cycle to its substantive work and maintains its own authenticated immutable source/evidence lineage. Peers cannot commandeer or edit one another's cycle. All-five checkpoint and independent review rules are unchanged.
- **Member-created AI workers:** apply the same evidence discipline to the substantive task delegated by their parent. Return source, observations, tests/unknowns and disposition recommendations to the **same original parent**. Workers do not become Council seats, make authoritative parent dispositions, override the parent phase budget, declare checkpoint readiness or access another peer's private data.
- **One persistent non-voting Final Integrator:** uses feedback-driven iteration while composing the **Council-authorized** Blueprint into one output; it may not replace the five members' chosen intellectual direction with its own unchecked high-level preference. Record deviations, versioned artifacts and negative evidence before its authored `OUTPUT_READY_INTENT`; actual artifact/operations verification and five original-member sealed review remain distinct.
- **Project Orchestrator:** may use ordinary evidence/constraint-check feedback when drafting the user's semantic milestone/contract proposal. It remains a **planning/clarification role**, not another Council investigative member or quality judge of the five. Do not force it into the original members' experimental development or grant it a vote.
- **Trusted runtime, Step 9 gateway and Step 10 tool broker:** ordinary deterministic services that **do not run a Karpathy reasoning loop**. They authenticate, moderate/authorize required boundaries, reserve budgets, execute or route permitted requests, verify actual effects, record observations, and fence epochs. Step 9 routes model/tool protocol exchanges; it never chooses the intellectual next iteration.

## 3. What qualifies as verification?

Match the Project Contract and evidence profile, never force software-style code tests into all fields:

| Domain | Appropriate feedback examples |
| --- | --- |
| Software | execute relevant tests, inspect failures, compare changed behavior and regressions, retain actual build/test records |
| Scientific or investigative analysis | compare independent sources, challenge assumptions, reconstruct calculations, look for counterexamples and report unresolved provenance |
| Hardware/engineering | compute bounds, use appropriate simulations/measurements if available, verify interfaces/clearances and label unperformed physical tests |
| Business/strategy | compare scenarios and assumptions with available evidence; disclose uncertainty and alternative interpretations |
| Documents and non-code design | check contractual requirements, internal consistency, sources, factual claims and versioned artifacts; do not invent Git/test outputs |

A successful command only proves that command's observed effects. It does not prove the hypothesis, the protected user acceptance criterion or a final product is correct. `KEEP` is an agent-authored *working direction*, **not** a runtime-certified true hypothesis. Even `INCONCLUSIVE` or `DISCARD` is a legitimate recorded cycle outcome. Failed attempts inform future iteration, never a universal blacklist of approaches.

## 4. Fit with existing steps and minimum evidence

- **Step 8 loop owner:** member/worker/Integrator controls the intelligent hypothesis → action → evaluation → disposition → repeat cycle. Use existing Step 8 experiment/attempt and Step 6 evidence/provenance records. A trace/reference must exist for every **material approach presented as a concluded finding**, or an explicit reason that evaluation was impossible; minor actions need not generate new durable records. No additional experiment scheduler, supervisory agent, queue or dedicated experiment database.
- **Step 7:** existing whole-member scheduling, aggregate worker resource limits and five user-approved protected budgets still control which model/tool operations are possible. Budget exhaustion remains `INCOMPLETE`, not forced readiness.
- **Step 9:** **every model inference and brokered tool operation** from these reasoning loops uses the trusted gateway/broker and current authorizations, moderation where applicable, deterministic checks, provider-native tool continuation and cost reporting. A member's purely local permitted computation is not itself a new Step 9 model request; Step 10 still constrains it.
- **Step 10:** the existing approved sandbox/verifier permissions govern execution. A checkpoint `/work` verification loop is **read-only verification** against pinned snapshots; no repairs or source writes until normal checkpoint closure. The Integrator's iterative workspace is separately scoped and frozen before the original five review it.
- **Step 11:** on a context rollover or authorized Docker recreation, the **same logical agent** retrieves its exact versioned hypothesis, last observation, current disposition, remaining unknown provider/tool effects, unresolved objections and intended next work. A fresh model session is not a fresh Council seat, a forgotten failure, or automatic provider fallback.
- **Step 3–5 and final acceptance:** immutable feedback references may support provenance/ready claims, but the runtime verifies only *mechanical completeness and authentic observations*, not substantive soundness. Protected tests and the original five independent sealed reviews can contradict a member's own `KEEP`. Genuine negative/inconclusive final investigations may be concluded within the user's authorized scope; unsupported success cannot be substituted. The user alone accepts the exact final version.

## 5. Further design discussion, not yet agreed mechanics

The **policy** (Karpathy-first as default) is approved; the exact runtime prompt/action binding, minimal durable feedback-record schema linkage, how checkpoint readiness reports cycle coverage without an artificial experiment counter, worker-result merging under member autonomy, and how to present untestable domain claims must be reconciled with the existing Step 8 v1 command schema. Do not invent a sixth quality judge, a mandatory empirical test for every thought, or extra tables to solve these prematurely.

**No implementation or runtime validation has occurred.** Retain Step 8 overall **IN DESIGN for this approved amendment** until its operational semantics are reviewed. Existing Step 8.2–8.5 designs remain the baseline; this change does not reset their approvals or initiate Step 9/10/11 implementation.
