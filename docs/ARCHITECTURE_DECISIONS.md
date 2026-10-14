# Architecture decisions and verification boundary

**Owner approval:** October 13, 2026, with phase-budget clarification October 14, 2026. **Delivery:** specification amendments only.
**Application implementation:** NOT STARTED. **Runtime tests/evaluations:** NOT RUN.

The owner corrected the repository policy to public member repositories at checkpoints and approved the other architecture-review improvements. Current topic documents incorporate these decisions; this index tracks them without declaring implementation complete. The latest owner instruction remains authoritative.

| ID | Accepted requirement | Primary specification | Design status | Runtime implementation / tests |
|---|---|---|---|---|
| ADR-01 | Private/public/private member repositories; publication consent/history checks; frozen SHAs; no collaborator grants | PART_4A_AUTHORITY_BOUNDARIES.md | Specified; GitHub integration pending | NOT STARTED / NOT RUN |
| ADR-02 | Five fixed members; Orchestrator-defined semantic phases; member-declared readiness; per-member/phase token-cost ceilings instead of mandatory private-work slices; all-five barrier; explicit blocked/failed members | PART_7_MEMBER_SCHEDULING_RECOVERY_RESOURCES.md | In design; concrete limits/wiring pending | NOT STARTED / NOT RUN |
| ADR-03 | Separate disposable peer verifiers and protected acceptance evidence | CHECKPOINT_COMMUNICATION_GATEWAY.md | Specified; containment backend pending | NOT STARTED / NOT RUN |
| ADR-04 | Operation-class uncertainty gates and stale-epoch fencing | PART_5_TRANSACTIONS_IDEMPOTENCY_CONFLICTS.md | Specified; adapters/recovery wiring pending | NOT STARTED / NOT RUN |
| ADR-05 | Atomic conservative reservations, hard per-phase/member token/cost budgets, protected review allowance, optional non-binding uncertain token estimates, resource-vector admission | PART_7_MEMBER_SCHEDULING_RECOVERY_RESOURCES.md | In design; schema/defaults pending | NOT STARTED / NOT RUN |
| ADR-06 | Transactional committed event ordering; no skipped outbox rows; canonical state above framework checkpoints | POSTGRES_DATA_MODEL.md | Specified; migrations/concurrency tests pending | NOT STARTED / NOT RUN |
| ADR-07 | Outcome milestones; faithful source-linked clarifications; scoped Orchestrator memory | PART_4A_AUTHORITY_BOUNDARIES.md | Specified; contracts/UI integration pending | NOT STARTED / NOT RUN |
| ADR-08 | Sealed independent reviews before shared discussion | CHECKPOINT_COMMUNICATION_GATEWAY.md | Specified; Step 8 integration pending | NOT STARTED / NOT RUN |
| ADR-09 | Version-bound /done; communication/verification/readiness/acceptance separation | TYPED_INTERACTION_CONTRACTS.md | In design; complete state wiring pending | NOT STARTED / NOT RUN |
| ADR-10 | Conditional evidence-backed Git lessons; frozen memory; verified archive closure before teardown | POSTGRES_DATA_MODEL.md | Specified; Step 11 policy/implementation pending | NOT STARTED / NOT RUN |
| ADR-11 | Single agent, five independent attempts, full Council, and ablations under consistent evaluation | APP_DESIGN.md | Evaluation requirements specified | NOT STARTED / NOT RUN |
| ADR-12 | Reconciled defaults and explicit status/evidence tracking | architecture_contract.json | Documentation/contract maintenance only | Council runtime NOT STARTED / NOT RUN |

## Completion policy

SPECIFIED means requirements have been written. IN DESIGN means named design decisions or integration details remain open. IMPLEMENTED requires executable behavior and a code reference. VERIFIED requires actual test execution, scope/environment, and result evidence. A test plan, stub, mock, static documentation check, or successful push cannot by itself complete a runtime step. No row above marks runtime work completed.

Step 7 remains open for concrete phase-budget defaults/accounting, individual operation-timeout/recovery ceilings, capacity sizing/provider compatibility, reservation schemas, pause/stop wiring, and enforcement tests. Mandatory periodic private-work slices were superseded by the owner's October 14 decision; budget exhaustion preserves an incomplete member, never forced readiness. Step 8 still needs the full member loop and termination/progress policy. Step 10 still needs tested containment. Step 11 still needs memory selection, lesson promotion, and archive-validation implementation. Earlier design-baseline approvals are not evidence that these new details are finished.

## Required runtime evidence (all pending)

- [ ] A one-slot execution admits the next eligible member once the current member reaches the milestone, blocks, safely yields, or exhausts its authorized phase budget; exhaustion never implies checkpoint readiness. No mandatory periodic private-work rotation is required.
- [ ] Phase token estimates are displayed only as uncertain forecasts, separately from user-approved quotas and metered usage; they never silently adjust the hard budget.
- [ ] Missing/failed members cannot silently shrink Council or pass either arrival or sealed-review barriers.
- [ ] Public opening checks all exposed refs/history/surfaces; partial/unknown transitions remain guarded; failed private closure prevents new unpublished commits; prior exposure is never claimed erased.
- [ ] Sealed reviews do not leak via repository commits, gateway, retrieval, caches, or member context before reveal.
- [ ] Peer test code cannot write another persistent workspace, continuation state, credentials, or protected acceptance definitions.
- [ ] Unknown inference allows safe unrelated progress with retained accounting; unknown writes are not blindly repeated; uncertain authority fails closed.
- [ ] Simultaneous member/worker/Orchestrator requests cannot overspend or consume protected review funds; timeout does not refund uncertain dispatched usage.
- [ ] Delayed commits, rollback, duplicate/out-of-order outbox delivery, and snapshot/SSE races cannot lose canonical events or falsely advance projections.
- [ ] Restored framework state cannot override canonical permissions, current epochs, or external-operation outcomes.
- [ ] New messages/actions race with /done and closure without being missed; deferred tests do not become passes.
- [ ] Processed clarification strength/scope is preserved; branch-local normalization memory does not influence unauthorized branches.
- [ ] Retained lessons resolve evidence after a fresh archive checkout without the temporary database; broken references prevent teardown.
- [ ] Comparative experiments and ablations run with fixed evaluation, full spend accounting, and failure/regression reporting.
