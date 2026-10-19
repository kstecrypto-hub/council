# Steps 8.5C + 8.5D — Lean command, recovery and finalization contract

**Owner correction, October 16, 2026:** Simplify. **ADR-40 dedicated internal-API submission queues are SUPERSEDED.** Reuse the **existing Step 7 low-resource whole-agent execution scheduler** and **existing Step 5 PostgreSQL transactions/operation queue**. Docker provides container isolation and durable volumes; the trusted runtime already handles logical agent admission and recovery authorization. Do not build a second API scheduling/queue/recovery layer. **ADR-36–39 remain approved.** No app code, database migrations, Docker implementation, queues, or runtime tests have been executed; Step 8 remains **IN DESIGN**.

Prerequisites: [Step 8.5A](STEP_8_5_STRUCTURED_COUNCIL_BLUEPRINT_HANDOFF.md), [Step 8.5B](STEP_8_5B_FINAL_INTEGRATOR_EXECUTION_AND_RECOVERY.md), [Step 8.4](STEP_8_4_COLLECTIVE_SYNTHESIS_AND_FINAL_INTEGRATION.md), [Step 7 scheduler](PART_7_MEMBER_SCHEDULING_RECOVERY_RESOURCES.md), [Part 5 transactions](PART_5_TRANSACTIONS_IDEMPOTENCY_CONFLICTS.md), [Part 4 command registry](TYPED_INTERACTION_CONTRACTS.md) and [PostgreSQL data model](POSTGRES_DATA_MODEL.md). This file is **the authoritative replacement** for the earlier over-specified 8.5C/D queue plan.

## 1. Approved policies (ADR-36–39 and simplified ADR-40)

**ADR-36 — Reuse one typed command/state system.** Extend existing actor-scoped Part 4 commands and current run activities through executable Blueprint, persistent non-voting Integrator, one verified integrated output, five original-member sealed review, separate five sealed premortems, exact user approval and verified customer-owned delivery. Prefer existing commands with a stage/review-kind discriminator where semantics already fit. No second global lifecycle, microservice, sixth Council seat or automated winner judge.

**ADR-37 — Exact immutable versions.** Bind all decisions and reviews to the precise approved Contract, Blueprint, code or content-hashed non-code artifact, review generation, frozen premortem artifact+provisional report pair, and final user package. Old reviews/tests/acceptance do not silently transfer to new substantive versions; genuine five-member delta or full re-review still follows ADR-28. Exact version validation is a simple existing transaction guard, not a new version-control subsystem.

**ADR-38 — Existing failure/recovery mechanisms.** Step 5 provides durable intent/outbox, idempotency, transaction/epoch guards and UNKNOWN consequence/billing reconciliation. Step 7 provides whole-agent admission, pause/stop, limited hardware scheduling and safe logical restart. Docker/cgroups provide isolation, execution resource limits, observable exits/OOM and **named-volume persistence of files**. No per-worker resurrection supervisor, extra orchestration queue or artificial failure-handling manager. Docker itself does **not** restore live LLM/process memory or know whether an external model call, paid operation or Git write completed after a timeout; the **already-approved** Council runtime retains these few necessary facts.

**ADR-39 — Honest completed outcome.** Distinguish model-authored output-ready **intent**, mechanically observed immutable artifact, actual protected test PASS/FAIL/NOT_RUN, completed five-person review, sealed hypothetical premortem, explicit exact-version user acceptance, archived customer-owned artifacts with valid reference/restore checks, and authorized resource cleanup. **Only applicable verified delivery/cleanup permits `RunCompleted`**, never a model saying "finished" or a mere five-member verdict. Research may be explicitly inconclusive if the approved objective allows it; an incomplete application cannot be presented as a delivered working application without user-approved scope change.

**ADR-40 — Simplified/superseded queue requirement.** The previously approved **new per-key internal API submission queues are withdrawn** at the owner's request. **Do not implement them by default.** The previously approved **Step 7 seat/resource queue** schedules whole agent/Integrator execution on low-spec hardware; **Step 5 existing committed event-clock, row/aggregate locks, scoped idempotency, review-seat unique constraints and generation checks** already safely handle simultaneous API submissions. Two distinct authentic members may submit at the same wall-clock moment; both records persist under distinct seat identities. No sleep, timing offsets, new queue-specific DTO, Redis, in-memory lane or global serial API are required. Reconsider only upon actual observed performance/contention evidence and separate approval.

## 2. One compact versioned transition chain (reusing Part 4)

| Transition | Authority | Minimal hard condition |
| --- | --- | --- |
| Council-authored Decision Register -> frozen Blueprint | Five original members author; trusted backend assembles/freeze | Genuine structured member positions/citations, real five comparison reviews, immutable exact source and Contract version; no inferred consensus. |
| Frozen Blueprint -> executable handoff | Trusted backend | Genuine five-member normal `/done` and closeouts, no required outstanding discussion or `/work`, **verified** checkpoint read-grant/route revocation. Forced-incomplete closeout is not approval. |
| Integrator admitted and running | Existing trusted runtime | Same persistent non-voting Integrator identity, approved source grants/workspace/epoch/provider/egress, separate user-approved integration pool and protected downstream review capacity. |
| Integrator declares output ready | Integrator | Authored current-version code Git tree or non-code content-hashed manifest, evidence and limitations. **Not a verified artifact or test PASS.** |
| Integrated output frozen/verified | Trusted backend | Actual immutable artifact and reference closure, fenced writers, safe whole-integrator suspension and reconciliation of material outstanding operations. |
| Five sealed independent integrated-output reviews | **Original five members** | One exact frozen integrated output version, reviewer identity+generation, five distinct current authentic submissions and a single atomic reveal. Integrator never acts as a sixth reviewer. |
| Material revision if needed | Same logical Integrator, after review closure | Authorized new writable generation; original reviewed target stays immutable. ADR-28 five-person delta/full scope as supported by actual impact evidence. |
| Five-member premortem | Original five members | One exact frozen integrated artifact + provisional report pair, five hypothetical sealed submissions and atomic reveal; preserve scenario uncertainty. |
| Final package/user acceptance | Trusted editorial/report assembly; **user** decides | Actual verification status and attributable findings; immutable one-result package bound to exact Contract, artifact, evidence and report; existing user interaction. |
| Verified archival/cleanup -> `RunCompleted` | Trusted runtime | User-accepted current package; customer-owned authorized export/restore/reference closure, relevant consequence reconciliation, verified retention and temporary cleanup. |

Existing commands such as `CreatePeerAction`, `SubmitIndependentCheckpointReview`, `RevealCheckpointReviews`, `MarkCheckpointCommunicationDone`, `AcceptCandidate`, `RequestCandidateRevisions`, `FinalizeCandidate` are **reused** when suitable with proper actor, target and review-kind fields. Only add a command if the existing semantics genuinely cannot express the required operation. Existing state, transaction and actor checks remain mandatory; they need not be redesigned here.

## 3. Exactly simultaneous submissions: existing PG correctness

When Members 2 and 4 submit review assessments at exactly the same instant:
1. The existing internal API authenticates each original seat and its exact current review generation/immutable artifact ID.
2. The established Step 5 transaction and scoped idempotency receipt handle concurrent mutations, including cross-process deployment. Each unique **(generation, original_member_seat)** persists once; retries with the same key/hash return their original receipt.
3. The trusted backend may reveal the previously private assessments only after **five genuine unique current-generation seats actually commit**, in one atomic visibility transition.
4. A duplicate from Member 2 cannot fill Member 5's missing assessment; a review targeting V1 cannot count toward V2. The canonical event-clock, not wall-clock timestamp or a queue position, records committed order.

This is sufficient **without a dedicated API submission queue**. Continue using Step 7's original slot/resource queue for limited hosts, the existing durable operations/outbox for runtime work, and the checkpoint gateway's existing message/action inbox for inactive/working peers. They are different uses, not duplicate services. No extra per-key API dispatch or artificial stagger is necessary.

## 4. Docker versus Council responsibility — minimal recovery contract

**Docker/cgroups handle** sandbox resource isolation, actual container stop/exit events, and keeping agent-written files/Git/notes on the permitted persistent named volume or bind mount. Whole-agent stop/recreate lets limited hardware reuse a slot after trusted observed quiescence and release.

**The existing Council controller (Step 5 + Step 7) handles** permission to start/resume under current member/integrator identity, Contract, epoch, budget, grants and checkpoint; restoring that same logical agent with its correct volume; preserving submitted reviews/decisions and actual verified artifact identities; and reconciling uncertain external side effects/costs before an unsafe retry.

Stopping/restarting Docker **does not** preserve RAM, running worker processes or unflushed work. An intentionally paused, checkpoint-ready, suspended or budget-exhausted agent must not restart itself via Docker `restart: always`; Step 7 already governs scheduled re-entry. Workers' local continuation is the member/Integrator's concern, from saved artifacts; no per-worker restart table.

**Examples using existing operation ledger only:**

- Container dies after writing a file: restart same logical authorized agent with its retained volume; inspect saved work, don't pretend unsaved thinking survived.
- Container dies after paid provider request: Docker cannot determine its provider completion/bill; keep Step 5 UNKNOWN and possible charge until reconciled. Don't blindly repeat potentially consequential calls.
- Final Integrator freezes output while a worker could still modify it: no verified pinned output until trusted runtime observes immutable selected artifact and safe write fencing.
- Five reviews complete but tests fail: report genuine review completion and failure; do not automatically call product successful.
- User accepted the final report but archive restore fails: acceptance remains a real decision; delivery is not verified and runtime stays in truthful FINALIZING/incomplete condition.

No newly invented recovery retry engine or special stage-specific queues.

## 5. Minimal contract/verification cases still pending, not run

Existing Steps 3–5 implementation will need the **smallest necessary** exact DTO extensions and SQL uniqueness/expected-version checks for Integrator actor, artifact/review identity and final package. Avoid speculative workflow transitions, extra table families or abstract queue interfaces.

Eventually verify (when implementation is separately authorized):
- simultaneous distinct original-seat reviews each persist; a duplicate doesn't count twice; atomic reveal only after five;
- frozen Blueprint still cannot launch Integrator while checkpoint grants remain physically active;
- original five Council seats cannot be impersonated by Integrator or sibling;
- same durable agent/volume recovers under Step 7, not uncontrolled Docker restart;
- UNKNOWN provider/Git side effects are not silently re-sent or called free;
- an Integrator ready claim without actual pinned safe result cannot open review;
- V1/V2 reviews, premortem artifacts, provisional reports and user acceptance cannot be mixed;
- mandatory failed/not-run checks or incomplete archive/reference restore cannot produce `RunCompleted`.

These are **test cases, not results**. Exact DTO/DDL/external adapter wiring is **still IN DESIGN**; no application code, Docker deployment, migrations or runtime/security tests have been run.

## 6. Current status

Owner approved the **simplification and supersession of ADR-40**, while retaining ADR-36–39. This corrected document **supersedes** the earlier overengineered 8.5C/D queue proposal. **Council Step 8 remains IN DESIGN**, not marked DESIGN COMPLETED; implementation remains NOT STARTED and tests NOT RUN.


## October 19 — exact v1 design specification boundary

The earlier interface-design questions are specified in [Step 2 snapshot/transfer](STEP_2_SNAPSHOT_TRANSFER_CONTRACT_V1.md), [Steps 3–5 relational/typed/transaction contract](STEPS_3_TO_5_EXACT_INTERFACE_CONTRACT_V1.md), [Step 8 action/finalization contract](STEP_8_ACTION_AND_FINALIZATION_CONTRACT_V1.md), and [unexecuted verification matrix](STEP_2_TO_8_VERIFICATION_MATRIX_V1.md). Conflicting earlier claims that these **v1 interface choices** remain undecided are superseded, while original owner policies and archival decision history remain unchanged. Steps 2–5 and 8 are **DESIGNED** as specifications, not implemented. Physical migrations, code, real broker/provider integrations, actual concurrency/runtime/security/model tests **NOT STARTED / NOT RUN**. Implementation-time customer configuration and Step 9–11 adapter choices remain open. ADR-40 additional API submission queues remain superseded.
