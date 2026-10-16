# Step 8.5A — Structured Council conclusions and verified Blueprint handoff

**Owner approval:** October 16, 2026. **Design status:** TWO HANDOFF RULES APPROVED; the rest of Step 8.5 and exact Step 3/4/5 DTO, relational constraint and external-operation design remain **IN DESIGN**. **Application implementation:** NOT STARTED. **Runtime/security/comparative tests:** NOT RUN.

This document records the two owner-approved follow-up rules for [Step 8.4 collective synthesis](STEP_8_4_COLLECTIVE_SYNTHESIS_AND_FINAL_INTEGRATION.md) and the refined **ADR-26 Council-first integrator authority**. It is not permission to re-decide the five-member Council, selection weighting, final integration roles, budgets, review gates, evidence graph or privacy policy.

## Owner-approved rules

**ADR-30 — Council-authored structured decisions, not retroactive AI-inferred consensus.** During the existing final comparison checkpoint, the *five actual member identities* record their important recommendations, supporting and contradictory evidence, revisions of position, unresolved objections and conditional requirements as **authenticated structured Council actions**. The trusted backend assembles/validates the Blueprint/Decision Register **from genuine records**, not from an LLM later guessing what a conversation meant. Council has primary intellectual authority for the *recommended direction*; the Final Integrator follows it by default and may only make previously approved bounded, attributable decisions. No new sixth voting member, intellectual supervisor, voting quota or requirement of unanimous consensus.

**ADR-31 — Frozen, verified handoff only after genuine five-member closure.** A Blueprint is an executable Integration Agent handoff **only** when the exact source/decision/contract version is durably frozen, all five required final-comparison member communication/response obligations are legitimately satisfied, and the trusted checkpoint closes under existing verified local snapshot-access/grant revocation, active verification closure, epoch and resource safeguards. **An LLM declaration, a draft hash or /done alone is not final verified handoff.** `DISPUTED` or genuinely `DEFERRED` with a documented permissible disposition may close an obligation while preserving substantive uncertainty; a missing review, missing authentic /done, ceiling-forced incomplete closeout, unresolved required procedural obligation, unauthorised source, or unverifiable revocation does **not** make the Blueprint executable. Materially unresolved contract choices remain blocked for the appropriate user decision; the blueprint can represent permissible open technical alternatives without falsifying consensus.

## 1. Structured Council decision record (within the existing Blueprint)

A material decision entry is a **projection of member-authored, version-bound, full-detail source actions** rather than a new Council judge. Minimum fields:

| Field | Meaning |
| --- | --- |
| `decision_id`, `issue_scope`, `checkpoint_generation` | Stable issue and exact final comparison checkpoint/version |
| `alternative_refs`, `contribution_refs` | Permitted candidate/source/analysis alternatives with hashes/versions |
| `pre_discussion_member_positions` | Authentic positions actually submitted during the sealed independent review, **if present**; no invented initial stance |
| `post_discussion_member_positions` | Authenticated final positions, supported reasons, known limitations, and **explicit NO_POSITION/UNRESOLVED** where a member authors them; silence is not agreement |
| `position_change_refs` | Genuine authored revisions and attributable reasoning/evidence changes, not a retrospective model narrative |
| `support_and_counterevidence_refs` | Versioned actual tests, sources, experiment/assumption/claim references and source-dependence warnings |
| `recommendation`, `recommendation_status` | The **Council-authored** preference/conditional choice; `RECOMMENDED`, `CONTESTED`, `UNRESOLVED` or `REQUIRES_USER_DECISION`, with traceable authorship and scope |
| `minority_objection_refs`, `open_checks` | Reproducible contradicting evidence, material disagreements, dependencies and authorized next validation |
| `applicability`, `approved_priorities` | Conditions, compatibility restrictions, Project Contract version and required user permissions |
| `source_action_ids`, `content_hash` | Audit back to the exact immutable full message/typed action records and canonical version |

No mandatory five individual votes are created for each technical choice. Each member has the existing checkpoint opportunities and obligations to propose, challenge, correct misattributed positions and record final closeout. An unanswered obligation stays pending until legitimately disposed; no member who says nothing is classified as agreeing. A 4/5 preference is a **rebuttable qualitative signal**, especially where independent initial positions converge, not four proofs or an automatic algorithmic winner. One strong reproducible dissent can outweigh that preference. Evidence, actual requirements and compatibility always matter first.

**Authorship:** each view, objection, recommendation or changed position is created under the authenticated original Council member/epoch, via the existing typed gateway and event clock. Workers cannot impersonate the logical member; the Orchestrator, Auditor, backend and Final Integrator cannot author a member position or present editorial synthesis as a Council verdict. The same already-designed commands/actions may be extended with precise payloads; examples are design labels only and **do not imply implemented APIs**.

**Assembly:** existing trusted control-plane code may deterministically gather validated action IDs, full original conversation references, versioned evidence and permissions into a draft Blueprint. A writing/model tool may improve prose **editorially** but cannot invent recommendations, change vote counts, drop counterevidence, promote uncertain findings, or fill missing positions. All decision and discussion source refs remain independently inspectable. Members may challenge omissions or inaccuracies through their existing structured actions before closure, which updates relevant obligations/frontiers.

**Cross-domain:** for code, references may bind exact local Git tree/commit and verified tests; for research, source studies/data/analyses/claims; for engineering, measurements/design/evidence manifests; for strategy, original assumptions/metrics/documents. Software-specific objects must not be fabricated for non-code work. Customer source, snapshot permission and egress policy remain unchanged.

## 2. Exact distinction: draft, immutable freeze and executable handoff

Three different durable facts must not be collapsed into one boolean:

1. **Blueprint draft / source projection:** assembled from authorized member actions under an **open final-comparison checkpoint**. May change as legitimate discussions, objections and member-authored dispositions develop. The draft has a version and pending requirements; it is **not executable** by the integrator.
2. **Blueprint frozen:** the trusted control-plane, with the checkpoint/generation, event clock, current obligation frontier and version guards, validates the draft's **mechanical integrity**: original member authorship, five required sealed comparison reviews/reveal, permitted source/evidence identities, canonical Project Contract revision, exact member-authored recommendations/alternatives, preserved objections, complete source/action reference closure and no unauthorized additions. It then records an **immutable exact snapshot/hash and freeze intent/result**. It does **not** judge whether a Council technical conclusion is wise or magically prove that all necessary ideas were discovered.
3. **Blueprint executable:** only after **normal genuinely complete five-member checkpoint closure**, all current valid communication /done frontiers and required closeouts/obligation dispositions, stopped verification excursions, and independently **observed** local checkpoint source-grant/route revocation. The trusted Integrator admission separately checks allowed input artifact scope, user-approved integration + protected later five-member review/premortem budget, permissions, provider egress/credentials, available sandbox resources, approved model/tool policy and execution epoch. A frozen draft that cannot pass these observations stays **FROZEN_NOT_ADMITTED/BLOCKED** rather than being labeled executed.

**Ordering and races:** when a final comparison Blueprint is ready, the existing transaction/guard system fences new ordinary review-message/admission work **under the same generation/obligation frontier used by `/done` and checkpoint closeout**. Any legitimately accepted required objection/message before the fence increments obligations and prevents freezing until disposition. A stale freeze attempt cannot overtake a newly accepted objection; two competing versions cannot both become the one authoritative Blueprint for the same integration generation. After immutable freezing the runtime requests checkpoint closure and revokes externally held read routes/grants. A SQL write of `CLOSING`, `CLOSED` intent or `BLUEPRINT_FROZEN` **never itself proves external revocation**.

**Unanimity is not required:** members can finish communication while preserving `DISPUTED` findings, acknowledged risks and unresolved-but-permissible alternatives. If a choice depends on new customer scope, safety-critical deviation, unapproved data/egress or budget, the dependent execution remains **blocked for existing explicit user approval**; the runtime must not infer a permission from a headcount. A forced-incomplete closeout retains its recorded report/partial artifacts but **does not satisfy this approved executable-handoff rule**.

**After freeze:** immutable records are not edited in place. Any material correction needs a newly authorized Blueprint version/generation, provenance and appropriate original-member review/closure and scoped permissions; only one exact frozen Blueprint version can be the Integrator's current approved input. A routine Integrator execution detail within that version remains governed by bounded ADR-26 discretion and required deviation records—not a wholesale fresh Council vote.

## 3. Deployment and implementation contract still to specify

**Reuse existing application components only:**
- **Step 3 PostgreSQL:** canonical authenticated member action/event source refs, current checkpoint generation/obligations and five valid /done/closeout certificates, Blueprint drafts and immutable hashes, source/evidence/candidate manifests, freeze and executable/admission projection, Integrator grant and operation identity. No new DB.
- **Step 4 typed command and UI:** illustrative `RecordCouncilDecisionPosition`, `RecordCouncilDecisionObjection`, `RecordCouncilDecisionRecommendation` and `FreezeIntegrationBlueprint` are **candidates for existing action/command registry refinement**, not a demand for new message transports. Actor, version, scope, idempotency, admissible status, return receipts and command-to-event definitions remain to specify. The trusted backend alone authors freeze/observed executable transition; members author intellectual content.
- **Step 5 transactions and external effects:** canonical same-frontier locking and idempotent event/outbox commits; exact freeze intent/observation; source read grants/revocation with UNKNOWN reconciliation; no cross-PostgreSQL/Git/Docker atomicity claims. Physical closeout/access proof is verified before separate Integrator read-grant admission.
- **Step 6 graph and Step 11 knowledge:** complete cited source and position-change lineage; no invented initial stance, source-independence or automatic majority-as-truth; no private cross-member leakage before sealed reveal.
- **Existing IRC/checkpoint gateway:** full member-authored messages and structured actions, five real sealed reviews before reveal, current /done frontiers, pending obligations, response dispositions, verification-only /work and observed physical revocation. No unsolicited files, direct peer messaging bypass, extra supervisor or majority voting gate.
- **Existing Final Integrator role:** receives only permitted immutable source/evidence and the exact executable Blueprint after authorized new source grants, respects Council recommendation by default and records evidenced material deviations for original five-member re-review.

**Crash/edge cases to preserve (test plans, NOT RUN):**
- New objection races with /done or freeze: serialize under the existing checkpoint frontier and do not lose the objection.
- Backend crash between immutable freeze intent and verified snapshot: reconcile exact content/hash, no fabricated frozen state.
- All five finish legitimately but peer grants fail to revoke: Blueprint stays non-executable; do not admit Integrator using lingering checkpoint rights.
- Invalid/missing contributor citation: freeze blocked or material source removed through attributable correction; no backend-invented Council conclusion.
- Recovery after successful freeze but before Integrator source grant: resume from exact pinned Blueprint and recheck contract, consent, cost and source-grant physical observations.
- Missing reviewer, incomplete forced closeout, review allowance exhausted or UNKNOWN consequential operation: no forged five-member normal closure; preserve incomplete evidence.
- Two concurrent freeze/launch attempts: idempotent same-version replay, otherwise expected-version conflict; no double integrator admission.
- Different permitted domains/formats: validate their actual content-hashed source manifests rather than requiring a Git SHA for a research report.

## 4. Status and next design boundary

**Approved on October 16, 2026:** (A) structured Council-authored material conclusions with no AI-inferred consensus, and (B) immutable validated Blueprint execution handoff **only after genuine five-member closure and independently verified access revocation**. These are policy contracts and refine rather than replace ADR-26/ADR-25 and existing checkpoint mechanics.

**Still to design:** exact Step 3 DDL/constraints, Step 4 command/event payloads and actors, Step 5 freeze/concurrency/UNKNOWN race reconciliation, versioned reference/manifest validation, and follow-on persistent Final Integrator lifecycle plus actual five-member re-review state transitions and failure-recovery tests. Step 8 as a whole is **IN DESIGN**; application build and all runtime/evaluation tests remain **NOT STARTED / NOT RUN**.
