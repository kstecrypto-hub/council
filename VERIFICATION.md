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
