# Council

**Status: approved design; application not implemented.**

Council is a general-purpose, evidence-grounded investigation platform governed by peer agents. Each council member develops its own analysis using workers, challenges other members' findings, revises its position when justified, and contributes to a traceable result.

DeepSeek is the initial default for every agent. Per-agent provider/model selection remains part of the design so mixed-model councils can be enabled later.

## Start here

- [Complete app design](docs/APP_DESIGN.md) - the authoritative approved product and architecture specification, including the complete UI, graph, context lifecycle, execution boundaries, and acceptance criteria.
- [PostgreSQL data model](docs/POSTGRES_DATA_MODEL.md) - the authoritative Part 3 persistence model and invariants.
- [Part 5 transactions](docs/PART_5_TRANSACTIONS_IDEMPOTENCY_CONFLICTS.md) - transactional event ordering, idempotency, external effect reconciliation and budget-operation contracts.
- [Step 7 execution and budget design](docs/PART_7_MEMBER_SCHEDULING_RECOVERY_RESOURCES.md) - approved sandbox scheduling, user-budget, model-concurrency, recovery, and pause/stop specification.
- [Step 8 member loop and experiments](docs/PART_8_AGENT_LOOP_EXPERIMENTATION_DELEGATION.md) - accepted optional Karpathy-style experiment cycle inside the autonomous member loop; Step 8 overall remains in design.
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

**October 15 Step 2 owner-approved subdesign:** Generated member Git repos are temporary and **customer/company-owned native local Git**, never vendor-hosted by default. At checkpoints the trusted customer-local snapshot service exposes only selected immutable read-only snapshots via the narrow IRC-inspired checkpoint bridge; larger artifacts use bounded verified transfers, not chat context dumps. Access closes with checkpoint communication and is independently verified revoked. Accepted output goes only to a customer-approved destination; provider/tool egress needs separate authorization. See [Step 2 customer Git and checkpoint record](docs/STEP_2_CUSTOMER_LOCAL_GIT_CHECKPOINT.md). **Step 2 remains IN DESIGN; implementation NOT STARTED, tests NOT RUN.**

**October 15 Steps 3–5 unified-trust approval:** One customer-controlled modular trusted application coordinates PostgreSQL, the Orchestrator, runtime/operation worker, and IRC-inspired command gateway, with separate restricted Docker/host and snapshot authorities. **hosted OpenAI Moderation API** performs policy-based *semantic* checks on authorized exchanges in addition to deterministic permissions/network restrictions; a model verdict never grants capabilities or replaces technical isolation. Members use only typed commands to request/receive approved frozen checkpoint data, with no arbitrary peer file selection/upload/send/attachment and no file response followed by an automatically attached chat message. Source bytes are resolved and delivered solely by the trusted snapshot service. Complete [Steps 3–5 deployment architecture](docs/STEPS_3_TO_5_DEPLOYABLE_ARCHITECTURE_2026_10_15.md) records ADR-19/20/21. The project remains a complete **evidence-grounded five-member research/engineering Council**, not a generic group-chat swarm. **Architecture review only: Steps 3–5 remain IN DESIGN; no implementation or tests.**

> **Correction ADR-22:** Use hosted [OpenAI Moderation API](docs/OPENAI_MODERATION_API_CORRECTION.md), **not** a local GPT-OSS safeguard. The free API requires credentials/internet and company-approved data egress; deterministic permission and sandbox controls remain mandatory. This later correction supersedes any inconsistent older safeguard wording. No implementation or testing.

## Architecture review update - October 13, 2026

The approved corrections are integrated into the current design documents. See [decision/status index](docs/ARCHITECTURE_DECISIONS.md) and [machine-readable contract](docs/architecture_contract.json).

**SUPERSEDED PUBLIC CHECKPOINT RULE (ADR-17):** Generated member Git repositories remain within customer-controlled infrastructure. At approved checkpoints, the local gateway shares only selected, immutable, read-only pinned snapshots with authorized peers; internet-public publication is not required or the default. Council has five fixed logical members, sealed independent reviews, isolated peer testing, semantic phases with user-approved token/cost budgets (not mandatory periodic private-work slices), and explicit recovery/accounting/completion boundaries.

**Application implementation: NOT STARTED. Runtime acceptance tests and comparative evaluations: NOT RUN.** Steps **2, 3, 4 and 5 were previously DESIGN-CLOSED under a now-superseded public-GitHub assumption and are REOPENED IN DESIGN only for local checkpoint/tenant-controlled retention interfaces.** Their stable database, typed-authority, transactional event-ordering and budget rules remain specified. Step 6 and 7 have their existing design status. Step 7 specifies user-approved 70/25/5 suggested budget allocation, BYOK/local-LLM billing, resource admission and recovery. Their executable migrations, providers, sandbox integrations and tests are not complete. Steps 8–15 still contain design work and/or follow-on validation.

**Step 8.1 accepted (October 14):** Each independent member may optionally run a controlled `hypothesis -> change/alternative -> test/check -> observe -> keep/revise/discard/inconclusive -> record` experiment under its existing ACT action. Preserve exact baselines, failures and evidence for peer challenge; no forced experiment count, automatic quality judge, global metric or extra scheduler. Authorized workers operate under parent branch/budget; checkpoint `/work` remains read-only verification. The internal worker freedom/persistence policy has since been approved in Steps 8.2/8.2a; Step 8 still needs remaining member-loop/finalization details. **No application implementation or runtime tests were performed.**

**Step 8.2 worker/resource policy accepted (October 14):** Each member may create unlimited numbers and nesting depths of sandbox-local worker agents/processes **within its single authorized Docker sandbox**. There is no Council-wide internal-worker scheduler or worker-count/depth cap. Workers share the sandbox's aggregate CPU/RAM/PIDs/storage/approved GPU capabilities and parent's BYOK phase budget; no agent receives Docker daemon access. A small trusted monitor reads Docker Engine stats and OOM/lifecycle events **outside sandboxes**, applies configurable initial 2–5s polling with 80%/90% memory-pressure responses to **new brokered heavy work**, and enforces supported container limits through Docker/cgroups. Host/WSL2 RAM, free disk/volumes, and optional GPU/VRAM need separate observation. Thresholds **do not guarantee crash prevention**; unsafe or OOM outcomes go through existing durable recovery. See [Part 8 worker autonomy](docs/PART_8_AGENT_LOOP_EXPERIMENTATION_DELEGATION.md), [Part 7 monitoring](docs/PART_7_MEMBER_SCHEDULING_RECOVERY_RESOURCES.md), and [backend references](docs/REFERENCES.md).

**Step 8.2a worker persistence approved (October 14):** each logical member's Docker **named volume** (or approved persistent bind mount) retains its private workspace and worker-written progress/results across stopped or recreated containers. Worker processes and in-memory state do **not** automatically resume on restart; the member decides how to restart/repeat its own local subtasks from saved files. Council adds **no per-worker recovery manager**, maintaining only its whole-member admission, volume mount security, provider/UNKNOWN-effect reconciliation and budget controls. An intentionally PAUSED, checkpoint-ready or BUDGET_EXHAUSTED container must remain stopped until explicitly re-admitted, not automatically revived by an unconditional Docker restart policy. [Docker documentation](docs/REFERENCES.md).

**Status:** Step 8 remains IN DESIGN for member actions, private-phase/final readiness and termination/checkpoint integration; internal worker persistence/recovery policy is **approved**. Step 10 Docker storage/monitoring enforcement implementation is NOT STARTED and tests NOT RUN.

**New customer-local repositories and memory (October 14; ADR-17/18):** Native local Git per member; a trusted customer-controlled gateway shares scoped frozen read-only checkpoint exports. Forgejo or the organization's own Git service is optional by customer policy, never a prerequisite. Customer-specific source, build/reconstruction artifacts and lessons stay owned by the customer and are only retained as authorized; general cross-customer knowledge from client projects requires specific opt-in and appropriate IP/privacy review. Memory retrieves previously **working approaches first** and uses prior failed/inconclusive experiments as **context-specific cautions and test ideas**, never as a global ban on an approach under merely similar conditions. [Read the local-first and knowledge policy](docs/LOCAL_REPOSITORY_AND_KNOWLEDGE_RETENTION.md). No local Git gateway, source sharing, memory indexing or runtime tests have been implemented.

Run `python3 tools/check_specs.py` for static documentation/contract checks only. These checks cannot establish runtime correctness or research performance.
