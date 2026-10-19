# Step 8.3 — Member phase completion, final-candidate readiness and incomplete outcomes

**Owner approval:** October 15, 2026. **Design status:** STEP 8.3 POLICY APPROVED; detailed Step 4/5 command DTO and Step 8.4 final-review integration remain IN DESIGN. **Application implementation:** NOT STARTED. **Runtime/evaluation tests:** NOT RUN. No implementation or testing is requested.

**Authority:** [Part 8](PART_8_AGENT_LOOP_EXPERIMENTATION_DELEGATION.md), [Step 7](PART_7_MEMBER_SCHEDULING_RECOVERY_RESOURCES.md), [Part 4 commands](TYPED_INTERACTION_CONTRACTS.md), [Part 5 operations](PART_5_TRANSACTIONS_IDEMPOTENCY_CONFLICTS.md), [Part 4A authority](PART_4A_AUTHORITY_BOUNDARIES.md). This design closes only the three Step 8.3 policy choices approved by the owner; it must not reopen approved 8.1/8.2/8.2a, the local-Git checkpoint bridge, or the five-member barrier.

## 1. Scope and invariant

**Every member is the sole intellectual authority for its own work and readiness.** The trusted runtime enforces only structural authorization, current contract/phase/epoch, durability, version validity, safe storage/operation boundaries and resource release. It does not invent progress, decide whether a proposed solution is intelligent, grade candidate quality, appoint a sixth judge or make one member's conclusion authoritative for all peers.

The Orchestrator prepares **user-approved outcome-based semantic checkpoints**, not fixed-time milestones or mandated solution components. Members independently choose when to declare readiness; Step 7 schedules whole-member slots, without time-slicing intellectual completion. For a software project, reference a committed local Git tree and typed evidence/artifact manifest. For a research or other non-code phase, reference the applicable versioned evidence/result package instead of inventing a Git implementation requirement.

This step is the boundary between a member's private development/analysis loop and the existing five-member checkpoint/final candidate process. It is not the checkpoint communication /done protocol and not final user acceptance.

## 2. Distinct member-authored and runtime-owned outcomes

| Outcome | Authority | Meaning / advancement |
| --- | --- | --- |
| CONTINUE / ACT / DELEGATE | Member | Independently chooses further authorized private work or workers; no readiness event. |
| CHECKPOINT_READY intent | Member | Affirms the *current approved semantic phase* is ready for peer evaluation; it is **not** a verified frozen arrival until mechanical readiness completion. |
| FINAL_CANDIDATE_READY intent | Member | Declares its own final candidate suitable for the later final Council review; **not** user acceptance, verified completion or /done. |
| CONCLUDED_NO_VIABLE_CANDIDATE | Member | Completed its investigation but cannot provide a viable candidate under identified constraints; preserves findings/limitations, **never silently counts as a viable implementation or normal five-arrival checkpoint readiness**. Step 8.4 must define final-review intake of this distinct outcome without changing the five fixed members. |
| BLOCKED / CONSTRAINT_CONFLICT | Member or observed runtime condition | Work cannot proceed with current constraints/dependencies; evidence and needed change are recorded. A member's impossibility claim is scoped to its investigation and is not a proof that the project is impossible. |
| WAITING_DEPENDENCY | Member/runtime | Durable, named dependency/trigger; release the execution slot at a safe boundary; do not count it as ready. |
| BUDGET_EXHAUSTED_INCOMPLETE | Trusted runtime, per Step 7 | Hard approved spend/token allowance reached: preserve progress/UNKNOWN liabilities and wait for explicit user allowance change or stop; **never creates readiness**. |
| RECOVERING / SUSPENDED / PAUSED / CANCELLED | Trusted runtime or user authority | Operational lifecycle, not an intellectual result; verified persistence/epoch fencing/cleanup rules apply. |

**Milestone-context distinction:** A feasibility-only phase may legitimately complete with a well-supported negative or inconclusive answer if that is the approved deliverable. The same finding must not be relabeled as a delivered working implementation when the approved milestone requires one. The member describes the substantive outcome; the runtime validates that the declared outcome type and required reference *shape* match the approved phase contract, not the truth of the conclusion.

## 3. Approved two-stage readiness boundary

**Stage A — member's authored declaration:** Through the already-designed trusted typed command gateway, the parent logical Council member submits a current run/member/phase/checkpoint-generation declaration, candidate revision or evidence-result package reference, evidence/experiment/claim references, concise outcome summary, explicit limitations, and unresolved relevant operations. The bridge supplies authenticated caller/epoch; agent-supplied identity is not trusted. Workers cannot independently declare their parent's readiness. A canonical versioned **readiness intent** is recorded durably and idempotently, separate from the eventual mechanically verified arrival.

**Stage B — trusted mechanically verified transition:** After the intent is recorded, the trusted runtime:
1. Stops admitting new ordinary private-development operations for this member/phase; fences the old write authority while retaining reconciliation/cleanup authority.
2. Requests **whole-member** safe quiescence, including member-managed ordinary workers, without adding a Council per-worker manager.
3. Preserves durable member-owned volume data/continuation references; outstanding consequential operations are reconciled, safely fenced or kept explicitly UNKNOWN under their existing Part 5 dependency policy.
4. Verifies exact submitted candidate Git commit/tree (or approved non-code result manifest), required authorized evidence references, current contract/phase/generation and selected immutable export scope. A dirty worktree is not implicitly included in the pinned commit; missing essential uncommitted files/dependencies keep the transition incomplete rather than silently broadening publication.
5. Confirms no active sandbox authority can modify the **pinned** checkpoint candidate, stops the whole-member container at a safe boundary, and **observes** slot/resource release through Step 7/10.
6. Atomically records the successful mechanically verified phase arrival, pinned candidate identity and applicable canonical event. Only that verified arrival counts toward the all-five checkpoint barrier.

The exact internal order of Git observation, quiescence and event writes must be finalized in Step 4/5 DTO design. The invariant is stronger than either ordering: **neither a model declaration nor a stop request alone proves a frozen safe checkpoint arrival**. SQL stores intent and observations, not imaginary atomic Git/Docker effects. Do not silently replace the author's conclusion with a runtime quality judgment.

### Illustrative existing command reuse (not a new global service)

- Existing member command **RecordMemberCheckpointReady** carries the authored readiness intent and the expected candidate/evidence identity; the command receipt is idempotent.
- Existing **MarkCandidateReadyForReview** handles the author's final-candidate readiness, with mechanically verified pin before admitting final review.
- Existing escalation/dependency commands represent a blocked or infeasible investigation with explicit scope; if a precise no-viable-candidate event/payload addition is required, it belongs in the existing Step 4 command and canonical event registry, **not** an independent completion subsystem.
- Existing **RecordMemberPhaseBudgetExhaustion** remains exclusively runtime-authored. A new user-approved allowance updates budget policy; it does not retroactively make a member ready.

**Canonical minimum result record:** member + current phase/contract revision; member-authored outcome code; exact candidate/source/evidence refs and versions; outcome summary; limitations; unresolved operations/dependencies; authoring session/epoch and idempotency; separate intent/verification/blocked observations; timestamps/event positions. Avoid duplicating source files or unbounded model reasoning inside the manifest. Graph/provenance records retain the attributable experiment and decision lineage.

## 4. Failure and recovery

- **Readiness intent then crash before verified freeze:** retain the authored intent and unfinished operation. On restart, reconcile trusted Git/storage/volume identity and pending side effects; complete the mechanical transition if the *same exact* authorized revision can still be proven, otherwise keep READY_INTENT_PENDING/BLOCKED and resume or request action as applicable. Do not generate a second intellectual declaration or falsely claim READY.
- **Snapshot/export cannot validate:** retain the member's decision, identify missing/unsafe paths, dependencies, evidence or scope; no successful arrival until the approved material is fixed/reconciled. A valid Git commit alone does not guarantee a reconstructible candidate.
- **Worker or external operation still active/UNKNOWN:** fence future writes/new dispatch; confirm candidate immutability and use Part 5 operation-specific dependency guards. Do not treat unresolved consequential writes or costs as failed, cancelled, free or completed.
- **Member gets ahead of peers:** freeze only its exact pinned work, safely release its host slot, and wait. It cannot start the next private revision until all five valid arrivals, authorized review, closure and verified snapshot-access revocation are complete.
- **Dependency/user question:** use existing RequestUserInput/Orchestrator faithful clarification and Step 7 waiting/admission policy. Unaffected authorized work may proceed; no user answer sent raw to members.
- **Impossible/negative finding:** preserve context, evidence and claim provenance; do not turn a member's scoped impossibility conclusion into project-global impossibility.
- **Budget exhaustion/host failure:** preserve member work in its stable private volume, fence epochs, record actual resource release and outstanding UNKNOWN effects. The runtime never declares readiness to use the next seat or close a barrier.

## 5. Avoiding unproductive loops without intellectual supervision

**Approved:** use existing typed-operation idempotency, denied-command handling, bounded infrastructure retries, per-call safety timeouts, spending/resource ceilings and optional observable repetition warnings. Replaying a forbidden or already-consumed operation cannot grant new authority. Do **not** introduce a sixth model as a "productivity judge", forced experiment count, fixed number of attempts, global reasoning deadline, mandatory private work slices or automatic CHECKPOINT_READY after exhaustion. A member may independently reconsider a previously failed approach when conditions differ (ADR-18).

An apparent loop can trigger an accurate UI warning or block a repeated unsafe side effect under existing policy; it is **not** proof that reasoning is unproductive or that the current phase intellectually concluded.

## 6. Final readiness and the Step 8.4 handoff

A regular **CHECKPOINT_READY** is a member-authored declaration for a user-approved intermediate semantic milestone. **FINAL_CANDIDATE_READY** is a member-authored declaration that its versioned final deliverable is suitable for the later final Council review; it is **not** checkpoint discussion /done, automatic success, collective consensus, user acceptance, verified archival or teardown.

The member's final result manifest identifies deliverable revision, applicable method/evidence/verification references, limitations, known outstanding risks and unresolved operations. The trusted backend pins/isolates the exact submitted result and records an observed versioned final-readiness outcome using the same safe intent/observation distinction as ordinary checkpoint readiness.

A member may also declare **CONCLUDED_NO_VIABLE_CANDIDATE**, with actual investigation/evidence and failure conditions rather than a manufactured working solution. The logical seat and its review identity still exist. **Step 8.4 must explicitly decide how the final five-member review ingests member-authored negative/inconclusive terminal investigations without bypassing the all-five independent-review requirement or falsely certifying a successful implementation.** Until then, this outcome does not automatically satisfy the normal deliverable-ready barrier.

**Step 8.4 remains open:** final review/coverage, sealed review/checkpoint integration, mandatory six-month-plus premortem, report editorial versus adjudicative authority, real user choice and termination/archival conditions. Do not mark Step 8 fully DESIGNED or implement the finalization engine from this Step 8.3 approval.

## October 16 approved Step 8.4 handoff clarification — domain-general synthesis

The owner clarified that **Step 8.4 culminates in ONE final integrated result**, not a user default choice between five independent candidates. Five authentic concluded investigations—including a truthful scoped `CONCLUDED_NO_VIABLE_CANDIDATE` that did not yield viable code—feed the **final comparison/synthesis checkpoint** when mechanically verified; an incomplete BLOCKED/BUDGET_EXHAUSTED member does not. The original five independently review each other's findings and construct a source/evidence-backed blueprint. A separate **non-voting Integration/Synthesis Agent** executes that plan in a separately authorized workspace; the same five original members then perform a **fresh sealed review of the actual integrated output**, before the existing premortem, report and explicit user acceptance. Applies to research, science, hardware, business analysis, documents and software; non-code outputs use evidence/artifact snapshots rather than fake required Git builds. No change to ordinary earlier all-five semantic implementation checkpoints or the approved Step 8.3 readiness intent/freeze separation. See [Step 8.4](STEP_8_4_COLLECTIVE_SYNTHESIS_AND_FINAL_INTEGRATION.md).

This is **approved Step 8.4 design direction**; exact DTO/integration contracts and completion tests remain IN DESIGN / NOT RUN.

## 7. Storage, integration and precise status

Implement with **existing components** when build is later authorized: parent member + command gateway (authorial declarations), Part 3 PostgreSQL phase/arrival/candidate/evidence records, Part 5 durable operations and idempotency/event clock, trusted customer-local Git/snapshot service, existing Step 7 whole-member lifecycle controller/scheduler, Step 10 sandbox checker, and Step 11 bounded continuation. No separate phase completion daemon, no per-worker recovery manager, no new model assessor and no new storage database.

**Approved policy choices:** (1) separate authored readiness intent from verified quiescence/freeze/arrival; (2) allow an explicit scoped concluded-without-viable-candidate result without treating it as completed implementation; (3) repetition checks stay at existing operation/safety controls and remain non-intellectual.

**Still DESIGN OPEN:** exact Step 4 input/output events/versions and Step 5 transaction/UNKNOWN boundary; how Stage B handles edge-case workspace and in-flight files under Step 10; full Step 8.4 final review/termination intake. **Application implementation and runtime/evaluation tests: NOT STARTED / NOT RUN.**


## October 19 — exact v1 design specification boundary

The earlier interface-design questions are specified in [Step 2 snapshot/transfer](STEP_2_SNAPSHOT_TRANSFER_CONTRACT_V1.md), [Steps 3–5 relational/typed/transaction contract](STEPS_3_TO_5_EXACT_INTERFACE_CONTRACT_V1.md), [Step 8 action/finalization contract](STEP_8_ACTION_AND_FINALIZATION_CONTRACT_V1.md), and [unexecuted verification matrix](STEP_2_TO_8_VERIFICATION_MATRIX_V1.md). Conflicting earlier claims that these **v1 interface choices** remain undecided are superseded, while original owner policies and archival decision history remain unchanged. Steps 2–5 and 8 are **DESIGNED** as specifications, not implemented. Physical migrations, code, real broker/provider integrations, actual concurrency/runtime/security/model tests **NOT STARTED / NOT RUN**. Implementation-time customer configuration and Step 9–11 adapter choices remain open. ADR-40 additional API submission queues remain superseded.


## October 19 ADR-44 — approved feedback operating rules and checkpoint self-review

[Binding policy](STEP_8_ADR44_FEEDBACK_CYCLE_AND_CHECKPOINT_SELF_REVIEW.md): every substantive Council approach uses hypothesis/approach, action, appropriate check, real observation or honest limitation, member-authored KEEP/REVISE/DISCARD/INCONCLUSIVE, durable evidence and self-directed repetition. Existing Step 6/8 records suffice; no extra experiment scheduler, quality judge, test per trivial action, fixed iteration quota or invented PASS. **Before every normal intermediate or final checkpoint, the original parent member must author an immutable, exact-version self-review** covering current objective/approach, observed evidence, unsupported assumptions, defects, unperformed checks and why it considers the version ready for *peer review*. Reference the report in existing readiness intent and freeze it for authorized peer access. Backend verifies only original-member authorship, presence, correct run/phase/generation and target hash; it does **not** judge intellectual sufficiency. Blocked/exhausted/incomplete work cannot fake review/readiness. The nonvoting Integrator similarly provides a versioned self-check with output-ready intent; actual checks and five genuine independent peer reviews remain distinct. **Policy APPROVED; exact runtime binding IN DESIGN; implementation NOT STARTED; tests NOT RUN.**
