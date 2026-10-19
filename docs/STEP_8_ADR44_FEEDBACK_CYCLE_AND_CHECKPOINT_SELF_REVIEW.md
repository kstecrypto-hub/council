# ADR-44 — Operating rules for Karpathy-first Council loops and checkpoint self-review

**Owner approval: October 19, 2026.** Approved policy refinement of [ADR-43](STEP_8_KARPATHY_FIRST_AGENT_LOOP_AMENDMENT.md). **Step 8: IN DESIGN** while remaining concrete prompt/command/runtime integration is worked through. Application implementation NOT STARTED. Runtime, provider, and model evaluations NOT RUN.

## 1. The four accepted operating rules

1. **Begin every substantive approach with a feedback cycle.** The original member, its authorized substantive worker, or the non-voting Final Integrator records an attributable goal/hypothesis, proposed approach or alternative, and **the evidence/check that would help support, weaken, or falsify it**. Ordinary mechanical actions and model tokens need not each generate a new experiment. One substantive cycle may span multiple existing ACT and tool operations.
2. **The reasoning agent controls iteration.** After observing real results or honestly recording that a check was not possible, it chooses **KEEP / REVISE / DISCARD / INCONCLUSIVE** with an attributed reason. It may start another cycle or choose to address another user-approved objective, within the existing Step 7 budgets/resource/permission gates. No forced experiment count, numerical score, special quality-judge agent, new scheduler, additional supervisory Council seat, or automatic winner selection.
3. **Persist the evidence across cycles.** Reuse the existing Step 6 source/claim/assumption/provenance graph and Step 8 experiment, attempt and member-owned workspace records, tied to the actual source/code/artifact version and tool or model operation. KEEP is only an agent recommendation, not an observed test PASS. Retain unsuccessful/INCONCLUSIVE attempts with their applicability conditions, limitations, and checked versions; never universally blacklist an approach merely because it once failed.
4. **Readiness remains authored by the original member.** The five original Council seats each decide when their *user-approved semantic phase* has been substantively addressed. Their workers may return bounded evidence and recommendations but never declare parent readiness. The trusted backend checks authentication, exact submission/version and evidence existence, pinning, current grants, quiescence and resource release, **not whether the intellectual outcome is correct**. Other four original peers still perform their genuine independent sealed assessment at the checkpoint.

## 2. Mandatory final self-review before EVERY checkpoint

**Accepted owner decision:** Before *each* normal intermediate or final checkpoint readiness declaration, the original parent member performs **one final current-phase self-review** as the closing reflection of its existing Karpathy-style feedback loop. This is **not** a sixth member, second inference service, new quality supervisor, separate peer-review round or mandatory extra experimental test.

The parent self-review must say, in a concise member-authored versioned report:
- **Approach and objective:** which current user-approved phase objective, current candidate/result revision and main conclusions it is presenting.
- **Evidence actually checked:** references to substantive feedback cycles, observed tests/source checks, supporting and contradictory evidence with their exact version/status; any result still FAILED, BLOCKED, NOT_RUN or inconclusive is labeled as such.
- **Weaknesses and assumptions:** unresolved important assumptions, known counterexamples, defects/regressions, failed approaches and limitations relevant to the checkpoint.
- **Next meaningful validation:** remaining important checks that cannot be performed yet, why, and what peer review should challenge next.
- **Authored readiness rationale:** why the member considers this particular version ready **for review**, not a promise that it is a verified final solution.

The self-review can be short for a genuinely small phase and may honestly state no meaningful empirical test was available. It must not invent evidence, run arbitrary tests for compliance, or turn absent checks into PASS.

### Minimal contract binding, reusing current records

- Persist the self-review as one immutable member-authored **phase closeout/evidence artifact**, referenced by an added `self_review_ref` and `self_review_content_hash` in the **existing** `RecordMemberCheckpointReady` / `MarkCandidateReadyForReview` readiness intent payload as applicable, together with `run_id`, original seat, approved Contract revision, current phase/checkpoint generation, candidate/result manifest hash, authoring epoch and existing idempotency key. It may reference existing feedback/experiment record IDs; **no new service, table or external reviewer**.
- The report must be **authored after the substantive work it summarizes**, before the authored readiness intent, and bind the **same exact candidate/result manifest revision** submitted for checkpoint freeze. A changed candidate/phase/Contract/generation requires re-reviewing the changed conclusions and submitting a fresh correctly bound report; an old self-review cannot satisfy a new snapshot by automatic carry-over.
- The trusted controller verifies only the **presence, authenticated original-parent authorship, referential integrity, current run/phase/manifest binding and immutable readability** of this self-review before accepting the corresponding normal readiness intent/verified arrival. It cannot judge the quality, number of experiments, correctness, subjective confidence, or whether the member should have continued trying.
- Include the self-review in the customer-approved **frozen selected checkpoint evidence manifest** so peers can use it when permitted by the existing source-sharing policy; do not bypass grant/privacy/independent sealed-review rules. The peer assessment is still separately sealed until five genuine submissions.
- If no self-review exists, or its hash, author, target or generation mismatches, reject/hold **normal checkpoint readiness** with a specific mechanical missing/stale reference error; the member remains independently free to revise or to report honest incomplete/blocked status.
- A `BLOCKED`, `WAITING_USER`, `BUDGET_EXHAUSTED` or infrastructure failure **does not require fabricating a final self-review and cannot count as checkpoint arrival**. A genuine user-authorized `CONCLUDED_NO_VIABLE_CANDIDATE` final investigation submitted to the normal five-member final comparison should include the same honest self-review of failed/inconclusive evidence, without being mislabeled a viable implementation.

**Integrator analogy:** The single non-voting Final Integrator should attach its own bounded version-matched critical self-check/limitations record to `SubmitIntegratorOutputReadyIntent` before the actual integrated output can be considered for **mechanical verification**. This is **not** an extra Council vote or a substitute for the five original members' sealed integrated-output review, nor a claim of protected test PASS. The precise command-field placement remains part of Step 8.5 interface reconciliation.

## 3. Runtime ownership is unchanged

Step 8 owns the *intellectual cycle* and parent self-review. Step 9 routes inference and provider tool-call continuations, with existing deterministic authorization and applicable hosted moderation; it does not direct agent reasoning. Step 10 owns trusted tools, brokered effects, container limits and customer-local read-only verifier sandboxes. Step 11 owns bounded session continuity for the **same** logical agent and includes the latest hypotheses, failures, original citations, dispositions and self-review references. Step 7 retains finite **user-approved budgets** with no mandatory reasoning deadline; exhaustion does not force self-review, success or checkpoint-ready.

Checkpoint `/work` remains **verification-only** and never edits frozen candidate source. Each real peer independently assesses the original candidate and this self-review; another member's TEST_REQUEST is advisory, not a command to mutate the member's branch. The final Integration Blueprint, non-voting Integrator, exact-version five-member re-review, sealed premortem and explicit user acceptance remain governed by existing Steps 8.4–8.5.

## 4. Acceptance tests to implement LATER — all NOT RUN

| ID | Future scenario | Required outcome |
| --- | --- | 
| K44-01 | Normal checkpoint readiness without a self-review | Reject/hold the readiness intent; no false all-five arrival |
| K44-02 | Original member submits concise report with honest NOT_RUN/limitations | Accept structurally when hashes/actor/phase bind; no quality-judge refusal or invented PASS |
| K44-03 | Worker submits report or readiness intent on behalf of parent | Does not meet original-member authorship/readiness gate |
| K44-04 | Candidate hash or generation changes after self-review | Old reference stale; fresh member-authored report required for revised target |
| K44-05 | Member had no executable tests for source-based investigation | Domain-appropriate check and honest limitation permitted; no dummy execution/test quota |
| K44-06 | Member is budget-exhausted/blocked | Persist incomplete status; no fake self-review or checkpoint arrival |
| K44-07 | Report included in peer frozen manifest | Only granted readers see report; original five sealed reviews remain hidden until five real submissions |
| K44-08 | Integrator authors self-check on V1 but output V2 actually verified | Old self-check cannot stand in for V2; real checks and five-member review still required |
| K44-09 | Member records failure, revises, then resumes after context rollover | Same member identity retains failed attempt, revisions, relevant evidence, and next intent |
| K44-10 | Model declines further iteration after honest INCONCLUSIVE | Preserve true status and limitations; no forced confidence score, extra arbitrary cycle or fabricated readiness |

**Verification status:** These are examples of required *future runtime/integration tests*, not executed test results. Recording ADR-44 approves the policy, not its implementation, and does **not** mark Step 8 design/runtime/testing complete. The exact DTO mutation/invalidation ordering and concise UI/prompt representation can be completed in the following operational design discussion without redefining the five-member Council or adding new components.
