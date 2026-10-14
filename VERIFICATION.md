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

Cross-document design assertions checked by connector read-back include: five fixed member seats; separately approved internet-public GitHub publication and observed private closure; all-five sealed reviews and version-bound /done; branch-local scope; ephemeral BYOK credential references; user budget policies and pre-dispatch reservations; one locked transactional event clock; idempotency replay preceding stale-target checks; unknown external effects retaining outstanding reservations; and verified Git reference closure before deletion of the project-lifetime Council database. Corresponding implementation/test statuses stay **NOT STARTED / NOT RUN**.

The repository's `tools/check_specs.py` was extended to assert these invariants, but this entry **does not claim that the script ran in a complete local checkout**. Connector read-back and static text/JSON consistency are not PostgreSQL migrations, deployed security controls, executed failure-injection tests, live provider requests or an implemented Council runtime.

The October 13 publication blob hashes above refer to the original publication snapshot and are not current content hashes.

## October 14 Step 8.1 design verification boundary

The new `docs/PART_8_AGENT_LOOP_EXPERIMENTATION_DELEGATION.md` captures the **owner-approved optional** Karpathy-style experiment cycle inside each Council member's ordinary agentic loop. The Step 8 roadmap, complete app design, handoff, architecture decision ADR-14, machine-readable contract, Part 3 experiment/provenance hooks, README, and agent instructions were aligned. The machine-readable Step 8 status remains **IN_DESIGN**, while Step 8.1's accepted subdecision is recorded separately.

A source/design consistency read-back is documentation verification only; the repository's `tools/check_specs.py` assertions were updated but are **not claimed executed** in a full checkout as part of these remote file edits. No model calls, durable agent experiments, worker execution, benchmark, sealed-review test, token accounting verification, or application implementation was run. **Runtime implementation NOT STARTED; tests NOT RUN.**
