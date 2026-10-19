# Steps 2–8 cross-step reconciliation — October 19, 2026

**Status: design-contract reconciliation only.** This document aligns the previously reopened Steps 2–5 and existing Steps 6–7 with owner-approved Steps 8.3–8.5. It makes no new Council architecture decision, changes no user authority, and does not claim SQL migrations, executable DTOs, product implementation, security verification or runtime tests. For actual implementation, the current approved Project Contract and [architecture decisions](ARCHITECTURE_DECISIONS.md) take precedence over superseded historical text. See also the [lean Step 8.5C+D source of truth](STEP_8_5C_8_5D_COMMAND_STATE_RECOVERY_AND_FINALIZATION.md).

## Scope and unchanged invariants

- Exactly five original logical Council member seats. A persistent **non-voting** Final Integrator is a distinct *execution actor*, never a sixth reviewer/seat or an intellectual supervisor.
- Five genuinely independent investigations, genuine source/member-authored checkpoint positions, a versioned Council Decision Register and Blueprint, one integrated deliverable by default, independent sealed re-review by the original five, a separate sealed premortem and **explicit user acceptance**.
- Reuse the existing customer-local Git/artifact snapshot service, typed gateway, PostgreSQL event clock/transactions/idempotency/outbox, Step 6 evidence graph, Step 7 whole-agent resource admission and Docker persistent volumes. **Do not create an API serialization queue, new message broker, new global winner-voting mechanism, second database or per-worker recovery manager.**
- Data stays customer-owned; optional external/public Git publication and cross-customer knowledge require separate consent. Moderation uses the **hosted OpenAI Moderation API** only when customer-authorized, never a fictitious local open-weight service; deterministic authorization always remains final.

## R1. Steps 2/3: actor identity and durable data lineage

Logical identity and physical sessions are separate:
- **Member seat**: existing fixed seat 1–5, private customer-owned workspace/repo or permitted domain artifact workspace, authoring phase/version and budget.
- **Final Integrator**: exactly one run-scoped persistent logical execution identity *outside* the five-member seat uniqueness constraint; its current provider/model session(s), execution epochs, isolated durable workspace, admission, source grants and phase spending are associated with this identity. A crash creates a new authorized epoch of the **same** logical Integrator, never a new peer.
- **Blueprint revision**: contract/run/checkpoint-generation references; source-authenticated member Decision Register; alternative, dissent, selected/conditional/excluded contribution references; selected immutable source/evidence manifest; hash; DRAFT/FROZEN/EXECUTABLE-HANDOFF-VERIFIED distinction.
- **Integrated output revision**: own ID/generation, exact Blueprint/Contract, source dependency closure, content hash and manifest, Integrator authorship and operations, actual independently observed hash/quiescence/reconstruction evidence, verification check outcomes (PASS/FAIL/NOT_RUN), supersession history. Output-ready *intent* is not verification.
- **Review generation**: one exact verified integrated output revision and target manifest/hash; exactly original seats 1–5 can each commit one distinct authenticated sealed review per generation. Store actor/epoch/idempotency, complete result, scope (initial FULL, later warranted DELTA/FULL), submission sequence and independent atomic reveal marker. An old version's review can never count for another version.
- **Premortem generation**: *different* sealed generation keyed to one frozen integrated output hash **and** one provisional report hash, with five authentic seat submissions and independent all-five reveal; observations of future outcomes are not invented.
- **Final acceptance/archive**: user decision explicitly binds the exact integrated output/report/package hashes, observed verification statuses and relevant limitations, then separate authorized archive/restore verification, reference closure, grant cleanup and resource teardown evidence. Mark delivery/completion only after those real effects are observed.

Physical SQL schema/constraints, protocol serialization and migrations remain IN DESIGN. The authoritative transactional semantics are below; a conceptual record list is not proof of implemented tables.

## R2. Steps 4/5: versioned commands, final acceptance and atomic boundaries

Use the **existing** authenticated typed-command processor and event/operation ledger, not parallel mechanisms. Existing final user commands such as `AcceptCandidate`, `RequestCandidateRevisions`, `RejectCandidate` and `CancelFinalization` retain their command family names where useful, but in the default integrated-finalization path the target is **the immutable integrated result/package**, not a best-of-five original candidate. A compatibility adapter must reject ambiguous bare candidate IDs and old original-candidate approvals; require exact run, approved Contract, target kind, integrated output generation/content hash, provisional report/package hash, applicable review/premortem generations and expected canonical state version. A stale target requires re-review/reapproval, never silent retargeting. User approval is not Integrator intent, peer consensus or a UI status.

For each consequential command:
1. Authenticate actor, scoped permissions, current phase/epoch and user consent; deduplicate identical scoped command ID+canonical payload **before** stale-transition checks but after authentication/authorization.
2. Lock the established Part 5 deployment event clock first, then run/phase/budget/target review generation in the existing canonical lock order. Reject wrong Blueprint/output/report/generation, invalid seat or duplicate different-payload claim. An original member cannot impersonate the Integrator and vice versa.
3. Commit immutable command receipt, intent, current generation/version, one protected chargeability scope, budget reservation, event and outbox atomically in PostgreSQL. Dispatch external model, Docker, local snapshot/artifact or user-authorized provider effect **after** commit.
4. Observe external results separately; reconcile UNKNOWN/TIMED_OUT effects before any consequential retry. Increment execution epoch/fence old writers on loss of authority. PostgreSQL cannot atomically prove an external Git revision, filesystem read-grant removal, provider charge or Docker suspension.
5. For five-member sealed review/premortem, allow simultaneous distinct seats to commit in either arrival order under PostgreSQL uniqueness and the shared generation lock; the fifth legitimate committed assessment enables **one atomic reveal**. Reject stale generations and preserve earlier sealed/historical records.

Never mark verification PASS from source existence, model-reported completion or a successful API submission. An explicitly incomplete/failing review may be recorded truthfully but does not satisfy mandatory five-real-review gates.

## R3. Steps 2/4/5: customer-local snapshot and expired-access safety

A source/read grant is exact-purpose, read-only, time/epoch-limited and recipient-scoped: record run/phase, checkpoint or integration/review generation, approved source manifest and hash, permitted selected objects, customer authorization/data-egress policy, grantee, issuance/expiry, desired and **observed** enable/revoke states and operation attempts. Grant authorization does not prove physical readability; revocation intent does not prove removal.

- During checkpoint OPENING, enable sealed review only after verifying the frozen customer-local selected snapshots are hash-valid, readable to the intended recipients and no unapproved source is exposed.
- On CLOSING, fence new reads/messages in the canonical transaction, cancel/fence in-flight work where supported, dispatch independent grant/route revocation and verify observed no-access/isolation. Unknown/partial revocation keeps closure and return to private writing **blocked**. A cached earlier disclosure cannot be made unknowable; no fresh access is permitted.
- After the final-comparison checkpoint has **normally** closed and its peer routes/grants have actually been revoked, issue separate new approved Integrator read grants. A frozen Blueprint by itself grants nothing.
- On expiry, revocation, customer consent withdrawal, stale epoch or lost trust, deny **new dependent reads and work** immediately; retain unknown operations/effects and reconcile partial transfers. No silent grant renewal or reusing checkpoint grants for synthesis. To resume, require current authorization, exact immutable manifest and observed grant, budget, Contract and epoch rechecks. Old read tokens/credentials must not be persisted into agent workspaces.
- The same verified close/revoke boundary applies when ending read-only post-integration review before Integrator editing may resume; archive/deletion needs validated surviving references first.

## R4. Step 2–6: domain-neutral artifact contract

Member work and finished output may be **software or non-software**, according to the approved Project Contract. For code, pin customer-local Git commit/tree, environment and reproducibility evidence. For research, hardware, strategy and documents, use immutable content-hashed artifact/evidence manifests, named dependencies/versions, applicable citation/provenance graph and an appropriate verification method. Do not invent Git commits, tests or build/reconstruction claims for a PDF, research synthesis or other non-code output. The comparison, sealed reviews, Blueprint, exact output identity, impact invalidation, premortem, user acceptance and customer-retention policy remain the same. A negative/inconclusive investigation may contribute truthfully but cannot masquerade as a viable software deliverable or satisfy a different user contract without explicit scope revision.

## R5. Steps 3/4/5/7: five protected budget scopes (ADR-27)

**The 70/25/5 split is superseded as Council's mandatory-integration setup default**, including in machine-readable contract and UI guidance. Propose a **project-specific, explicitly user-approved** distribution across:
1. Original-five member independent development (including their internal workers);
2. Checkpoint comparison, sealed assessment and verification-only discussion work;
3. Separately authorized Integrator execution and its worker attempts;
4. Five-member post-integration validation, reruns and distinct premortem;
5. Orchestration, report assembly, approved delivery/archive and related overhead.

No universal replacement percentage is approved. One consequential spend attempt charges **one** scope, additionally enforced against its parent run/phase/member or integrator ceiling, with conservative reservations, actual settlement and UNKNOWN liability. Approval of an Integrator does not authorize consumption of protected reviewer allowance; check minimum authorized next-review capacity before Integrator admission. Any redistribution/top-up requires an immutable new explicit user-approved budget policy version. Local/provider usage forecasts remain non-binding and Council limits do not guarantee provider invoices.

## R6. Step 8.4: contested recommendations without a new voting system

For each **material** comparison decision, authentic original-member actions produce an attributed Decision Register containing admissible alternatives, hard requirements, independent earlier positions *only if actually authored*, final positions and change reasons, independent or shared evidence, minority objections, scope, applicability and status. The following **decision order** applies:
1. Filter options that violate hard approved requirements, rights, source/data consents, permissions or demonstrated contraindicating evidence. One supported counterexample may defeat many unsupported endorsements.
2. Prefer alternatives with more applicable verification and contractual fit. The members' evidence-backed Council recommendation is the default; support by multiple independently reasoned seats is a meaningful **rebuttable** secondary signal, never a numeric truth score, mandatory unanimity or mechanical majority.
3. If alternatives remain genuinely plausible, record a bounded **conditional/provisional, reversible** selection and what five-member validation must test. Ordinary implementation technique within authorized Blueprint scope can be chosen by the Integrator with an attributed rationale/deviation record; it must disclose material departure on five-member re-review.
4. If unresolved conflict would force a material high-level scope, safety, IP, egress, contract acceptance or resource decision **outside** granted authority, retain `REQUIRES_USER_DECISION` and use existing Orchestrator/user-approval interactions. No executable Integrator admission on that unresolved dependent action until the user selects an authorized path. If authorization/viable option is unavailable, report an honest blocked/incomplete outcome, not a fabricated Council majority or silent sixth-model decision.

An actionable Blueprint need not claim five-member agreement. It must explicitly bind the choice, conditions, dissent and permitted continuation. A late real objection moves the current frontier/version and invalidates stale ready/handoff declarations.

## R7. Exact re-review, premortem and final result versioning

- The **first** verified integrated result requires five independently sealed original-member FULL assessments before the existing atomic reveal.
- A **substantive localized** revision requires five genuinely new independent sealed DELTA assessments *of the new exact hash*. Foundational, high-risk or uncertain change requires five new FULL assessments. A demonstrably non-substantive/equivalent change can retain only mechanically evidenced prior applicability; no guessed equivalence.
- Changed artifact dependencies require actual affected verification reruns; old PASS/FAIL records remain historical and do not auto-transfer. A reviewer who is suspended, blocked, budget-exhausted or absent is **not** a submitted review.
- The five independently sealed hypothetical six-month-plus premortems target a single frozen `(integrated_output_hash, provisional_report_hash)` pair. A change of either target or material claim creates a new appropriate generation; do not mix old and new scenarios or confuse hypotheticals with observations.
- Exact frozen final package + visible limitations/check statuses + actual required review/premortem dispositions => present to **user**, who alone accepts/revises/rejects. A user acceptance is not project delivered until customer-owned archive/export hash/reference-restore checks, applicable grants/revocations, outstanding consequential operations and cleanup are separately observed and recorded.

## Verification cases required later — NONE EXECUTED

| Case | Expected runtime invariant |
| --- | --- |
| Two genuine same-millisecond member submissions | Both stored once, same generation, no extra API queue, no premature reveal |
| Fifth sealed submission / duplicate retry / conflicting payload | One atomic reveal; identical replay returns same result; different payload rejected |
| Checkpoint grant expires or revoke returns UNKNOWN | Dependent work blocked until independently observed new authorization or revocation |
| Integrator crash after model/provider dispatch | Same logical Integrator and frozen lineage retained, unknown effects reconciled, stale epoch fenced |
| Initial output intent without actual verified hash/quiescence | No five-member integrated-review opening or false PASS |
| Software Git and non-code content-hash artifact | Correct Project Contract-specific verification; no invented repository/test |
| Original candidate ID accepted instead of current integrated target | Reject stale/ambiguous command; user decision binds exact result/package |
| Five-member delta revision and separate premortem target changes | Five fresh legitimate matching assessments when required; no mixed-version seal/reveal |
| Integrator runs out of budget but review pool exists | No unauthorized borrowing, incomplete/blocked stated |
| Disputed high-level decision needs user consent | No silent Integrator vote, no unauthorized dependent execution |
| Hosted moderation unavailable or customer egress not approved | New affected guarded operation fails closed; local deterministic permission checks remain authoritative |
| Archive fails validation or an external revoke is UNKNOWN | Do not mark run delivered/COMPLETED or delete necessary recovery data |

**Completion ledger:** R1–R7 are **SPECIFIED/RECONCILED IN DESIGN**, not IMPLEMENTED and not VERIFIED. Exact SQL migrations, typed v1 wire DTOs, adapter capability checks and actual runtime/concurrency/failure-injection evaluation remain **IN DESIGN / NOT STARTED / NOT RUN**. This document does not close Steps 2–5, Step 8 overall, or Step 9 onward.
