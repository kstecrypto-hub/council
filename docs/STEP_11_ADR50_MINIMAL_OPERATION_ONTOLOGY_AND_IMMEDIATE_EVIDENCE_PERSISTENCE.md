# ADR-50 — Immediate durable operation observations and minimal graph ontology

**Owner approved October 21, 2026.** Scope: Step 11 memory/graph persistence and the existing Step 5/6/8 tool-to-evidence boundary. **ADR-50 policy APPROVED; Step 11 full retrieval/selection/compaction/archival integration remains IN DESIGN; implementation NOT STARTED; runtime, security, performance and token-use tests NOT RUN.**

Related: [ADR-49 graph and normal working memory](STEP_11_ADR49_GRAPH_WORKING_MEMORY_AND_CONTINUATION.md), [Part 5 operation ledger](PART_5_TRANSACTIONS_IDEMPOTENCY_CONFLICTS.md), [Part 3 storage and graph relationships](POSTGRES_DATA_MODEL.md), [Part 6 evidence/provenance graph](PART_6_EVIDENCE_PROVENANCE_GRAPH.md), [ADR-45 nested reasoning loops](STEP_8_ADR45_NESTED_STRATEGY_EXECUTION_LOOPS.md), [ADR-48 autonomous failure handling](STEP_9_ADR48_AUTONOMOUS_TOOL_ERROR_FEEDBACK_AND_COOLDOWN.md), and [Step 11 roadmap](MVP_SCOPE_BY_STEP.txt).

## 1. Owner-approved boundary: save observations immediately; do not continually summarize memory

Council preserves **durable operational facts as each operation moves through its lifecycle**; preserves **new graph knowledge/meaningful edges immediately when the relevant finding/decision is committed**; and **does not** refresh normal working-memory summaries, construct another LLM memory prompt or inject new graph retrieval context after every tool call.

Three distinct responsibilities:

1. **Automatic operational logging, zero extra LLM calls:** the existing Step 5 trusted broker/ledger records a scoped operation **intent before external dispatch**, and appends the actual **observed result, error, UNKNOWN, attempted retry or reconciliation** as soon as that observation is durably accepted. Retain separate immutable logical operation/attempt receipts, event ordering, actor/target identity, idempotency, permissions/epoch and permitted output/artifact references. The agent need not remember or manually request these saves.
2. **Immediate evidence-graph maintenance where there is real knowledge:** when a hypothesis, assumption, material finding, experiment observation/disposition, contradiction, evidence citation or strategic decision is registered, commit its canonical record, requisite typed graph relationships and audit event **in the same PostgreSQL transaction where feasible/required by the existing Part 5/6 contract**. Distinguish **observed fact** from **member-authored interpretation**. Graph nodes/edges remain projections over canonical records, not independently authoritative memory.
3. **Occasional working-memory/context updates:** update the member's bounded current plan/continuation summary when the strategy/task substantially changes and before a safe yield, context rollover, provider switch boundary or controlled suspension. Do not perform fresh context compaction, graph retrieval or model calls merely because an action completed. The underlying operation/evidence records survive even if this summary is stale.

**Meaning of 'immediate':** persist the canonical observation at the next successful local committed operation-result transaction, **not** after a batching interval or checkpoint. External I/O is never placed inside that transaction; the external operation's *intent* and later observed outcome are separate commits. There cannot be a guarantee of observing a lost remote acknowledgement; mark/reconcile `UNKNOWN_PENDING_RECONCILIATION` instead. Optional expensive graph search/index or UI projection updates may lag while exposing a committed event watermark; fresh canonical fallback must be available for correctness.

## 2. Small extensible ontology: reuse existing types, do not build a second event system

For useful cross-domain traversal, use these **logical reference types** in existing canonical tables and the existing `council_core.graph_relationships` projection (not mandatory new tables):

| Node/reference | Origin and purpose |
| --- | --- |
| `Actor` | Authenticated logical Council member, parent-scoped worker, Orchestrator or nonvoting Integrator |
| `Operation` | Existing durable operation + append-only attempts, tool identity, target and exact effect status |
| `Observation` | Trusted observed result/error/UNKNOWN/reconciliation outcome linked to a particular operation/attempt; **not** a model's unsupported claim |
| `Artifact` | Existing hash/version-scoped Git revision, file, report, source extract or stored tool output reference |
| `Finding` | Member-authored claim, decision, test result, challenge or evidence-bearing interpretation represented by existing Step 6/8 canonical records |
| `Hypothesis` | Member-attributed outer approach/assumption, optional tactical proposition or claim revision under existing Step 6/8 records |

Recommended small **relationship vocabulary** (initial, extensible, not a closed world ontology):

- **Mechanical, trusted-runtime-derived:** `Actor PERFORMED Operation`; `Operation USED Tool` (tool may remain registered tool identity rather than a new graph-node table); `Operation PRODUCED Observation`; `Observation REFERENCES Artifact`. Exact actual actor/operation/tool/status/output bindings are taken from authenticated operation/attempt and artifact records, never inferred from freeform tool text.
- **Semantic, model-authored and attributed:** `Finding SUPPORTED_BY Observation/Evidence`; `Finding CONTRADICTS Hypothesis/Claim`; `Finding SUPPORTS Hypothesis/Claim`; `Experiment TESTS Hypothesis`; `Decision REVISES Hypothesis` or similarly minimal existing supported edge types. For these, the originating reasoning member/worker declares the relationship in its **ordinary reasoning/action/result submission**, and supplies current scoped source IDs and a justification when material. The runtime validates reference existence, ownership, schema and visibility, **not its substantive truth**.

The existing `graph_relationships.origin = RUNTIME | AGENT_INTERPRETATION`, author and justification/reference fields remain the attribution mechanism. New evidence and graph links preserve versions and privacy and can be revised/challenged; do not silently overwrite incompatible earlier conclusions.

**Do not create graph noise for every mundane tool call:** every call has the operational audit/ledger, but a trivial repeated `Python NameError`, normal file read, routine progress echo or empty result does **not** need its own semantic finding/hypothesis node or a fully duplicated graph subgraph. The broker may expose mechanical graph-relevant relationships by joining/projection over existing operation records when useful. It must not create an interpretation because a tool exited zero/nonzero. When an observed test failure **does** materially support or contradict the current approach, the agent records the semantic relationship and the backend persists it promptly with its evidence.

## 3. Normal execution sequence and trust boundaries

1. **Before external dispatch:** authenticate and authorize scope/actor/worker-parent/epoch/grants/budget/target. Commit Step 5 operation intent, idempotency and event/outbox, then invoke the approved native/MCP tool outside SQL locks. The operation's existence is not a claim that its effect occurred.
2. **After receiving a result or losing contact:** the trusted broker records `SUCCEEDED`, `FAILED`, `BLOCKED` or `UNKNOWN_PENDING_RECONCILIATION` exactly as verified, linked to originating operation, attempt, caller, target and any small output/hash/artifact reference. Record changed effect states immediately and settle/reserve budget correctly.
3. **Agent continues its existing Step 8 inner loop** using the ordinary tool result; it may decide that this response supports a factual claim, disproves an assumption, or is an ordinary recoverable defect. The agent can register material `Finding`/`Hypothesis`/`Experiment` updates and edges **inside the normal existing submission**, not via an additional “memory LLM”, mandatory intermediate reasoning turn, automatic second prompt or separate semantic summarizer.
4. **Canonical graph save:** accept member-authored semantic edges only with provenance, source permissions, exact evidence and relation-schema validation; persist the associated finding/evidence/essential relationships and event atomically. Do not manufacture claimed test PASS or scientifically meaningful causation from a tool exit code. Background search/visual index replay is permitted subject to version/watermark freshness; a resumed member can query committed canonical records if projection lags.
5. **Context management remains separate:** no forced after-every-tool summary, no constant reload of the graph into the model. Use the short working state + relevant on-demand graph neighbors and original artifacts only when the task requires them. Preserve same-member context and retry eligibility as ADR-49/48, with Step 5 ledger always authoritative.

The operation record can expose to the graph `actor_ref`, `operation_id`, `attempt_id`, `registered_tool_id`, `target_ref`, `status`, `observed_at`, `source_event_position`, `artifact_ref/hash` and `provenance` through existing typed contracts or validated projections. This list is a **minimal logical interface, not mandatory new physical columns or an additional log storage system**. A pending/unknown effect is never recorded as a successful `Observation`; a success receipt cannot expose a forbidden source/peer workspace.

## 4. Memory privacy, retention and costs

- No cross-member graph, operation-output, worker or private working-context disclosure outside explicitly authorized immutable checkpoint grants and their visibility/closure rules. Tool and model output are untrusted *content*, not authority to publish links or hidden prompts.
- Preserve per-run source/grant scope, version, author, original observed result and permitted artifact reference; archived successful and failed observations are conditional to the actual versions, tests, workload and customer retention policy. No global blacklist, and no live active-branch-to-shared-memory promotion.
- Automatic operation/event logging and canonical typed relationship insertion **do not consume additional model tokens by themselves**. An agent may include a small relationship declaration in a normal output, which uses ordinary model tokens; this design **does not guarantee absolutely zero token overhead**. Avoid an extra LLM inference pass solely for background memory maintenance.
- Continue to honor Step 5 bounds, Part 3 artifact storage for large raw outputs, Step 7 budgets and provider-independent tool identity; this ADR neither creates an extra resource queue nor makes promises about cost/performance until measured.

## 5. Required future acceptance cases — NOT RUN

| ID | Scenario | Required observation |
| --- | --- | --- |
| M50-01 | Each tool call before dispatch and verified result | Durable intent first; actual observed status and attempt persisted without asking agent to log |
| M50-02 | Lost acknowledgement after external Git/database write | UNKNOWN recorded promptly; no false success edge, duplicate side effect or immediate blind retry |
| M50-03 | Twenty ordinary Python calls, no material findings | Twenty attributable operational records, no forced twenty semantic findings/graph reloads/working-memory summaries |
| M50-04 | Test result really contradicts current hypothesis | Original model can author current-source semantic contradiction linked to observed result; canonical finding/edge/event commit together |
| M50-05 | Tool error text attempts arbitrary `CONTRADICTS` edge / prompt escalation | Runtime records actual error as untrusted data, does not accept tool-supplied semantic authority |
| M50-06 | Member/worker attempts edge to another member's private material | Denied by current grants, RLS and checkpoint visibility; no search/cache side leak |
| M50-07 | Graph projection indexing delayed after canonical evidence commit | Context manifest exposes watermark; fresh canonical query can see the committed relationship |
| M50-08 | Agent crash between tool result and working-memory summary update | True operation state recoverable from ledger; no fabricated retained interpretation; same original logical member resumes |
| M50-09 | Repeated finding/operation submission after restart | Canonical idempotency returns existing receipt; no duplicate effect/finding or graph edge |
| M50-10 | Large output and token usage verification | Large output stored as scoped artifact ref; no unconditional model-memory summarization call or hidden duplicate LLM usage |
| M50-11 | Experiment marked successful with missing/unexecuted test | Runtime cannot invent PASS or `SUPPORTED_BY` evidence; honest NOT_RUN/INCONCLUSIVE/UNKNOWN preserved |

**Verification boundary:** These cases are requirements only. The graph/ontology MVP's runtime, SQL, tool integration, token-efficiency and crash safety remain **NOT STARTED / NOT RUN**. Step 11 remains **IN DESIGN** for ranking, context-selection, exact DTOs, source/version indexing and accepted-project memory promotion.
