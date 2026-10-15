# Documentation publication verification

This record concerns the documentation, not verification of the proposed application.

## Checks performed

- The complete design contains numbered sections 1 through 18.
- Relative documentation links and local heading anchors resolve in the prepared publication files.
- The remote Git tree was read after uploading the core documents. The Git blob hashes below matched the corresponding prepared export files exactly.
- The owner-created remote repository history was preserved. No force-push or repository recreation was performed.
- No earlier single-lead runtime, dashboard image, private evidence collection, credentials, or application dependencies were imported.

| File | Verified Git blob hash |
|---|---|
| `AGENTS.md` | `265f8a6fb3e940a686b8fc1c9cf21d6d4dd3967a` |
| `docs/APP_DESIGN.md` | `5a6ad97e389e10fb24e7e48239c96284fe12ed78` |
| `docs/IMPLEMENTATION_HANDOFF.md` | `202f500a5fbac3c7c4b74d5437db3ec15d79f996` |
| `docs/REFERENCES.md` | `d69d9bf8be6f88d2bfed30e5730d5eaac93633f9` |

Publication-specific notes in README, PUBLISHING, and this file were updated from the earlier offline export to reflect the actual remote publication. The approved design and handoff were not rewritten. Repository hygiene files and the retained helper use normalized text line endings in Git.

## Not performed

No model API calls, agent execution, application implementation, database or sandbox integration tests, application tests, or deployment were performed. The acceptance tests in the design are requirements, not passing test results.

The retained PowerShell new-repository helper was not executed or used to publish this repository. It is not needed to use the already published documentation.

No project license was selected, and no third-party implementation was copied.

## October 13 architecture correction verification scope

`python3 tools/check_specs.py` checks the machine-readable contract, explicit pending runtime statuses, removal of selected contradictory defaults, and local documentation links. `git diff --check` checks patch whitespace. These are documentation checks, not application tests.

The required runtime scenarios in docs/ARCHITECTURE_DECISIONS.md remain NOT RUN: single-slot fairness, all-five barriers, visibility failures, sealed review isolation, hostile peer-test containment, unknown external effects, reservation races, committed event replay, stale /done races, clarification isolation, and archive reference closure. Provider integration, sandbox integration, database migrations, live experiments, and deployment have not been verified by this update.

Do not mark implementation or runtime verification complete from a passed documentation check or a pushed commit.

## October 14 Step 7 design verification boundary

The Step 7 **specification** is marked DESIGNED. The latest Part 7 document, MVP scope, main design, implementation handoff, Part 3 schema proposal, Part 4 command/event/state interfaces, Part 5 transaction contract, architecture decisions, machine-readable contract, README, and agent instructions now carry the same approved budget/resource/recovery policies.

The repository's static-check script was updated to reject the superseded mandatory-private-work-slice assumption, check the Step 7 DESIGNED boundary without treating it as implementation, and recognize ADR-13 (BYOK). This record **does not claim that the script was executed in a complete local checkout** as part of this connector-based edit; no passing check output is invented.

**Runtime implementation, PostgreSQL migrations, provider/model integrations, Docker containment/recovery tests, concurrent budget tests, and repeated Council evaluations remain NOT STARTED / NOT RUN.** The acceptance checklist in Part 7 is a test plan only. Historical original-publication blob hashes above describe the earlier publication snapshot and are not current file hashes.


## October 14 Steps 3–5 specification reconciliation

Part 3 (PostgreSQL data), Part 4 (typed commands/events/state), and Part 5 (transactions/idempotency/UNKNOWN handling) have been reconciled and marked **DESIGNED at specification level**, not implemented.

Historical October 14 cross-document design assertions checked by connector read-back included five fixed member seats; the **then-approved, now SUPERSEDED** internet-public GitHub exposure/private-closure protocol; all-five sealed reviews and version-bound /done; branch-local scope; ephemeral BYOK credential references; user budget policies and pre-dispatch reservations; one locked transactional event clock; idempotency replay preceding stale-target checks; unknown external effects retaining outstanding reservations; and verified Git reference closure before deletion of the project-lifetime Council database. Corresponding implementation/test statuses stay **NOT STARTED / NOT RUN**.

The repository's `tools/check_specs.py` was extended to assert these invariants, but this entry **does not claim that the script ran in a complete local checkout**. Connector read-back and static text/JSON consistency are not PostgreSQL migrations, deployed security controls, executed failure-injection tests, live provider requests or an implemented Council runtime.

The October 13 publication blob hashes above refer to the original publication snapshot and are not current content hashes.

## October 14 Step 8.1 design verification boundary

The new `docs/PART_8_AGENT_LOOP_EXPERIMENTATION_DELEGATION.md` captures the **owner-approved optional** Karpathy-style experiment cycle inside each Council member's ordinary agentic loop. The Step 8 roadmap, complete app design, handoff, architecture decision ADR-14, machine-readable contract, Part 3 experiment/provenance hooks, README, and agent instructions were aligned. The machine-readable Step 8 status remains **IN_DESIGN**, while Step 8.1's accepted subdecision is recorded separately.

A source/design consistency read-back is documentation verification only; the repository's `tools/check_specs.py` assertions were updated but are **not claimed executed** in a full checkout as part of these remote file edits. No model calls, durable agent experiments, worker execution, benchmark, sealed-review test, token accounting verification, or application implementation was run. **Runtime implementation NOT STARTED; tests NOT RUN.**

## October 14 Step 8.2 worker monitoring specification verification

The owner accepted **sandbox-local worker count/depth autonomy** subject to aggregate sandbox resources, branch security and parent-approved BYOK model budgets. The existing five-member whole-sandbox scheduler remains authoritative; worker processes are not newly counted as Council seats or separately scheduled. No raw Docker Engine socket reaches agent-controlled sandboxes.

The approved monitoring design uses a small trusted **external** Council component consuming Docker Engine container stats, OOM/die lifecycle events, and supported Docker/cgroups CPU/memory/PID constraints. Proposed initial configurable telemetry/pressure defaults are **2–5 second sampling**, alerts/restricted new brokered heavyweight work near **80%** of assigned container RAM and stronger limits/safe whole-sandbox suspension near **90%**. Observe host/WSL2 VM RAM, disk/volumes and optional GPU/VRAM separately. These defaults are **not a crash-prevention guarantee**, and missing telemetry does not certify safe capacity. OOM and stale external effects follow existing recovery/fencing/reconciliation rules.

Updated specifications include Parts 7 and 8, the MVP Steps 7/8/10 roadmap, app design, implementation handoff, Part 3 transient telemetry/durable resource incidents, Part 4 resource incident events, ADR-15 and machine-readable architecture contract, official Docker/NVIDIA source references, README and agent instructions. The static specification checker was **updated**, but **not executed as a complete checked-out repository test** in this connector-based update. A connector read-back consistency review is not equivalent to a running Docker Engine monitor, Windows WSL2 verification, GPU/VRAM support, real container-limit enforcement, or crash/failure-injection test.

**Statuses:** Step 7 DESIGNED; Step 8 **IN DESIGN** (worker/resource and Docker-persistence subdesigns approved; final member phase/termination and action protocols still open); Step 10 PARTLY DESIGNED. Runtime implementation and all resource-monitor, worker and recovery tests **NOT STARTED / NOT RUN**.

## October 14 Step 8.2a Docker worker-persistence design verification

The owner approved native **Docker named-volume/authorized bind-mount preservation of member-owned workspace and locally written worker results** rather than an additional Council worker-recovery manager. Docker restart creates a fresh process and does **not** restore in-memory worker execution; the parent member is responsible for resuming/repeating subtasks from its own saved files. Named volume identity/mount scope stays bound to the correct logical member, and intentionally stopped checkpoint-ready, PAUSED or BUDGET_EXHAUSTED sandboxes cannot bypass Council's whole-member admission schedule via unrestricted automatic restart policies.

Updated the Part 7/8 specifications, Step 7/8/10 MVP scope, app design, handoff, ADR-16, machine-readable contract, official Docker storage/restart references, README and agent instructions; static-check assertions were updated as a specification consistency aid. Existing canonical external-operation/UNKNOWN reconciliation, budget caps, member checkpoint status, provenance and final archive/volume deletion guards remain authoritative.

**Verification boundary:** Remote repository read-back is **documentation consistency only**. The static checker was modified but not run in a complete local checkout; no Docker named-volume restore, container restart/stop behavior, protected mount isolation, resource headroom, provider replay, or Council runtime acceptance test was executed. **Step 8 remains IN DESIGN** for member phase/final readiness transitions and precise action/observation behavior. Runtime implementation **NOT STARTED**, tests **NOT RUN**.

## October 14 customer-local repository and contextual memory amendment

Owner-approved ADR-17 replaces the formerly internet-public GitHub checkpoint policy with customer-controlled native Git, selected hash-verified read-only local checkpoint snapshots, and independently verified temporary peer access grants/revocations. ADR-18 requires **success-first historical retrieval** and treats FAILED/INCONCLUSIVE approaches as **context-specific caution/test evidence**, not automatically banned solutions for similar problems. Customer-derived general lessons can reach a vendor/shared library only through separate, specific, informed customer permission and privacy/IP/license review.

Design changes have been committed to the repository's canonical [local repository/memory specification](docs/LOCAL_REPOSITORY_AND_KNOWLEDGE_RETENTION.md), decision log, machine contract, roadmap, app design, gateway/authority contracts, database/typed/transaction specifications, agent-loop spec, handoff, README, and instructions. Steps 2–5 are **REOPENED IN DESIGN** for the replacement sharing, consent and retention interfaces. Their previously designed unrelated event/lease/budget/agent invariants remain specified. Step 11 is still IN DESIGN. These are specifications, not executed security controls.

**Verification boundary:** Connector read-back and text/contract consistency checks are not equivalent to running `tools/check_specs.py` on a complete checkout or executing runtime/adapters/migrations. No vendor/customer code was obtained as part of this update. **Implementation NOT STARTED, runtime tests NOT RUN.**

## October 15 Step 2 v1 interface proposal verification

Inspection baseline: `3f5a109b22128b25370a96abaf63ad8a80df9d5f`. The existing Step 2 record now contains a **PROPOSED / REQUIRES OWNER APPROVAL** interface specification for discovery, immutable manifests, permitted tree/file/artifact reads, checkpoint grants, bounded transfers and receipts, shared closing fences and observed revocation. Parts 3–5, the communication gateway and implementation handoff link to that proposal. Existing approved architecture and machine-readable step statuses are preserved; no additional approved ADR or implemented schema is asserted.

Executed locally: `python3 tools/check_specs.py` against the repository specification documents and referenced files retrieved from the baseline. Result: **passed, 18 documents and 18 tracked requirements**; amendment status checks passed with no runtime requirement marked completed. Review also checked S2-01–S2-16 coverage, current-read checks on receipt replay, sealed-assessment visibility, complete five-snapshot/20-directed-grant activation, and canonical versus externally applied fence ordering. This is documentation review and the existing static consistency check, not executable validation of the proposed DTOs or acceptance cases.

**Proposal approval: PENDING. Step 2 and affected Steps 3–5: REOPENED IN DESIGN. Application implementation: NOT STARTED. Runtime acceptance/failure-injection tests and evaluations: NOT RUN.** Real SQL authorization/concurrency, Git export filtering, transfer/restart behavior, container/service route revocation, data-egress and filesystem enforcement require implementation and recorded runtime evidence before completion claims.

