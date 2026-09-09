# Council

**Status: approved design; application not implemented.**

**This branch: `design/code-level-implementation`.** It adds the approved code-level implementation proposal and a component-by-component review agenda. These changes are documentation only; the original approved product design is preserved. New refinements proposed during review are not automatically approved architecture.

Council is a general-purpose, evidence-grounded investigation platform governed by peer agents. Each council member develops its own analysis using workers, challenges other members' findings, revises its position when justified, and contributes to a traceable result.

DeepSeek is the initial default for every agent. Per-agent provider/model selection remains part of the design so mixed-model councils can be enabled later.

## Start here

- [Complete app design](docs/APP_DESIGN.md) - the authoritative approved product and architecture specification, including the complete UI, graph, context lifecycle, execution boundaries, and acceptance criteria.
- [Code-level implementation plan](docs/CODE_IMPLEMENTATION_PLAN.md) - all 15 approved implementation sections: modules, database records, typed commands, transactions, graph queries, queue behavior, agent loops, providers, context, API/UI, and testing. Code snippets are illustrative, not an implemented application.
- [Component review agenda](docs/COMPONENT_REVIEW_PLAN.md) - ordered, one-part-at-a-time analysis, beginning with application structure and process boundaries.
- [Implementation handoff](docs/IMPLEMENTATION_HANDOFF.md) - scope boundaries, build sequence, invariants, and instructions for a later authorized implementation.
- [Agent instructions](AGENTS.md) - repository-level requirements for future development agents.
- [Design references](docs/REFERENCES.md) - upstream concepts and documentation referenced in the design.
- [Publication record](PUBLISHING.md) - the original GitHub publication status and the role of the legacy export helper.
- [Verification record](VERIFICATION.md) - original documentation integrity checks and their limits; this is not an application test report.

## The three defining graph questions

1. Which conclusions depend on a particular source or assumption?
2. Which challenge caused a claim to be narrowed?
3. Which apparently independent findings came from the same underlying evidence?

The graph answers these from recorded actions, source lineage, claim versions, attributed interpretations, and explicit revision decisions. It is not a generated retrospective story.

## Architectural commitments

Peer council, not a single intellectual leader. Domain-agnostic investigators, not coding-only agents. Independent initial investigations followed by targeted cross-examination. Evidence support recorded separately from agreement. Persistent logical agents with replaceable bounded sessions. A runtime-recorded, agent-annotated provenance graph alongside checkpoints, search, and compaction. A mandatory simulated six-month-plus premortem before fully reviewed finalization.

The proposed stack is React/TypeScript/React Flow, Python/FastAPI/Pydantic, LangGraph, PostgreSQL, versioned artifact storage, and optional restricted Docker execution. This repository contains no implementation or dependency pins yet.

## Current contents and verification boundary

This repository contains Markdown specifications, repository hygiene files, and a retained PowerShell **new-repository publishing helper only**. The helper is not application code. There is no agent runtime, dashboard implementation, deployed service, or passing application test suite here.

The design does not assert that councils outperform strong single agents or that graph-assisted continuation eliminates context limits. Both are evaluation hypotheses.

The earlier single-lead swarm prototype is deliberately excluded. It is not the implementation baseline for this council design.

## Repository and publication

The original design was published to **`kstecrypto-hub/council`**, branch **`main`**, in the private repository created by the owner. The design and supporting records were committed through the connected GitHub file operations. These commits preserve the existing repository history; they are not the earlier archive's local commit.

The current documentation branch was created from `main` at `8f86db522b377f10eab79a2e75b11dc97ada7b86`. It adds `docs/CODE_IMPLEMENTATION_PLAN.md`, `docs/COMPONENT_REVIEW_PLAN.md`, and this navigation update. No application implementation or merge to `main` is part of this branch-publication request.

The full 18-section specification remains in `docs/APP_DESIGN.md`.

`publish.ps1` is retained from the earlier offline export for a separately authorized new-repository publication. It is not required for this repository and must not be run to recreate `kstecrypto-hub/council`. See `PUBLISHING.md`.

No project license has been selected. No upstream implementation is vendored by this revision. Inspect relevant upstream licenses and preserve required notices before any later code reuse.
