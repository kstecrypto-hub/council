# Step 8 — Agent action, checkpoint and integrated finalization contract v1

**Status: DESIGN-SPECIFIED (2026-10-19); NOT IMPLEMENTED; RUNTIME/SECURITY/MODEL TESTS NOT RUN.** This is the concrete member and final-stage state/authority protocol for the previously approved [agent loop](PART_8_AGENT_LOOP_EXPERIMENTATION_DELEGATION.md), [Step 8.3](STEP_8_3_MEMBER_PHASE_COMPLETION_AND_READINESS.md), [8.4](STEP_8_4_COLLECTIVE_SYNTHESIS_AND_FINAL_INTEGRATION.md), [8.5A](STEP_8_5_STRUCTURED_COUNCIL_BLUEPRINT_HANDOFF.md), [8.5B](STEP_8_5B_FINAL_INTEGRATOR_EXECUTION_AND_RECOVERY.md), [lean 8.5C+D](STEP_8_5C_8_5D_COMMAND_STATE_RECOVERY_AND_FINALIZATION.md) and exact [Step 3–5 command contract](STEPS_3_TO_5_EXACT_INTERFACE_CONTRACT_V1.md). Preserve exactly five original peers, one non-voting Integrator, one existing trusted runtime, and the approved user Contract. No separate intellectual supervisor, automatic winner vote, fixed worker count/depth, extra per-key API queue or new restart service.

## 1. Independent member action/observation protocol

Each original member owns its private investigation/candidate, may choose arbitrary internal workers under **its existing sandbox aggregate resources**, and decides which authorized ACT to attempt next. Step 7 alone admits whole member environments onto capacity slots (initial deterministic seat-order 1–5); it never dictates a solution. No mandatory reasoning-iteration count, compulsory experiment, timed private-work slice or generic completion deadline.

**ADR-45 nested execution design (October 20; policy approved, exact prompt binding IN DESIGN):** each original member controls an **outer strategic approach/hypothesis and success criteria** that contains an **inner task -> execute/investigate/delegate -> check -> repair/continue loop**. Inner operations are not required to produce a fresh strategic hypothesis or outer KEEP/REVISE/DISCARD verdict each time. Meaningful intermediate checks run during implementation; candidate-level evaluation occurs against the outer criteria before honest checkpoint readiness where applicable. Material foundational counterevidence may trigger an early outer revision. Reuse existing typed commands and Step 6/8 provenance, not a new workflow service. [ADR-45](STEP_8_ADR45_NESTED_STRATEGY_EXECUTION_LOOPS.md).

**Member action v1**, carried by the existing typed trusted bridge:
\`{action_id, parent_member_seat, phase_id, phase_generation, current_contract_revision, authorized_epoch, kind, proposal_ref?, tool_capability?, object_refs[], parent_operation_id?, expected_state_version, idempotency_key, expected_budget_scope, privacy_scope}\`.

Valid **action kinds**:
- \`REASON\`: local member-only deliberation; any persistable claim goes to attributed canonical evidence, not an automatically established fact.
- \`ACT\`: request one allowed tool/experiment/retrieval/local-command through the existing scoped broker and canonical effect ledger. The **trusted** controller checks user approval, tool/egress, current grants, budget and resource limits before dispatch.
- \`DELEGATE\`: create an authorized internal worker/task in the *same private member sandbox* with no additional Council seat/vote, no broader permission and charges to the same parent budget. A separate worker container would require an existing trusted broker and resource accounting; it is never automatic.
- \`REQUEST_USER_INPUT\`: issue the existing canonical clarification request; the Orchestrator processes the raw user answer into versioned authorized contract/branch-local instruction lineage. No raw user response bypasses the Orchestrator.
- \`RECORD_FINDING\`: append an attributed, versioned claim/assumption/experiment/result with exact evidence refs, confidence/limitations and source independence cautions. Recorded interpretation is not backend-verified truth.
- \`RECORD_EXPERIMENT\`: record an **outer strategic approach evaluation** or a useful scoped tactical experiment: hypothesis/criteria where applicable -> change/check -> observed evidence -> interpreted outcome. **Not mandatory for each inner execution action or mechanical fix.** Evidence/provenance includes exact input/environment, actual checks, limitations and applicable approach/version; no invented PASS.
- \`DECLARE_READINESS_INTENT\`: original member authors \`CHECKPOINT_READY\` or \`FINAL_INVESTIGATION_CONCLUDED\` intent; mechanics must be checked separately.
- \`REPORT_BLOCKER\`: genuine \`WAITING_USER\`, \`DEPENDENCY_BLOCKED\`, \`RESOURCE_BLOCKED\`, \`BUDGET_EXHAUSTED\`, \`FAILED\` or terminal honest \`CONCLUDED_NO_VIABLE_CANDIDATE\` **only when the approved outcome/phase actually permits**. No pretending exhaustion is intellectual completion.

**Trusted observation v1**:
\`{operation_id, attempt_id, logical_member_seat, session_epoch, action_id, observed_kind, real_status=NOT_RUN|BLOCKED|DISPATCHED|SUCCEEDED|FAILED|UNKNOWN_PENDING_RECONCILIATION, input_and_output_hashes, environment_and_tool_versions, actual_usage_or_reserved_unknown, artifact_refs, event_position, source_provenance, error_code?}\`.
The model may author an intent, recommendation or hypothesis; only the broker/controller records the observed outcome of provider, Git, container, verifier, grant or external effect. Preserve real failed/inconclusive experiments and latest applicable evidence for later work. Context rollover preserves exact logical agent identity and source/event/cost cursors; it does not start a sixth independent agent.

## 2. State axes and guarded member-phase transitions

Keep the **existing** run lifecycle, member execution status, checkpoint phase, communication member state, external operation, result verification, acceptance and archive progress as *separate axes*. Never flatten them to one ambiguous “DONE”.

| Scope | States and transitions / authoritative actor |
| --- | --- |
| Run lifecycle | \`PROVISIONING -> ACTIVE -> FINALIZING -> COMPLETED\`; \`ACTIVE -> QUIESCING_FOR_PAUSE activity -> PAUSED\` only after observed safe whole-agent quiescence; \`ACTIVE/PAUSED -> STOPPING -> CANCELLED\` only on verified safe cleanup, else honest FAILED/incomplete; current backend only |
| Ordinary member | \`PRIVATE_ACTIVE -> READY_INTENT -> FROZEN_VERIFICATION_PENDING -> CHECKPOINT_ARRIVED\`; mechanical failures return BLOCKED/FAILED/INCOMPLETE without counterfeit arrival; same **original** member authors intent, trusted runtime accepts verified arrival |
| Checkpoint | \`WAITING_FOR_FIVE -> OPENING -> SEALED_REVIEW -> REVIEWING -> CLOSING -> CLOSED\`; all five authentic arrivals, customer-local selected frozen manifests and **observed current recipient grants** required before sealed review |
| Peer communication | \`AVAILABLE <-> WORKING\` for bounded verification-only \`/work\` in disposable read-only verifier; \`AVAILABLE -> DONE\` only with processed sequence, obligation version, delivered outgoing frontier, no active /work; new accepted required action invalidates that member's DONE before closing |
| Results | \`INTENT_RECORDED -> PENDING_MECHANICAL_CHECK -> OBSERVED_VERIFIED | BLOCKED | FAILED | UNKNOWN\`; NOT_RUN and FAILED protected checks stay visible and never become PASS due to a model's self-report |
| End-of-phase capacity | Early READY/BLOCKED/EXHAUSTED member's container is safely quiesced and its whole-agent slot released; early READY cannot start the **next private phase** before actual all-five checkpoint closure. A new required peer action re-admits the same logical seat within Step 7's existing queue |

The five-member checkpoint barrier is **all five currently verified arrivals**, not all five model-authored claims. BUDGET_EXHAUSTED, MISSING, FAILED, a forced incomplete checkpoint, or missing reviewer cannot counterfeit arrival, review, /done, five-member consensus or final acceptance.

In SEALED_REVIEW, member assessments are immutable and concealed until **all five real same-generation reviewer seats** submit. No shared debate, pre-reveal search/graph snippet, cache or model context can expose sealed content. After atomic reveal, shared discussion uses original-member authenticated text and structured peer actions. \`/work\` remains separate from messaging and can **only verify pinned read-only inputs**; it cannot change any member's authoritative candidate or protected acceptance definitions. Normal close requires five valid **current** /done certificates and member-authored closeouts, no pending accepted outbound messages/required actions or active verifiers, fenced new communication/read admissions, then independently observed route/grant revocation. Forced/incomplete closeout is always *distinct* and cannot unlock an executable final Blueprint.

## 3. Five authentic final investigation outcomes and Decision Register

The approved **final comparison intake** is a special final investigation phase. Each original member submits one authentic concluded investigation record: \`VIABLE_CANDIDATE\` or \`CONCLUDED_NO_VIABLE_CANDIDATE\` with actual evidence, limitation and exact source/artifact manifest. A formally BLOCKED, BUDGET_EXHAUSTED or FAILED member does **not** become a completed final submission by default. A negative but genuinely concluded research investigation is allowed without fabricating code; an implementation-required earlier checkpoint still requires its real own phase outcome unless the user approves a contract revision.

At the final comparison checkpoint:
- The original five author per-material-choice \`RecordCouncilPosition\` actions with alternative/version IDs, initial sealed positions **only when actually authored**, post-discussion positions, changes with reasons, evidence/source overlap, minority counterexamples, unresolved objections and recommended direction.
- The trusted backend assembles a versioned \`Council Decision Register\` embedded in the Blueprint from those authentic actions; never invent support, agreement, votes or absent prior position. Each material decision has \`RECOMMENDED | CONTESTED | UNRESOLVED | REQUIRES_USER_DECISION\`, traceable citations and impact on permitted integration.
- The Council recommendation is the default; multiple independent supporting members are a **meaningful rebuttable qualitative signal**, never calibrated probability, automatic 3/5 or 4/5 truth rule. Hard constraints, demonstrable counterevidence and verified applicability have priority. One supported counterexample can defeat multiple unsupported endorsements.
- A genuine ambiguity within the already user-authorized design may receive an explicitly attributed **conditional, reversible** preferred direction with re-review tests; this is not fabricated consensus. A material unauthorized high-level scope, data access, IP, egress, budget or acceptance change becomes \`REQUIRES_USER_DECISION\`. No affected Integrator operation starts before proper existing user approval, otherwise honest incomplete/blocked output.
- The Integrator may choose ordinary *implementation/synthesis mechanics* within the exact Blueprint and record decisions; a material evidence-based deviation is an immutable \`IntegratorDeviation\` tied to Blueprint, evidence and new artifact version, disclosed to all five original reviewers. Its training preference never silently overrides the Council's higher-level direction.

## 4. Blueprint lifecycle and executable handoff

| Current state | Command / issuer | Required observed guard and next state |
| --- | --- | --- |
| \`DRAFT\` | \`RecordCouncilPosition\` / genuine member; deterministic trusted assembler | Current canonical original-five authored positions, exact approved Contract, content-hashed source manifests and checkpoint generation, versioned revision; remain DRAFT |
| \`DRAFT\` | \`FreezeIntegrationBlueprint\` / trusted backend | Five legitimate final investigation outcomes and actual final comparison sealed review+reveal/discussion evidence, source graph/decision register provenance, no invented positions, immutable Blueprint hash; -> FROZEN; *no execution authority yet* |
| \`FROZEN\` | \`VerifyBlueprintExecutableHandoff\` / trusted backend | All five original authenticated current-frontier /done/closeout, no outstanding required peer action, no active verification-only /work, normal CLOSED checkpoint, **observed** peer route/grant revocation; -> EXECUTABLE |
| \`FROZEN\` with incomplete/UNKNOWN revoke, stale frontier or forced close | any admission attempt | Deny/hold blocked; a new valid action may require re-freeze/versioning. Neither timeout nor “mostly done” grants authority |
| \`EXECUTABLE\` | \`AdmitFinalIntegrator\` / trusted backend, with existing user-approved spend/egress | Separate current Integrator workspace, source scopes and grants, current epoch, approved integration allowance *and* protected next-review allowance and resource capacity; -> INTEGRATOR_ACTIVE |
| \`EXECUTABLE\` with stale Contract/source authorization | admission/restart | Recheck new policy revision; safely block or obtain explicit user authorization; no silent extension |

Blueprint source sets and member-private unpublished work remain distinct. The Integrator cannot read old checkpoint peer grants; it receives **fresh separate customer-authorized immutable source grants** only after actual revocation of prior grants.

## 5. Integrator's durable execution and observed output

There is **one logical non-voting Integrator per run**, with stable customer-owned isolated workspace and serial authorized execution epochs. It can use permitted local worker processes under its own budget/resource allowance. It has **no original-member seat, reviewer role, peer write authority, automatic permission enlargement or new recovery daemon**.

Integrator protocol:
1. \`INTEGRATOR_PENDING_ADMISSION -> INTEGRATOR_ACTIVE\` only on current executable Blueprint, fresh observed source grants, user Contract, approved five protected spend scopes, host capacity and all deterministic/moderation egress conditions.
2. During ACT, durable original candidate refs, own work/provenance and relevant uncertainty are persisted. The Integrator can record bounded design choices/deviations with exact output versions, limitations and evidence. A crash is a **same-agent continuation** with fresh fenced epoch and broker checks, not a new “independent” reviewer.
3. \`SubmitIntegratorOutputReadyIntent\` identifies exact proposed \`SOFTWARE_GIT\` commit/tree or **\`NONCODE_MANIFEST\`** hash (research, hardware, documents etc), signed source-closure refs and limitations. This is only model-authored intent, **not** proof of output or test PASS.
4. Trusted \`VerifyIntegratedOutput\` observes actual immutable selected artifact hash and dependency closure, required format-specific reconstruction/source/citation checks, write fencing and whole-Integrator quiescence/resource release, and reconciles consequential pending UNKNOWN effects. If those conditions fail, report BLOCKED/UNKNOWN/FAILED and do not open review.
5. Record protected test outcomes separately as actual \`PASSED | FAILED | NOT_RUN | BLOCKED | STALE\`, pinned to exact output version/environment/harness. “Mechanically verified immutable output” **does not** imply its code is correct, its research is true or user approved.
6. Opening post-integration review issues **new** purpose-scoped read-only grants of **only that verified artifact version** to the five originals; Integrator has no seat or control over their sealed assessments.

On session rollover/host pressure/crash, safely stop whole-agent work, preserve only flushed files/Git/operation receipts on its persistent volume, fence stale epochs, reconcile model charges/provider/host operations and check permissions. Docker preserves persisted bytes and handles containment but **not** running worker processes, provider invoices or logical permission reconciliation. An intentionally paused/blocked/checkpoint-ready/exhausted agent cannot revive under unconditional Docker restart.

## 6. Exact post-integration reviews, material revisions, premortem and user gate

**First integrated output:** The original five seats submit one genuine authenticated, independent sealed **FULL** assessment each bound to \`(review_generation, verified_integrated_output_id, artifact_hash)\`. Under one Step 5 generation lock, the fifth committed distinct seat permits **one** atomic reveal, not a sixth Integrator vote or a silent majority pass. Five actual review submissions can report disagreement, defects or inconclusive evidence; “review complete” is **not** “verification PASS”.

**Revisions:** After normal post-integration review closure and independently **observed** revocation of read-only grants, the same logical Integrator may regain a separately authorized **writable** epoch for a new revision. Never mutate the frozen reviewed V1 in place. On V2:
- mechanically demonstrated **non-substantive equivalence** retains only evidence-proven applicable prior checks/reviews; no generic auto-waiver;
- genuinely **localized substantive** change requires five fresh independent sealed **DELTA** assessments against exact V2, using provenance dependency closure and impacted verification evidence;
- foundational/high-risk/ambiguous dependency change requires five fresh independent sealed **FULL** assessments. Missing/uncertain impact -> FULL.
Old V1 assessments/verification cannot be submitted as if authored on V2. Impact policy is governed by source dependency/evidence graph and actual reviewer-relevant semantic impact; an author's “cosmetic only” claim is not proof.

**Premortem:** A separate \`SEALED_PREMORTEM\` generation targets the exact *pair* \`(integrated_artifact_hash, frozen_provisional_report_hash)\`; all five original seats write genuine independent **hypothetical** six-month-plus failure scenarios, revealed atomically only after five. Neither scenarios nor pre-mortem model narratives are observations from the future. Material changes to either bound version invalidate the applicable premortem generation and require warranted five-person scoped/full re-review.

**Final package:** The trusted editorial/report stage freezes one immutable content-hashed result plus provisional report, actual verification statuses, source provenance, unresolved dissent, reviews, premortem, licensing/permissions and customer scope. It does not invent test PASS or erase reservations. The existing user interaction/command family accepts/revises/rejects **the exact integrated final package**; no automatic acceptance from vote, report model or Integrator completion. An original member-candidate ID cannot stand in for the integrated target. For unfulfilled mandatory acceptance requirements, record authentic failure/blocked/NOT_RUN and obtain explicit user-approved contract change/waiver where allowed; do not claim a successfully completed original contract.

**Delivered versus accepted:** Acceptance is one durable user event. Verified external customer-selected archive/export (source/artifacts, permitted evidence, reconstructable environment when applicable), fresh restore/reference closure, permission/grant cleanup, effect/budget reconciliation and durable teardown record are **later distinct observed events**. Mark \`COMPLETED\` only when all mandatory finalization guards pass. Preserve necessary recoverable state if archive validation fails; NEVER delete the control database as a response to a failed archive.

## 7. Atomicity, concurrent submissions, visibility and failure states

All consequential commands reuse [Step 3–5 reference transaction contract](STEPS_3_TO_5_EXACT_INTERFACE_CONTRACT_V1.md): trusted authenticated actor -> scoped identical-key replay before stale guard -> event-clock-first canonical lock ordering -> expected version -> committed command/idempotency/intent/budget/event/outbox -> external effect after commit -> observed reconciliation. No new API-specific queue; Step 7 whole-agent queue protects low-resource admission **only**.

- Two seats can submit at identical timestamps: database generation uniqueness + current version locks accept both valid distinct submitted rows; the event clock determines commit order, not submission time.
- A duplicate same-seat/key/payload returns its previous receipt; same key/different hash is rejected; a seat cannot forge another's submission. A sixth Integrator submission cannot fill missing seat 5.
- Checkpoint/final-review/premortem sealed text and evidence must be excluded from unauthorized model contexts, search indexes, graph projections and snapshots until correct current-generation atomic reveal.
- A required peer message accepted before close invalidates stale /done and may require a new Blueprint frontier; a message attempted *after* canonical closing fence is rejected/retried against the next legitimate phase, not silently backdated.
- A lost source grant, changed privacy policy, host crash, stale epoch, unknown external/provider write or uncertain spending blocks **only affected unsafe admissions**, preserving state and unspent unrelated eligible work. Protected review budget cannot be borrowed by Integrator.
- No manager or timeout can turn BUDGET_EXHAUSTED, NOT_RUN, MISSING_FIFTH, UNKNOWN_PENDING_RECONCILIATION, invalid artifact hash or forced-incomplete close into five real completion outcomes.

## 8. Exact v1 transition/termination invariants and external handoff

The trusted backend is authoritative **only for mechanical state**, not whether a member's scientific or design position is intellectually true. Models author positions, requests and completion intent. Human users approve material permissions, total scope, protected cost policy and final acceptance. Immutable project contract versions and user revisions remain the upper bound of delegated decision-making.

**Minimal final-stage chain** (all steps individually durable, distinct, version-checked):
\`FIVE_CONCLUDED_INVESTIGATIONS -> FIVE_ACTUAL_FINAL_COMPARISON_REVIEWS -> NORMAL_CLOSEOUT -> BLUEPRINT_FROZEN -> BLUEPRINT_EXECUTABLE_VERIFIED -> INTEGRATOR_ADMITTED -> OUTPUT_READY_INTENT -> OUTPUT_IMMUTABLE_VERIFIED -> FIVE_REAL_SEALED_INTEGRATED_REVIEWS -> REQUIRED_REVISION_LOOP_IF_ANY -> FIVE_REAL_SEALED_PREMORTEMS_ON_EXACT_REPORT_PAIR -> FINAL_PACKAGE_FROZEN -> USER_DECISION -> ARCHIVE_AND_RESTORE_VERIFIED -> CLEANUP_VERIFIED -> COMPLETED\`.

This order is a **partial order of required gates**, not an instruction to invent work or force all runs to succeed. Blueprint freeze may occur before verified closeout but cannot become executable without it. In an unresolved material conflict, no viable candidate, failed checks, withdrawn permission, missing review capacity or user rejection, preserve a truthful incomplete/revision/cancelled state and exact source records. The Orchestrator may re-plan semantic milestones only with existing required Project Contract/user approval; no hidden integrator executive vote.

**Implementation-time parameters left intentionally configurable**: provider/model-specific capabilities and prices, chosen customer sandbox backend/OS, source class/retention, token ceilings, exact context window, reviewer resource estimates, per-deployment streaming byte caps and policy. Those are configuration/adapter decisions, **not undecided Council governance**. Step 9/10/11 adapter implementation and runtime evaluation are separate later phases. The matching [deterministic/failure verification matrix](STEP_2_TO_8_VERIFICATION_MATRIX_V1.md) is a **test plan only**.

## ADR-43 amendment — binding feedback cycle (policy approved; command details in design)

Every material member/worker/Integrator approach uses hypothesis/alternative -> ACT/investigation -> domain-appropriate check/counterexample -> actual observation or truthful NOT_RUN -> KEEP/REVISE/DISCARD/INCONCLUSIVE -> durable evidence record, before presenting it as a substantively checked conclusion. Existing REASON/ACT/DELEGATE/RECORD_FINDING command mechanics remain; no new supervisory agent or per-action forced test. See [Karpathy-first amendment](STEP_8_KARPATHY_FIRST_AGENT_LOOP_AMENDMENT.md). **Step 8 reopened IN DESIGN for exact runtime binding, not IMPLEMENTED.**


## October 19 ADR-44 — approved feedback operating rules and checkpoint self-review

[Binding policy](STEP_8_ADR44_FEEDBACK_CYCLE_AND_CHECKPOINT_SELF_REVIEW.md): every substantive Council approach uses hypothesis/approach, action, appropriate check, real observation or honest limitation, member-authored KEEP/REVISE/DISCARD/INCONCLUSIVE, durable evidence and self-directed repetition. Existing Step 6/8 records suffice; no extra experiment scheduler, quality judge, test per trivial action, fixed iteration quota or invented PASS. **Before every normal intermediate or final checkpoint, the original parent member must author an immutable, exact-version self-review** covering current objective/approach, observed evidence, unsupported assumptions, defects, unperformed checks and why it considers the version ready for *peer review*. Reference the report in existing readiness intent and freeze it for authorized peer access. Backend verifies only original-member authorship, presence, correct run/phase/generation and target hash; it does **not** judge intellectual sufficiency. Blocked/exhausted/incomplete work cannot fake review/readiness. The nonvoting Integrator similarly provides a versioned self-check with output-ready intent; actual checks and five genuine independent peer reviews remain distinct. **Policy APPROVED; exact runtime binding IN DESIGN; implementation NOT STARTED; tests NOT RUN.**


## October 20 ADR-45 — nested strategy/execution loop, no per-step re-hypothesizing

[Owner-approved two-loop policy](STEP_8_ADR45_NESTED_STRATEGY_EXECUTION_LOOPS.md) supplements ADR-43/44. The original member makes the **outer strategic decision**; the inner loop fixes/test-checks ordinary implementation or investigation steps; strong counterevidence may interrupt inner work and promote reconsideration. Final candidate/outcome validation remains distinct from intermediate tests, the mandatory member-authored ADR-44 checkpoint self-review, sealed review by five authentic peers and user final acceptance. Existing action kinds, budget/resource controls, provenance, exact-version self-review and fail/unknown semantics remain authoritative. **Policy approved; command/prompt DTO reconciliation IN DESIGN; code NOT STARTED; tests NOT RUN.**
