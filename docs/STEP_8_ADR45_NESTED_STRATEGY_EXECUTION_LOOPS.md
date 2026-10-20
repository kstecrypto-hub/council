# ADR-45 — Two nested reasoning loops per Council member (strategy and execution)

**Owner decision: APPROVED October 20, 2026.** This is a Step 8 **policy/design** refinement, not application implementation or proof of better performance. **Operational prompt/command binding remains IN DESIGN; implementation NOT STARTED; runtime, comparative and acceptance tests NOT RUN.**

## Decision and relationship to prior policies

Each of the five original Council members uses **two nested loops** during substantive work:

1. **Outer strategic evidence-feedback loop**: choose an approach/hypothesis against the user-approved Project Contract, identify relevant success criteria and potential falsifiers, have the approach pursued, validate the resulting candidate or domain-specific outcome, then author KEEP / REVISE / DISCARD / INCONCLUSIVE with evidence. Repeat the *outer* loop only when the member judges a meaningful strategic revision or new approach warranted.
2. **Inner execution-and-improvement loop**: while pursuing the selected strategy, autonomously select the next task, implement/investigate/delegate, check the actual intermediate result, fix or refine, record material evidence, and continue. **A fresh strategic hypothesis is NOT required on each action, ordinary bug fix, tool call, inner iteration or worker result.** Inner work can use small tactical hypotheses/experiments where useful, but not as a mandatory ceremony.

The outer loop **wraps** the inner loop; it is not merely a second independent loop or a replacement for Council's existing overall five-member phases and sealed checkpoint reviews.

```text
ORIGINAL MEMBER (one persistent logical actor)
  OUTER STRATEGY: approved objective -> proposed approach/hypothesis and success criteria
    |
    +-- INNER EXECUTION: choose task -> act/investigate/delegate -> check -> repair/refine
    |      ^                                              |
    |      +------------- repeat as member chooses --------+
    |        (no new strategic hypothesis per iteration)
    |
    +-- APPROACH VALIDATION: evaluate candidate/outcome against the original criteria
    +-- MEMBER DISPOSITION: KEEP | REVISE | DISCARD | INCONCLUSIVE + exact evidence
    +-- member chooses whether to continue inner work, revise strategy, or conclude phase
    |
    +-- member-authored exact-version self-review -> readiness intent
        -> trusted mechanical freeze/check -> existing five-peer checkpoint
```

**ADR-45 refines, but does not repeal, ADR-43's mandatory evidence-feedback discipline or ADR-44's final self-review.** It clarifies their *level of granularity*: the full hypothesis/strategic disposition belongs to a meaningful **outer approach**, not to every inner implementation action. Previous text portraying a full strategic HYPOTHESIS -> ACT -> TEST -> KEEP/DISCARD sequence as mandatory for every inner step is superseded. The accepted optionality of any *particular executable experiment* remains; task-appropriate evidence checking and truthful limitations remain compulsory for material claims.

## Evaluation and early escalation

- **Inner checks happen throughout execution.** A failed unit test, bad API callback, source mismatch or mechanical defect is normally handled within the inner loop. Do not wait until the final product to discover routine failures.
- **Outer validation occurs after a meaningful candidate/outcome exists**, against the original objective, constraints and domain-appropriate evidence. For an executable product, run applicable completion/integration/rebuild/protected acceptance checks when authorized and available. For research, engineering or non-code tasks, use appropriately sourced, reproducible or critically examined evidence. When tests are unavailable, report NOT_RUN / BLOCKED / INCONCLUSIVE; never manufacture PASS.
- **Permit immediate strategic escalation.** An inner observation may falsify a central premise, uncover a hard Contract mismatch or show that reasonable corrections cannot satisfy a crucial requirement. The parent member may suspend/exit the inner loop and revise/reconsider the outer approach **before** producing a finished product. No mandatory failure count, threshold score or algorithmic detector is imposed; the reasoning member evaluates the evidence. Ordinary implementation errors do not themselves invalidate the strategy.
- **Budget, permissions, blocked/unknown effects and finite available resources still govern both loops.** A depleted budget does not force a fabricated outer judgment or readiness claim.

## Ownership, provenance and boundaries

- **Five original members:** each independently owns its current outer approach, inner execution, material evidence and strategic disposition. No central Orchestrator, moderator, model gateway, scheduler or backend intellectual quality judge selects strategies or decides when reasoning has succeeded.
- **Workers:** perform authorized scoped portions of the parent's inner work and may evaluate delegated alternatives; they return observations, artefacts, caveats and recommendations to the **parent**. They may not replace the original parent's overarching approach, declare parent checkpoint readiness, acquire a Council seat or exceed inherited capabilities.
- **Final Integrator:** may follow nested execution/verification discipline while carrying out the approved Council Blueprint, but cannot independently reopen or silently replace Council's major recommended direction. Material deviations follow existing Step 8.4/8.5 review and user-authority rules. It remains non-voting.
- **Durability without new infrastructure:** reuse Step 6 claim/source/assumption/provenance and Step 8 attempt/experiment/member-workspace records with existing Step 4/5 typed actions and operation receipts. Where needed, link a material inner observation and disposition to the owning outer approach and exact candidate/source/environment version; avoid a new mandatory event for every trivial operation. Failed inner attempts and discarded outer approaches remain contextual evidence, not global blacklists.
- **Step 11 continuity:** same logical member retains its current outer approach, inner next task, evidence checked or unavailable, unresolved blockers, and any pending consequences across context rollover and authorized Docker recovery.
- **Checkpoint readiness:** once the original member chooses to submit the current phase, its mandatory ADR-44 self-review references the outer approach, material inner checks/fixes, candidate-level validation, unperformed checks, defects, limitations and readiness rationale for the **exact submitted version**. The backend checks structure, identity, references, scope and freeze—not substantive intelligence. Five authentic sealed peer reviews, read-only checkpoint /work, non-voting integration, later protected validation and explicit user acceptance remain separate.

No new Council seat, dedicated hypothesis judge, numeric optimizer, experimental scheduler, per-inner-step approval gate, queue, service, database, forced iteration count or generic time limit is authorized by this decision.

## Proposed Step 8 contract reconciliation (design work, not implemented)

Reuse existing `REASON`, `ACT`, `DELEGATE`, `RECORD_FINDING`, `RECORD_EXPERIMENT`, `REPORT_BLOCKER` and member-authored readiness commands. Document **outer approach identity/criteria** in existing versioned evidence; accumulate significant inner observations as attributed attempts and optional tactical experiments; link them in the existing ADR-44 immutable self-review. Do **not** invent a new tool/model protocol or require a hypothesis for every `ACT`. Exact prompt/DTO representation and invalidation-on-revision need implementation-stage reconciliation; no claim they are currently implemented.

## Future acceptance cases — all NOT RUN

| ID | Scenario | Required behavior |
| --- | --- | --- |
| N45-01 | Routine failed implementation check under viable strategy | Inner loop can repair and retry without compulsory new outer hypothesis |
| N45-02 | New evidence disproves central approach premise | Parent can escalate immediately to outer reconsideration before finishing product |
| N45-03 | Parent submits completed executable candidate | Actual applicable intermediate and candidate-level tests recorded independently; no fake PASS |
| N45-04 | Non-code work lacks executable test | Appropriate source/counterexample checks or honest NOT_RUN/INCONCLUSIVE with rationale |
| N45-05 | Worker suggests alternative strategy | Original parent decides; no worker-authored parent readiness or sixth vote |
| N45-06 | Context rollover/blocked budget/checkpoint | Exact approach/evidence resumes within authority; no forced strategic conclusion, false arrival, or fabricated self-review |
| N45-07 | Candidate revised after self-review | Old self-review cannot qualify changed artifact/phase generation; fresh exact-version review required |
| N45-08 | Compare with conventional single-loop baseline | Measure correctness, cost, time, strategic churn and regressions; nested design superiority is a hypothesis, not an observed result |

**Status boundary:** ADR-45 principle APPROVED and recorded. Step 8 operational integration remains **IN DESIGN**; Council runtime, tests and empirical superiority claims remain **NOT STARTED / NOT RUN**.
