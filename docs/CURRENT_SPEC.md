# Council — current authoritative implementation map

**Reconciled 2026-10-22. This is a documentation reconciliation, not a new architecture approval.**

**Application implementation: NOT STARTED. Runtime, security, provider, and model-evaluation tests: NOT RUN.** Steps 2–5 and Step 8 have specified v1 architecture/interface contracts; the approved Step 9 provider/MCP policies and Step 10–11 minimal handoff still require implementation-time integration and testing. A specified state, DTO, validation rule, adapter signature, fixture, or documentation check is not a working service.

## How to resolve an apparent contradiction

1. The latest explicit owner-approved policy governs. The [ADR decision index](ARCHITECTURE_DECISIONS.md) records supersession. This map summarizes it; it does not grant new intellectual or operational authority.
2. For concrete v1 contracts, use [Step 2 snapshot transfer](STEP_2_SNAPSHOT_TRANSFER_CONTRACT_V1.md), [Steps 3–5 exact interfaces](STEPS_3_TO_5_EXACT_INTERFACE_CONTRACT_V1.md), [Step 8 action/finalization](STEP_8_ACTION_AND_FINALIZATION_CONTRACT_V1.md), [Step 8.5C+D corrected transitions](STEP_8_5C_8_5D_COMMAND_STATE_RECOVERY_AND_FINALIZATION.md), and the [Step 2–8 reconciliation](STEPS_2_TO_8_CROSS_STEP_RECONCILIATION_2026_10_19.md).
3. Use the detailed topical design for the rules it owns. Earlier prose recording a previous policy or describing a v1 interface as undecided is historical, not a competing implementation instruction. The machine-readable [architecture contract](architecture_contract.json) must agree with current policy.
4. Never silently implement both sides of a contradiction. If two current, non-superseded requirements truly conflict, identify the exact requirement/ADR and resolve it before building that affected behavior. Do not invent a new judge, service, store, queue, or alternative architecture to paper over it.

## Binding policy supersessions

| Historical statement — do not implement as current policy | Binding current policy |
| --- | --- |
| GitHub-public member repositories or complete-public-history checkpoint transfers | Customer-controlled native local Git; selected, hash-pinned, scoped read-only checkpoint snapshots; optional external publication requires separate authorization (ADR-17, Step 2) |
| DeepSeek as the main/lead/default reasoning model, or one reasoning LLM judging everyone | Five original equal peer seats, normally five distinct qualified user-approved models; open-ended qualified model catalog; non-voting Orchestrator and Integrator (ADR-47) |
| MVP requires customer BYOK for every remote model | Operator-funded provider accounts/keys by default for the pilot; optional user BYOK or compatible local inference; provider bills actual funding account owner; encrypted keys outside sandboxes (ADR-53) |
| Required individual member/phase hard spending limits or universal 70/25/5, 45/15/20/15/5 allocation | Hard funding-owner-approved account/run exposure and five protected project-specific pools; adaptive shares within a pool; tighter member/phase limits optional, explicitly approved (ADR-27/53) |
| The entire evidence-feedback/Karpathy loop is optional | Substantive outer strategy/validation and inner execution/check/repair are normal mandatory operating loops; a formal empirical experiment is optional when it is not meaningful; preserve real failures and uncertainty (ADR-43/44/45) |
| Additional keyed internal API submission lanes to prevent simultaneous reviews | ADR-40 withdrawn; use existing PostgreSQL transaction locks, seat uniqueness, generation checks, idempotency, event clock/outbox; Step 7 queue only schedules whole-agent resources |
| Per-model MCP servers | One trusted Council tool broker/MCP client layer with per-service/tenant scoping; model-native provider adapters; no direct sandbox external MCP/internet bypass (Step 9) |
| Local open-weight moderation model | Authorized hosted OpenAI Moderation API plus independent deterministic policy/permission checks (ADR-22) |
| Separate graph database / pgvector for archived project memory, or memory as effect authority | Canonical live evidence/operation data in existing PostgreSQL and customer Git; Qdrant is a derived customer-controlled *archived-project* RAG index; bounded agent continuation cannot override observed tool effects (ADR-49/50/54) |
| Five candidate outputs followed by regex rankings, majority-as-truth, or unilateral final LLM selection | Evidence-grounded Council-authored decisions, one integrated result by a non-voting Integrator, five genuine original-member independent reviews, independent premortem and exact-version user acceptance (ADR-25–39) |
| Step 2–5/8 v1 DTO/state/interface decisions still unspecified | Those v1 **design** interfaces were specified on 2026-10-19; physical migrations, compiled DTOs, provider/client adapters, security enforcement and actual tests remain unimplemented |

## Authoritative documents by responsibility

| Responsibility | Primary source |
| --- | --- |
| Product roles, domain-neutral investigation and UX | [Complete app design](APP_DESIGN.md) and [authority boundaries](PART_4A_AUTHORITY_BOUNDARIES.md) |
| Persistence, provenance, actual observed effects | [PostgreSQL data model](POSTGRES_DATA_MODEL.md), [evidence graph](PART_6_EVIDENCE_PROVENANCE_GRAPH.md), [transaction/idempotency](PART_5_TRANSACTIONS_IDEMPOTENCY_CONFLICTS.md) |
| Typed actor commands, frontend state, UI/SSE | [Typed interaction contracts](TYPED_INTERACTION_CONTRACTS.md) |
| Checkpoint phase, immutable snapshots, sealed discussion and review | [Local repository policy](LOCAL_REPOSITORY_AND_KNOWLEDGE_RETENTION.md), [checkpoint communication](CHECKPOINT_COMMUNICATION_GATEWAY.md), [Step 2 exact snapshot transfer](STEP_2_SNAPSHOT_TRANSFER_CONTRACT_V1.md) |
| Original five members, loops, experiments and readiness | [Part 8 loops](PART_8_AGENT_LOOP_EXPERIMENTATION_DELEGATION.md), [ADR-45 nested strategy/execution](STEP_8_ADR45_NESTED_STRATEGY_EXECUTION_LOOPS.md), [Step 8 action contract](STEP_8_ACTION_AND_FINALIZATION_CONTRACT_V1.md) |
| Collective synthesis, original-member decisions and output verification | [Step 8.4 collective synthesis](STEP_8_4_COLLECTIVE_SYNTHESIS_AND_FINAL_INTEGRATION.md), [Step 8.5A structured Blueprint](STEP_8_5_STRUCTURED_COUNCIL_BLUEPRINT_HANDOFF.md), [Step 8.5C+D transitions](STEP_8_5C_8_5D_COMMAND_STATE_RECOVERY_AND_FINALIZATION.md) |
| Model choice, credentials, tools and budget policy | [ADR-47 open model choice](STEP_9_ADR47_OPEN_ENDED_PEER_MODEL_SELECTION.md), [Step 9 model/tool gateway](STEP_9_PROVIDER_ADAPTER_AND_SHARED_MCP_CONTRACT_V1.md), [ADR-53 funding/egress](STEP_9_ADR53_OPERATOR_BYOK_CREDENTIALS_MCP_EGRESS_ADAPTIVE_SPENDING.md), [Part 7 resources](PART_7_MEMBER_SCHEDULING_RECOVERY_RESOURCES.md) |
| Context rollover, graph memory, local runtime and archive RAG | [ADR-49 working memory](STEP_11_ADR49_GRAPH_WORKING_MEMORY_AND_CONTINUATION.md), [ADR-50 immediate evidence logging](STEP_11_ADR50_MINIMAL_OPERATION_ONTOLOGY_AND_IMMEDIATE_EVIDENCE_PERSISTENCE.md), [ADR-54 minimal handoff](STEP_10_11_ADR54_MINIMAL_IMPLEMENTATION_HANDOFF_QDRANT.md) |
| Authorized implementation order and tests | [Implementation handoff](IMPLEMENTATION_HANDOFF.md), [Step 2–8 verification matrix](STEP_2_TO_8_VERIFICATION_MATRIX_V1.md), [static checker](../tools/check_specs.py) |

## Required implementation consequences — not new systems

- **Identify exact contributions:** Assign stable actor, original seat, provider/model profile and revision, action, alternative, decision, review-generation and immutable artifact/source IDs. Validate canonical structured submissions against typed schemas, identity/scope/version permissions and idempotency. Never extract a decision by regex from prose, assume silence means agreement, create fictional initial votes, or treat duplicated underlying sources as independent support.
- **Persist rather than merely display:** Store genuine discussions, revisions, objections, review positions, evidence/source links, the Decision Register/Blueprint, actual verification attempts, UNKNOWN effects and ordered audit events. The UI is a projection of these records. Version-bound review and acceptance must never transfer silently to different outputs.
- **Separate model assessment from checked reality:** A peer review or majority is a rebuttable interpretation, not proof. Trusted observed tests/source checks record PASSED, FAILED, BLOCKED, NOT_RUN or STALE where appropriate; no model can mark its own work mechanically verified.
- **Keep contextual continuity:** The user-facing conversation/Contract, processed clarifications, allowed source-linked records, bounded continuation packets and current graph/canonical operation state supply follow-up context. A stored chat or compacted note must not be mistaken for a complete native provider context or source of effect authority.
- **Keep one state-machine path:** HTTP streaming versus non-streaming presentation must not change authorization, sequencing, audit, tool effects, budget, checkpoint or finalization gates. Provider-native streaming/tool segments remain adapter-private and are normalized only as supported; frontend SSE is a replayable transport over committed state, not a second orchestration engine. Buffer arbitrary network chunk splits (including partial UTF-8 and multiline SSE records) instead of parsing each read as a complete event.
- **Complete the five-peer process:** Freeze approved candidate/source versions at semantic checkpoints; get five authentic independent sealed reviews before reveal; record evidence-linked changed positions, genuine dissent and communication frontiers; let the non-voting Integrator implement the frozen verified Blueprint; independently re-review the exact integrated output with the original five and run a separate sealed hypothetical six-month-plus premortem before exact-version user acceptance/delivery. No infinite unapproved spend or forced consensus.

## Acceptance checks that must be executed during implementation

1. Malformed/missing/duplicate review IDs, actors, generations, cross-scope inputs or purported rankings fail schema/authority checks without becoming votes or accepted source evidence.
2. Simultaneous fifth-review submissions reveal exactly one all-five current-generation set; a missing fifth seat never passes. An unresolved objection remains visible even when its response obligation is disposed.
3. Context rollover and interrupted provider/tool calls retain the same member/plan, fresh authorized graph findings, and true completed/FAILED/UNKNOWN effects; they never invent earlier model thought, tool success, extra data access or a new member.
4. SSE client reconnect, cursor gap and arbitrary byte/UTF-8/SSE-frame fragmentation recover committed state without duplicating UI decisions; streaming and non-streaming paths produce the same authoritative transitions and failure checks.
5. Compare one integrated artifact against the frozen Blueprint, actual protected checks and five original sealed reviews; revised substantive versions correctly invalidate/re-run affected checks/reviews/premortems.
6. Validate isolation/egress, funding-owner spend/account and five-pool controls, local source-grant revocation, and verified customer-owned archive/cleanup with executable tests and observed evidence.

These are **planned acceptance criteria**, not executed passes. Static checks only test documentation consistency; neither GitHub commits nor model summaries demonstrate application correctness.
