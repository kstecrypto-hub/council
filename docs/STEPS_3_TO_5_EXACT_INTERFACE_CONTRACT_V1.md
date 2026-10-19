# Steps 3–5 — Exact final-phase data, typed commands and transaction contract v1

**Status: DESIGN-SPECIFIED (October 19, 2026); not a migration, deployed API, or test result.** Normative under the approved [Step 2 transfer contract](STEP_2_SNAPSHOT_TRANSFER_CONTRACT_V1.md), [R1–R7 crosswalk](STEPS_2_TO_8_CROSS_STEP_RECONCILIATION_2026_10_19.md) and [Step 8 phase protocol](STEP_8_ACTION_AND_FINALIZATION_CONTRACT_V1.md). **No new PostgreSQL database, external queue, separate Integrator service, persistent child-worker recovery service or sixth original member.** Use existing \`council_core\`/\`council_runtime\`, event clock, command receipts, outbox, grants, budget accounts and snapshots.

## 1. Stable v1 types and control-plane envelope

The **wire envelope** for a consequential command (JSON shown as the normative shape; exact values are illustrative):
\`\`\`json
{
  "protocol_version": "council.v1",
  "command_id": "18a4ae6b-9d92-4d4f-92ee-0c468ff9583a",
  "idempotency_key": "stable-logical-attempt-opaque-value",
  "run_id": "91a2d5a4-6f48-4f22-a57b-d3f42b15b2e7",
  "target_type": "INTEGRATED_OUTPUT",
  "target_id": "3226768b-2049-4982-a321-b02ca25f278c",
  "target_generation": 2,
  "expected_state_version": 12,
  "command_type": "SubmitIntegratedReview",
  "payload": {"review_generation_id": "f25823ee-f2f4-44f9-9310-d7a07d681031", "exact_output_sha256": "a64f...64_hex_chars", "assessment_ref": "sealed-customer-artifact-id", "assessment_sha256": "a64f...64_hex_chars", "scope": "DELTA"}
}
\`\`\`
The actual \`sha256\` is **64 lowercase hexadecimal characters**; short placeholders above are not valid payloads. \`command_id\` and \`idempotency_key\` are generated once for a logical operation and carried unchanged across retry/reconnect; \`target_generation\` and \`expected_state_version\` are strictly positive integers; \`payload\` validates under its specific command schema. Client-supplied actor/seat/role/session claims are **ignored**: derive actor and epoch from the trusted bridge. A model-authored suggestion is never accepted as the backend's observation of Git/Docker/provider/SQL.

**Canonical success reply:** \`{receipt_id, protocol_version, run_id, command_id, effective_state_version, event_position, operation_id?, status=ACCEPTED|ALREADY_APPLIED|REJECTED|PENDING_EXTERNAL, data?}\`. \`ALREADY_APPLIED\` for the identical authenticated scoped key+hash returns the **prior exact result**; it does not advance an event. **Error reply:** \`{code, correlation_id, expected_state_version?, actual_state_version?, retryable, receipt_id?}\`. Denials avoid leaking hidden branch/tenant identities.

**Minimum stable errors:** \`INVALID_SCHEMA, UNAUTHENTICATED, FORBIDDEN, USER_APPROVAL_REQUIRED, POLICY_EGRESS_DENIED, MODERATION_UNAVAILABLE, TARGET_NOT_FOUND_OR_FORBIDDEN, STALE_GENERATION, VERSION_CONFLICT, IDEMPOTENCY_CONFLICT, PHASE_GUARD_FAILED, FIVE_SEATS_REQUIRED, MISSING_REVIEWER, SOURCE_HASH_MISMATCH, UNSAFE_GRANT_STATE, UNKNOWN_EXTERNAL_EFFECT, BUDGET_INSUFFICIENT, REVIEW_SCOPE_INDETERMINATE, TEST_NOT_RUN, ARCHIVE_NOT_VERIFIED\`. Business rejection is persisted only if it changes canonical state or must be auditable under the existing policy; a malformed unauthenticated packet never becomes a canonical fact.

## 2. Normative additive relational schema and constraints (design-time DDL)

The baseline \`council_core.runs\`, \`council_core.council_seats\`, \`council_core.project_contract_revisions\`, \`council_core.events\`, \`council_core.command_receipts\`, \`council_core.acceptance_decisions\`, \`council_runtime.operations/operation_attempts/outbox/budget_accounts\` remain. The following **reference DDL is a specification of constraints**, not a run migration; implementation migrations must establish compatible types/indexes on referenced baseline tables, with the same-run FK checks and controlled RBAC/RLS. No physical schema has been applied.

\`\`\`sql
-- Design reference only. Parent runs(id), council_seats(run_id,seat_no)
-- and project_contract_revisions(id) are the existing Step 3 baseline.
CREATE TABLE council_core.final_integrators (
  id uuid PRIMARY KEY, run_id uuid NOT NULL REFERENCES council_core.runs(id),
  workspace_ref text NOT NULL, current_epoch bigint NOT NULL DEFAULT 0
    CHECK (current_epoch >= 0),
  status text NOT NULL CHECK (status IN
    ('PENDING_ADMISSION','ACTIVE','QUIESCING','SUSPENDED','BLOCKED','EXHAUSTED','FINISHED')),
  state_version bigint NOT NULL DEFAULT 1 CHECK (state_version >= 1),
  UNIQUE(run_id), UNIQUE(run_id,id)
);
-- Integrator id MUST NOT reference council_seats nor be allowed to submit
-- a council-seat review. Its container sessions/epochs are replaceable.

CREATE TABLE council_core.integration_blueprints (
  id uuid PRIMARY KEY, run_id uuid NOT NULL REFERENCES council_core.runs(id),
  revision_no bigint NOT NULL CHECK (revision_no > 0),
  contract_revision_id uuid NOT NULL REFERENCES council_core.project_contract_revisions(id),
  checkpoint_id uuid NOT NULL, checkpoint_generation bigint NOT NULL
    CHECK (checkpoint_generation > 0),
  decisions_json jsonb NOT NULL, source_manifest_sha256 char(64) NOT NULL
    CHECK (source_manifest_sha256 ~ '^[0-9a-f]{64}$'),
  blueprint_sha256 char(64) NOT NULL
    CHECK (blueprint_sha256 ~ '^[0-9a-f]{64}$'),
  frozen_at timestamptz, executable_handoff_verified_at timestamptz,
  checkpoint_revocation_evidence_ref text, closeout_frontier_sha256 char(64),
  status text NOT NULL CHECK (status IN ('DRAFT','FROZEN','EXECUTABLE','SUPERSEDED')),
  state_version bigint NOT NULL DEFAULT 1,
  UNIQUE(run_id,revision_no), UNIQUE(run_id,id),
  CHECK (executable_handoff_verified_at IS NULL OR
     (frozen_at IS NOT NULL AND checkpoint_revocation_evidence_ref IS NOT NULL
      AND closeout_frontier_sha256 IS NOT NULL AND status IN ('EXECUTABLE','SUPERSEDED')))
);
-- The trusted transition (NOT this row CHECK alone) verifies five real
-- current /done, closeouts, no /work, and observed physical revocation.

CREATE TABLE council_core.integrated_outputs (
  id uuid PRIMARY KEY, run_id uuid NOT NULL REFERENCES council_core.runs(id),
  blueprint_id uuid NOT NULL, integrator_id uuid NOT NULL,
  revision_no bigint NOT NULL CHECK (revision_no > 0),
  artifact_kind text NOT NULL CHECK (artifact_kind IN ('SOFTWARE_GIT','NONCODE_MANIFEST')),
  artifact_sha256 char(64) NOT NULL CHECK (artifact_sha256 ~ '^[0-9a-f]{64}$'),
  artifact_ref text NOT NULL, source_closure_sha256 char(64) NOT NULL
    CHECK (source_closure_sha256 ~ '^[0-9a-f]{64}$'),
  intent_event_id uuid, verification_event_id uuid,
  verification_evidence_ref text, write_fence_evidence_ref text,
  status text NOT NULL CHECK (status IN ('INTENT_ONLY','VERIFIED','STALE','SUPERSEDED')),
  state_version bigint NOT NULL DEFAULT 1,
  UNIQUE(run_id,revision_no), UNIQUE(run_id,id),
  FOREIGN KEY (run_id,blueprint_id) REFERENCES council_core.integration_blueprints(run_id,id),
  FOREIGN KEY (run_id,integrator_id) REFERENCES council_core.final_integrators(run_id,id),
  CHECK (status <> 'VERIFIED' OR
     (verification_event_id IS NOT NULL AND verification_evidence_ref IS NOT NULL
      AND write_fence_evidence_ref IS NOT NULL))
);

CREATE TABLE council_core.integrated_review_generations (
  id uuid PRIMARY KEY, run_id uuid NOT NULL REFERENCES council_core.runs(id),
  output_id uuid NOT NULL, generation_no bigint NOT NULL CHECK (generation_no > 0),
  output_sha256 char(64) NOT NULL CHECK (output_sha256 ~ '^[0-9a-f]{64}$'),
  impact_scope text NOT NULL CHECK (impact_scope IN ('FULL','DELTA')),
  impact_evidence_ref text, status text NOT NULL
    CHECK (status IN ('SEALED','REVEALED','DISCUSSION','CLOSING','CLOSED','ABORTED')),
  revealed_event_id uuid, closeout_evidence_ref text,
  state_version bigint NOT NULL DEFAULT 1,
  UNIQUE(run_id,output_id,generation_no), UNIQUE(run_id,id),
  FOREIGN KEY (run_id,output_id) REFERENCES council_core.integrated_outputs(run_id,id),
  CHECK (impact_scope = 'FULL' OR impact_evidence_ref IS NOT NULL)
);
CREATE TABLE council_core.integrated_review_submissions (
  id uuid PRIMARY KEY, run_id uuid NOT NULL REFERENCES council_core.runs(id),
  review_generation_id uuid NOT NULL, original_seat_no smallint NOT NULL
    CHECK (original_seat_no BETWEEN 1 AND 5),
  assessment_ref text NOT NULL, assessment_sha256 char(64) NOT NULL
    CHECK (assessment_sha256 ~ '^[0-9a-f]{64}$'),
  authored_epoch bigint NOT NULL, submission_event_id uuid NOT NULL,
  UNIQUE(review_generation_id,original_seat_no),
  FOREIGN KEY(run_id,review_generation_id)
    REFERENCES council_core.integrated_review_generations(run_id,id),
  FOREIGN KEY(run_id,original_seat_no) REFERENCES council_core.council_seats(run_id,seat_no)
);

CREATE TABLE council_core.premortem_generations (
  id uuid PRIMARY KEY, run_id uuid NOT NULL REFERENCES council_core.runs(id),
  output_id uuid NOT NULL, generation_no bigint NOT NULL CHECK (generation_no > 0),
  artifact_sha256 char(64) NOT NULL CHECK (artifact_sha256 ~ '^[0-9a-f]{64}$'),
  provisional_report_sha256 char(64) NOT NULL
    CHECK (provisional_report_sha256 ~ '^[0-9a-f]{64}$'),
  status text NOT NULL CHECK (status IN ('SEALED','REVEALED','CLOSED','ABORTED')),
  revealed_event_id uuid, state_version bigint NOT NULL DEFAULT 1,
  UNIQUE(run_id,output_id,generation_no), UNIQUE(run_id,id),
  FOREIGN KEY(run_id,output_id) REFERENCES council_core.integrated_outputs(run_id,id)
);
CREATE TABLE council_core.premortem_submissions (
  id uuid PRIMARY KEY, run_id uuid NOT NULL REFERENCES council_core.runs(id),
  premortem_generation_id uuid NOT NULL, original_seat_no smallint NOT NULL
    CHECK(original_seat_no BETWEEN 1 AND 5),
  scenario_ref text NOT NULL, scenario_sha256 char(64) NOT NULL
    CHECK(scenario_sha256 ~ '^[0-9a-f]{64}$'),
  authored_epoch bigint NOT NULL, submission_event_id uuid NOT NULL,
  UNIQUE(premortem_generation_id,original_seat_no),
  FOREIGN KEY(run_id,premortem_generation_id)
    REFERENCES council_core.premortem_generations(run_id,id),
  FOREIGN KEY(run_id,original_seat_no) REFERENCES council_core.council_seats(run_id,seat_no)
);

CREATE TABLE council_core.integrated_final_packages (
  id uuid PRIMARY KEY, run_id uuid NOT NULL REFERENCES council_core.runs(id),
  output_id uuid NOT NULL, review_generation_id uuid NOT NULL,
  premortem_generation_id uuid NOT NULL,
  artifact_sha256 char(64) NOT NULL CHECK(artifact_sha256 ~ '^[0-9a-f]{64}$'),
  report_sha256 char(64) NOT NULL CHECK(report_sha256 ~ '^[0-9a-f]{64}$'),
  package_sha256 char(64) NOT NULL CHECK(package_sha256 ~ '^[0-9a-f]{64}$'),
  review_disposition_ref text NOT NULL, verification_summary_ref text NOT NULL,
  status text NOT NULL CHECK(status IN ('FROZEN','ACCEPTED','REVISIONS_REQUESTED','REJECTED','ARCHIVED_VERIFIED')),
  state_version bigint NOT NULL DEFAULT 1,
  UNIQUE(run_id,package_sha256), UNIQUE(run_id,id),
  FOREIGN KEY(run_id,output_id) REFERENCES council_core.integrated_outputs(run_id,id),
  FOREIGN KEY(run_id,review_generation_id)
    REFERENCES council_core.integrated_review_generations(run_id,id),
  FOREIGN KEY(run_id,premortem_generation_id)
    REFERENCES council_core.premortem_generations(run_id,id)
);
\`\`\`

**Further required physical constraints, not expressible by standalone CHECKs:**
- A transaction/deferrable same-run invariant must verify the \`output_sha256\` in each review generation equals its \`integrated_outputs.artifact_sha256\`, and the premortem/final package hashes equal the exact referenced output and frozen report. A foreign UUID alone does **not** enforce matching versions. Same-run FK pairing above prevents cross-run references; runtime must validate checkpoint/approval ownership and current generation under lock.
- \`status=EXECUTABLE\` requires *actual* five legitimate current member \`/done\` and closeout receipts, no outstanding required peer actions or verifier work, closed final-comparison checkpoint, and **observed** temporary source/route grant revocation. A SQL CHECK cannot attest to external access removal; store signed/probed broker evidence before advancing.
- \`status=VERIFIED\` requires exact content-hash closure, supported reconstruction/verification observations, safely fenced writes and observed Integrator quiescence (without requiring tests to PASS). An observed artifact is distinct from the protected test verdict.
- \`revealed_event_id\` must remain NULL until the **same transaction** observes count **five distinct original authenticated seats in the current exact generation** and atomically exposes the existing sealed rows to authorized readers. Never reveal sealed bodies through RLS, a retrieval index, message bus, snapshot or SSE beforehand. A duplicate or old-generation review cannot satisfy the fifth.
- \`final_packages.status=ACCEPTED\` requires an actual explicit user acceptance decision bound to \`(package_id,package_sha256,artifact_sha256,report_sha256)\`; update the existing \`acceptance_decisions\` type/target projection rather than creating a new approval service. Archive verification is later and independent. User acceptance of failed/untested requirements needs an explicit approved Contract revision or scoped exception; it never silently flips \`FAILED/NOT_RUN\` to \`PASSED\`.
- Required finalization joins include current review/premortem generations and evidence/reference closure, user authorization, actual archive restore verification, revocation/cleanup and no unresolved consequential operation. **RunCompleted** is not inferred from any one row status.
- Initial implementation should use ordinary B-tree unique/foreign-key indexes above and conditional current-generation guarded updates, not elaborate partitioning or a second distributed lock manager. Preserve prior Step 3 indexes and event-clock-first lock order.

**Existing table refinements rather than duplicate tables:** \`council_core.checkpoint_snapshot_manifests\` gains artifact-kind and purpose-scoped object refs; \`council_runtime.checkpoint_snapshot_access_operations\` gains grant actor/purpose/epoch/observed expiry/revoke; \`council_core.command_receipts\` carries canonical payload hash/expected target and prior reply; \`council_runtime.budget_accounts\` gets the five approved \`scope_kind\` values (\`MEMBER_WORK, CHECKPOINT_COMPARISON, INTEGRATION, POST_INTEGRATION_VALIDATION_PREMORTEM, ORCHESTRATION_REPORT_ARCHIVE\`); \`council_core.acceptance_decisions\` target kind defaults to \`INTEGRATED_FINAL_PACKAGE\` for the current workflow, retaining historical original-candidate decisions. Customer/local archive, moderation policy/decision, transfer receipts, context/continuation, step8 attempts and external operation records reuse already specified Step 3/5 groups. Avoid a new permanent SQL learning database.

## 3. v1 domain command payload and authoritative actor table

These are **selected actual v1 names**, replacing earlier "illustrative command" ambiguity. Each command additionally carries the common envelope, exact relevant target/version/hash and authenticated execution epoch. Required evidence refs are customer-controlled immutable identifiers, not embedded raw source.

| Command (v1) | Only authoritative issuer | Required domain payload; required gate/outcome |
| --- | --- | --- |
| \`RecordMemberReadinessIntent\` | original member, own current seat | \`phase_id, phase_generation, intent_kind=CHECKPOINT_READY|FINAL_INVESTIGATION_CONCLUDED|BLOCKED, candidate_or_evidence_manifest, member_rationale_ref, incomplete_flags\`; authors intent, **not** accepted readiness |
| \`VerifyMemberReadiness\` | trusted backend after mechanics | \`readiness_intent_id, observed_manifest_sha256, broker_evidence_ref, observed_quiescence_ref, contract_revision\`; only legitimate verified intent adds a current five-seat arrival; unproven claims stay PENDING/BLOCKED |
| \`SubmitFinalInvestigationOutcome\` | original member | \`phase_generation, outcome=VIABLE_CANDIDATE|CONCLUDED_NO_VIABLE_CANDIDATE, exact_manifest_sha256, evidence_ref, limitations_ref\`; negative conclusion allowed as real **investigation** outcome only under approved final intake, not earlier software milestone |
| \`RecordCouncilPosition\` | original member during correct phase | \`decision_id, alternatives[], position, prior_position_id?, rationale_ref, source_refs[], unresolved_objections[], version\`; pre-discussion positions sealed if applicable; member cannot author another seat's view |
| \`FreezeIntegrationBlueprint\` | trusted backend after genuine member material | \`blueprint_id, expected_draft_revision, exact_contract_revision, current_five_final_outcome_ids, exact_decision_register_hash, source_manifest_sha256\`; DRAFT->FROZEN hash pin; no Integrator admission |
| \`VerifyBlueprintExecutableHandoff\` | trusted backend after observed closure | \`blueprint_id, final_comparison_generation, five_closeout_ids, current_frontier_sha256, observed_revocations[]\`; only actual complete normal closeout and observed revocation -> EXECUTABLE |
| \`AdmitFinalIntegrator\` | trusted backend under existing user authorization | \`blueprint_id, final_integrator_id, current_epoch, workspace_ref, new_approved_source_grant_refs[], budget_policy_version, integration_scope_id, protected_review_scope_id\`; distinct source/grant/budget, no original seat |
| \`SubmitIntegratorOutputReadyIntent\` | non-voting Integrator | \`blueprint_id, artifact_kind, proposed_artifact_ref, proposed_sha256, exact_source_refs[], limitations_ref\`; intent only; cannot set VERIFIED |
| \`VerifyIntegratedOutput\` | trusted backend | \`output_intent_id, observed_artifact_hash, verified_source_closure_ref, fenced_writer_evidence_ref, quiesced_resource_evidence_ref, external_effect_reconciliation_refs[], check_summary_ref\`; actual pin -> VERIFIED (PASS of tests still independent) |
| \`OpenIntegratedReviewGeneration\` | trusted backend | \`output_id, exact_artifact_sha256, impact_scope, impact_evidence_ref?, approved_five_recipient_snapshot_grants[]\`; first version FULL; later DELTA only with closure proof; opens SEALED review after observed grant |
| \`SubmitIntegratedReview\` | **one of original five seats** | \`review_generation_id, exact_output_sha256, scope, assessment_ref, assessment_sha256, findings_ref\`; one immutable submission per authentic seat/generation; never Integrator |
| \`RevealIntegratedReviews\` | trusted backend only | \`review_generation_id, expected_state_version\`; five genuine same-generation submissions and atomic reveal; no inferred endorsement |
| \`CloseIntegratedReview\` | trusted backend only | \`review_generation_id, five_current_done_closeout_refs[], observed_revocation_refs[], unresolved_findings_ref\`; closure must be observed before authorizing Integrator's next writable revision |
| \`OpenPremortemGeneration\` | trusted backend after review/report freeze | \`output_id, exact_artifact_sha256, provisional_report_sha256, required_impact_scope\`; separate sealed generation/pair |
| \`SubmitPremortemScenario\` | original member | \`premortem_generation_id, exact_artifact_sha256, exact_report_sha256, scenario_ref, scenario_sha256\`; hypothetical scenarios, not observed future facts |
| \`RevealPremortem\` | trusted backend | \`premortem_generation_id\`; five real sealed submissions, one atomic reveal |
| \`FreezeIntegratedFinalPackage\` | trusted backend/editorial assembly only | \`output_id, review_generation_id, premortem_generation_id, report_ref, report_sha256, verification_summary_ref, limitations_ref, manifest_sha256\`; exact current hashes+dispositions, immutable user-review target |
| \`AcceptCandidate\` / \`RequestCandidateRevisions\` / \`RejectCandidate\` / \`CancelFinalization\` | authenticated **user** via existing Interaction Center | \`target_kind=INTEGRATED_FINAL_PACKAGE, package_id, package_sha256, artifact_sha256, report_sha256, expected_state_version, decision\`; never silently accept an original member candidate as integrated output |
| \`RecordArchiveValidation\` | trusted backend after external probe | \`final_package_id, archive_manifest_sha256, customer_destination_ref, restore_validation_ref, reference_closure_ref, observed_revocation_cleanup_ref, outstanding_effects_status\`; archive is separate observed fact |
| \`CompleteRun\` | trusted backend only | \`final_package_id, accepted_user_decision_id, verified_archive_validation_id, cleanup_evidence_ref, actual_check_status_summary\`; only after all mandatory contractual gates, no fabricated successes |

A **materially changed** output/report requires a new immutable generation and affected test/review/premortem invalidation. The Integrator never opens its own review nor consumes a protected reviewer fund. A genuinely no-viable investigation remains evidence that informs the Blueprint; a final completed software product must still satisfy its explicit contract or a user-approved revision.

## 4. Guard, lock, event and external-effect transactions (normative)

1. **Authentication first**: validate trusted session/actor type, current scope/permission/policy/egress, target run, session epoch and command envelope. Then look up the scoped \`(actor,command_type,idempotency_key)\` receipt and canonical payload hash: identical replay returns prior receipt **even if the aggregate has since advanced**; conflicting key/hash rejects. A formerly authorized result replay does not reveal content to a now-unauthorized caller: authorize access to the *returned content* again before displaying it.
2. **Canonical lock order** for new state changes: \`deployment_event_clock FOR UPDATE\` first, then \`run\`, \`checkpoint/blueprint/integrated_output/review_generation or premortem_generation\`, then five protected budget accounts in deterministic ID order (and member/phase accounts as applicable), then operation row. Never reverse across command types. Assign event position only in the committing transaction by updating the clock row; one transaction may commit multiple consecutively allocated positions. Outbox/event + canonical aggregate + scoped idempotency receipt + budget reservation + external operation **intent** commit atomically.
3. **External side effects after commit**: trusted broker/model/Git/artifact/Docker dispatch from existing outbox/operation ledger. Statuses \`PREPARED -> DISPATCHED -> SUCCEEDED|FAILED|UNKNOWN_PENDING_RECONCILIATION\`; a timeout/lost reply cannot be guessed SUCCEEDED or non-billed. Repeated consequential effect reuses provider idempotency token where supported and probes external truth *before* unsafe retry. Refund only a proven non-dispatch or settled credit, not an elapsed timeout.
4. **Generation locking**: when a member submits review, lock the current review/premortem generation row, verify signed actor/seat 1–5, exact target hash, allowed SEALED phase and proper impact scope. INSERT with \`UNIQUE(generation,seat)\`; same-key/hash returns receipt; different payload rejected. Under **the same lock/transaction**, if the newly committed cohort now contains five distinct genuine seat rows, insert the unique reveal event and change visibility once. A recipient without reveal authorization receives no assessment text, text indexing or cached references.
5. **Blueprint closure**: \`FreezeIntegrationBlueprint\` may commit FROZEN while separate revocation operations are pending; \`VerifyBlueprintExecutableHandoff\` requires all-five current closeouts, no open /work or peer obligations, verified gateway closure and **observed** broker revoke evidence recorded after effect. A timed-out revoke is UNKNOWN and blocks admission. Any newly accepted required action before closure invalidates stale \`/done\`/freeze-gate frontier and requires correct reversioning, not silent overwritten state.
6. **Output closure**: result-ready intent can be inserted without result verification. Only trusted observer can mark exact immutable artifact VERIFIED after fencing all writable actors, actual source/ref hashes, quiescence, relevant external effect reconciliation and conservation of approved budget. A verification check with FAIL/NOT_RUN remains truthfully failed/not run.
7. **Version invalidation**: current target pointer changes **under same versioned run/target lock**. Previous reviews and PASS observations remain historical; affected checks become STALE/NOT_RUN for new output. DELTA only with recorded mechanical dependency closure + reviewer-verifiable semantic impact evidence, otherwise FULL. Review closure and physical grant revoke precede writable same-Integrator revision.
8. **Final acceptance and archive**: \`AcceptCandidate\` must bind the exact FROZEN package hash, user identity and project contract, with review/premortem gates and actual check results/waivers disclosed. If required checks are unsatisfied without authorized scope change, do not emit \`CompleteRun\`. The customer archive/export is an external effect requiring fresh-checkout/restore, reference-closure and revocation validation before any destructive cleanup or COMPLETED state.
9. **Read model/SSE**: event position is **committed canonical** ordering, not a PostgreSQL sequence or clock timestamp; consistent snapshot + cursor replay closes reconnect races. Outbox can retry/reorder delivery but consumers deduplicate immutable event IDs and re-read canonical run-filtered state. Sealed content never enters authorization-inappropriate projections, logs, RAG or public/optional repo exports.

## 5. Verified source/permission/moderation decision boundary

- Deterministic allowlisted tools, authenticated grants, sandbox/network rules, user-approved egress, BYOK scoped credentials and data retention are **independent** enforcement gates.
- The **hosted OpenAI Moderation API** (subject to customer approval and current documented text/image capabilities) returns moderation flags/categories/scores. It does **not** execute customer-defined policies, guarantee detecting exfiltration, prove permission or inspect arbitrary code/binary safety. Local backend combines provider result + explicit deterministic policy into \`ALLOW|BLOCK|REQUIRE_USER_REVIEW|UNAVAILABLE\`; no invented arbitrary moderation-model commands or local GPT-OSS moderation requirement. A missing permitted external service or customer egress consent makes new affected guarded operations \`BLOCKED\`, while unrelated purely local deterministic state may continue as allowed.
- Persist versioned limited audit receipt: \`run_id, actor_scope, command_id, content_sha256, data_class, provider, moderation_model_version, category_flags, policy_version, deterministic_enforcement_result, consent_ref, observed_at\`. Do **not** log secret/raw file payloads; a BYOK credential is not permission to transmit confidential data.
- Snapshot-read grants are immutable-purpose object+recipient scopes with broker observed ACTIVE/REVOKED separate from SQL intent. Expiry denies new reads but does not prove physical revoke; inherited reads across generations are forbidden. For external host actions, privilege escalation uses a separate customer-approved broker, never agent Docker-socket access.

## 6. Test-design / execution status

The required scenario matrix is in [Step 2–8 verification matrix](STEP_2_TO_8_VERIFICATION_MATRIX_V1.md). Design-time schema checks, static cross-file assertions and peer review can confirm **document consistency only**. The SQL above and commands are **precise reference contracts**, not applied migrations or a generated API. Actual PostgreSQL transactions, RLS, containers, provider calls, external access-probe outcomes, concurrency races, failure injection and model comparisons remain **NOT IMPLEMENTED / NOT RUN**. Completion of this contract closes design ambiguity, not implementation evidence.
