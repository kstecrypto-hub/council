# ADR-49 — Graph memory + normal working memory + existing durable continuation

**Owner approved October 21, 2026.** This records the memory and resumption architecture for Council's existing Step 11 and its interaction with Step 8/9 recovery. **Policy APPROVED; Step 11 detailed selection, prompt/DTO wiring, evidence-index and archive integration remain IN DESIGN. Application implementation NOT STARTED. Runtime/model/security/recovery tests NOT RUN.**

Links: [Step 11 roadmap](MVP_SCOPE_BY_STEP.txt), [Council canonical storage/graph](APP_DESIGN.md), [Step 8 ADR-45 nested reasoning loops](STEP_8_ADR45_NESTED_STRATEGY_EXECUTION_LOOPS.md), [Step 9 ADR-48 autonomous tool recovery](STEP_9_ADR48_AUTONOMOUS_TOOL_ERROR_FEEDBACK_AND_COOLDOWN.md), [Step 5 canonical effects](PART_5_TRANSACTIONS_IDEMPOTENCY_CONFLICTS.md), [Step 7 recovery/admission](PART_7_MEMBER_SCHEDULING_RECOVERY_RESOURCES.md) and [local-first evidence/archives](LOCAL_REPOSITORY_AND_KNOWLEDGE_RETENTION.md).

## 1. Approved decision: no new AI memory system

Council retains **two complementary intellectual memory views**:

1. **Graph memory**, for attributable and versioned *knowledge*: current strategic hypothesis/approach, claims, assumptions, source relationships, supporting/contradicting evidence, observed experiments, conditional failures, decisions and dependencies. Implement as approved typed relationships/retrieval over canonical customer-local records in PostgreSQL, not a second independently authoritative graph database. Query only a small relevant neighborhood, verify freshness/permissions, and allow source/history search if a relevant edge is missing.
2. **Normal agent working memory**, for *continuity of intent*: the member's current objective, outer-loop approach and success criteria, current inner-loop plan/task, what it tried and observed, unresolved questions, worker notes and next intended action. Persist its needed portion in existing bounded **continuation packets/context manifests** plus its authorized private durable sandbox workspace. This is not a promise to preserve the model's raw context window, hidden chain of thought, entire token transcript or live worker process stack.

There is also a **third necessary authority category, but it is NOT another AI memory system**: Step 3–5 canonical PostgreSQL operation/permission/budget/lease/epoch/event records determine the *actual* state of a tool, whether an external action was observed, when the service cooldown expires and whether a retry is authorized. Graph facts and model summaries cannot overrule these records. User-approved, customer-controlled local Git/hashed artifacts hold reproducible project files and explicitly retained accepted-project learning; these are existing storage mechanisms, not another live reasoning memory.

**Do not add Redis, a second graph database, a dedicated vector database, a new memory agent, a cooldown-memory service, or another scheduler solely for recovery/context continuity.** Step 11's retrieval quality may be evaluated later, without prejudging a more complex storage/index requirement.

### October 21 ADR-50 — immediate logging, selectively immediate graph semantics

[Owner-approved minimal logging ontology and evidence persistence](STEP_11_ADR50_MINIMAL_OPERATION_ONTOLOGY_AND_IMMEDIATE_EVIDENCE_PERSISTENCE.md): every brokered operation's intent and actual trusted observation enter the **existing Step 5 durable operation/attempt ledger immediately**, with no extra model inference. Material new hypotheses, findings, experiment evidence and graph relationships enter canonical Step 6/8 records and their **essential graph edges immediately on submission/commit**, distinguishing `RUNTIME` mechanics from `AGENT_INTERPRETATION`. No duplicate semantic nodes for every mundane tool call. **Do not** regenerate the working-memory summary, compact, reload graph neighborhoods or allocate additional model calls merely because a tool returned; do those on material plan change or controlled suspension/rollover and on-demand retrieval. External UNKNOWN stays UNKNOWN regardless of any summary. This refines timing/ontology but preserves this ADR's two-view memory and canonical authority boundaries. **Design only; runtime/token tests NOT RUN.**

## 2. Suspension and continuation during MCP cooldown/provider loss

When a trusted tool result is `RETRY_LATER`, `BLOCKED`, `FAILED` or `UNKNOWN_PENDING_RECONCILIATION`, preserve its observed status and originating member/model-call/operation IDs in the existing ledger. The reasoning model may pursue other currently authorized inner-loop tasks; if it has no useful independent work it can **safely yield** under Step 7's existing whole-member scheduler instead of polling or keeping a container/model session awake for the 3–7-minute MCP cooldown. Never force a strategic-hypothesis reset or imply the platform can suspend and restore raw LLM RAM.

On intentional yield, context rollover, model-provider interruption, Docker stop/recreate or safe recovery, persist a **bounded, source-referenced continuation packet** for the same original logical member (or the original worker's parent-scoped progress), containing, as applicable:

- logical member/worker-parent identity, run, Contract and semantic phase/checkpoint generation; current policy/source-visibility scope and record versions;
- current **outer** approach/hypothesis and success/falsification criteria, and **inner** task, immediate plan, last genuinely observed result and next possible actions;
- decisive graph/source/claim/experiment IDs and revisions, unresolved objections, assumptions, known risks or tests not run (not an unsourced all-knowing summary);
- exact private candidate/workspace/Git/artifact references and task/worker handoffs that are still authorized;
- pending operation/attempt IDs, actual last-known outcomes including `UNKNOWN`, and any cooldown `retry_not_before`; **do not** copy a stale `retry_allowed` as permanent authority;
- the next intended action or safe independent work and explicit known blockers/uncertainty.

The **context manifest** separately captures which exact scoped records, versions, source hashes and graph/index event watermarks were loaded into the model context and flags omitted/uncertain information. The packet is a bounded resume aid and **non-authoritative** whenever it disagrees with newer canonical state. Normal memory can be rewritten/summarized for context efficiency, but the underlying evidence and failed attempt receipts remain traceable.

## 3. Safe resume order (same member identity)

1. **Trusted admission first:** Step 7 verifies the same member's identity, current Contract/phase, resource slot, execution epoch and permitted sandbox workspace; Step 5 loads fresh permissions, grants, approved budgets, outstanding external effects and true operation/cooldown states. An old LLM session or continuation packet does not grant authority.
2. **Load bounded working memory:** recover the latest permitted version of that member's context packet and private notes, checking hashes/versions against canonical state. Preserve the member's original outer approach and pending inner task instead of introducing an unnecessary new hypothesis.
3. **Retrieve graph evidence on demand:** pull only current and authorized related claims, evidence, objections and recent operation references. Query canonical sources/fallback search if the graph projection is stale; never assert that an old graph view includes a newly committed change.
4. **Build a fresh model continuation:** provide the selected qualified model with a minimal factual context, genuine observed tool results, unresolved status and next possible work. Native provider-specific continuation is preserved only when actually compatible within the current approved model profile. No silent provider switch, raw cross-vendor reasoning-state transplant, fabricated missing tool response or new Council voting seat.
5. **Recheck before any action:** the model may request a retry or alternate action, but the broker must independently revalidate the exact tool, caller, recipient, permissions, budget, epoch, dependencies and actual `retry_not_before`. A timer expiry is not proof an `UNKNOWN` Git/database write failed. Reconcile consequential unknown external effects first and block only dependent work as existing Step 5/ADR-48 require.

There is **no automatic new user question** for ordinary tool recovery, and no automatic user permission, spending increase, egress expansion, checkpoint readiness or success declaration.

### October 21 ADR-52 — provider interruption gets graph + compacted memory

[Approved Step 9 interruption-reconstruction policy](STEP_9_ADR52_PROVIDER_INTERRUPTION_CONTEXT_RECONSTRUCTION.md) consumes **the latest persisted, permitted compacted working packet**, **relevant current, authorized graph findings** including new material observations since that packet, and **trusted Step 5/7 exact operation state**. Before any restarted inference, validate current member/phase/epoch/grant, budget and unknown effects. Explicitly tell the same model/member that its provider connection was interrupted; preserve original outer strategy, inner task, and true completed versus pending tool status. Resume provider-native same-profile context only when real call IDs and session state remain valid; otherwise construct a fresh bounded context for the same model profile. A stale packet cannot erase fresh graph or overwrite canonical effects, and no graph/context refresh is required for every normal tool action. No forced extra LLM compaction, no separate memory/retry service or silent provider switch; **Step 11 still IN DESIGN; implementation/tests NOT STARTED/NOT RUN.**

## 4. Privacy, scope and long-term retention

- Each Council member's active graph neighborhoods, notes and continuation packets are **private to that member/parent authority**. Another member sees only independently authorized frozen checkpoint publications under the existing local gateway and sealed-review barriers. Tool results, queued failures and retriever caches cannot become covert inter-member communication.
- All five original members may begin from the same **permitted pinned prior-project memory snapshot**, but independently query, interpret and challenge it. Do not refresh that shared corpus using live private branch findings during a run.
- Customer-approved accepted-project lessons and reconstruction files belong in the existing customer-owned Git/archive system with source/version/test lineage and retention permissions. Retrieval is **success-first**; earlier failures remain context-specific warnings and do not become permanent strategic blacklists. Cross-customer transfer requires explicit, scoped release approval.
- A long cooldown or fresh model context window must not expose extra project data, secret keys, private provider reasoning or other members' unpublished work. Authorization applies equally to graph edges, search hits, summaries, continuation packets and archived artifacts.
- Agent memory is **not evidence that an action succeeded**. A retained model note saying 'push completed' cannot override the operation ledger's `UNKNOWN_PENDING_RECONCILIATION` status.

## 5. Required future acceptance scenarios — all NOT RUN

| ID | Future case | Required result |
| --- | --- | --- |
| M49-01 | MCP cooldown pauses member with no other work | Bounded packet retained; existing whole-member slot safely released where appropriate; no hot polling |
| M49-02 | Resume after cooldown | Original outer approach/inner task restored; real current cooldown and tool status checked before dispatch |
| M49-03 | Git push had unknown result despite summary claiming success | Canonical UNKNOWN wins; no duplicate push before safe reconciliation |
| M49-04 | Context packet stale after changed phase/grant/budget | Old authority not reused; unauthorized action blocked |
| M49-05 | Graph projection lags a committed objection/tool result | Context manifest exposes watermark; fresh canonical retrieval or honest stale limitation |
| M49-06 | One private member requests another's unpublished evidence during resume | Request denied outside authorized frozen checkpoint scope |
| M49-07 | Provider session lost or context window exhausted | Same logical member resumes from bounded source-linked context; no invented raw reasoning continuity |
| M49-08 | Worker notes survive authorized Docker recreation | Original parent retains authority and decides recovery; no central worker resurrection/extra seat |
| M49-09 | Previously failed approach retrieved for new project | Conditional failure context and test suggestions, not a universal exclusion |
| M49-10 | Archived project accepted and temporary Council DB ready for teardown | Retained permitted Git/evidence reference closure verified under customer retention policy before archive claim |

**Status boundary:** ADR-49 specifies a **memory/resumption direction** and affirms existing Step 11 MVP continuity elements; it does **not** finalize all Step 11 ranking/indexing, packet DTOs, context selection, archive-validation implementation or testing. Those remain IN DESIGN / NOT STARTED / NOT RUN.
