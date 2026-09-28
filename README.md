# Council

**Status: approved design; application not implemented.**

Council is a general-purpose, evidence-grounded investigation platform governed by peer agents. Each council member develops its own analysis using workers, challenges other members' findings, revises its position when justified, and contributes to a traceable result.

DeepSeek is the initial default for every agent. Per-agent provider/model selection remains part of the design so mixed-model councils can be enabled later.

## Start here

- [Complete app design](docs/APP_DESIGN.md) - the authoritative approved product and architecture specification, including the complete UI, graph, context lifecycle, execution boundaries, and acceptance criteria.
- [PostgreSQL data model](docs/POSTGRES_DATA_MODEL.md) - the authoritative Part 3 persistence model and invariants.
- [Typed interaction/state contracts](docs/TYPED_INTERACTION_CONTRACTS.md) - the approved Part 4 design linking every meaningful state to runtime behavior, user surfaces, commands, events, transitions, and recovery.
- [Implementation handoff](docs/IMPLEMENTATION_HANDOFF.md) - scope boundaries, build sequence, invariants, and instructions for a later authorized implementation.
- [Agent instructions](AGENTS.md) - repository-level requirements for future development agents.
- [Design references](docs/REFERENCES.md) - upstream concepts and documentation referenced in the design.
- [Publication record](PUBLISHING.md) - the GitHub publication status and the role of the legacy export helper.
- [Verification record](VERIFICATION.md) - documentation integrity checks and their limits.

## The three defining graph questions

1. Which conclusions depend on a particular source or assumption?
2. Which challenge caused a claim to be narrowed?
3. Which apparently independent findings came from the same underlying evidence?

The graph answers these from recorded actions, source lineage, claim versions, attributed interpretations, and explicit revision decisions. It is not a generated retrospective story.

## Architectural commitments

Peer council, not a single intellectual leader. A separate Project Orchestrator converts user conversation into an approved versioned Project Contract, neutral council instructions, and a project-specific communication-checkpoint policy without becoming a solution supervisor. The user does not directly guide individual council members. Domain-agnostic investigators remain private between scoped checkpoints, then cross-examine published work when policy allows it. Evidence support is recorded separately from agreement. Persistent logical agents use replaceable bounded sessions, a runtime-recorded provenance graph, search, compaction, and a mandatory simulated six-month-plus premortem before fully reviewed finalization.

For executable projects, the default is a Council-managed reproducible container environment that agents may evolve as needed; matching the user's existing machine is optional rather than the default. The proposed stack is React/TypeScript/React Flow, Python/FastAPI/Pydantic, LangGraph, PostgreSQL, versioned artifact storage, and restricted container execution when enabled. This repository contains no implementation or dependency pins yet.

## Current contents and verification boundary

This repository contains Markdown specifications, repository hygiene files, and a retained PowerShell **new-repository publishing helper only**. The helper is not application code. There is no agent runtime, dashboard implementation, deployed service, or passing application test suite here.

The design does not assert that councils outperform strong single agents or that graph-assisted continuation eliminates context limits. Both are evaluation hypotheses.

The earlier single-lead swarm prototype is deliberately excluded. It is not the implementation baseline for this council design.

## Repository and publication

Published to **`kstecrypto-hub/council`**, branch **`main`**, in the private repository created by the owner. The design and supporting records were committed through the connected GitHub file operations. These commits preserve the existing repository history; they are not the earlier archive's local commit.

The full 18-section specification is in `docs/APP_DESIGN.md`. Application implementation has not been authorized by this publication request.

`publish.ps1` is retained from the earlier offline export for a separately authorized new-repository publication. It is not required for this repository and must not be run to recreate `kstecrypto-hub/council`. See `PUBLISHING.md`.

No project license has been selected. No upstream implementation is vendored by this revision. Inspect relevant upstream licenses and preserve required notices before any later code reuse.
