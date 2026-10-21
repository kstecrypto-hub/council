# ADR-52 — Step 9 provider interruption: resume from compacted working memory, fresh scoped graph and actual operation receipts

**Owner approved October 21, 2026.** This specifies the **interrupted model-provider connection recovery** within Council's existing Step 9 gateway and Steps 5/7/8/11 infrastructure. **Policy APPROVED, Step 9 overall IN DESIGN; implementation NOT STARTED and provider, reconnection, security, cost and runtime tests NOT RUN.**

Related: [Step 9 gateway/provider continuations](STEP_9_PROVIDER_ADAPTER_AND_SHARED_MCP_CONTRACT_V1.md), [ADR-46 tool ordering/IDs](STEP_9_ADR46_TOOL_CALL_ORDERING_AND_MCP_ISOLATION.md), [ADR-48 MCP retry and failures](STEP_9_ADR48_AUTONOMOUS_TOOL_ERROR_FEEDBACK_AND_COOLDOWN.md), [ADR-49 graph + compact working memory](STEP_11_ADR49_GRAPH_WORKING_MEMORY_AND_CONTINUATION.md), [ADR-50 immediate operational/graph persistence](STEP_11_ADR50_MINIMAL_OPERATION_ONTOLOGY_AND_IMMEDIATE_EVIDENCE_PERSISTENCE.md), [Step 5 operation/idempotency ledger](PART_5_TRANSACTIONS_IDEMPOTENCY_CONFLICTS.md), [Step 7 admission](PART_7_MEMBER_SCHEDULING_RECOVERY_RESOURCES.md), and [ADR-45 nested Karpathy loops](STEP_8_ADR45_NESTED_STRATEGY_EXECUTION_LOOPS.md).

## 1. Approved owner intent

If Council loses the **LLM provider connection or usable native model session**, it **does not discard or restart the agent's original task**. Council reconstructs the same logical member's current, bounded context from:

1. **Latest retained compacted working memory / continuation packet** for the member: original objective, outer strategic approach, inner task, recent progress, constraints, pending worker handoffs and next intended action.
2. **Latest relevant and currently authorized graph evidence**: source-linked findings, tested observations, challenges, relationships, decisions and revisions committed since that packet, subject to exact private member/source/grant visibility. Do **not** dump the entire graph, make a stale index appear current or use live private member data to update another member's frozen common memory.
3. **Canonical Step 5/7 operation state and genuine observed tool results**: authoritative completed, not-yet-dispatched, failed, blocked or `UNKNOWN_PENDING_RECONCILIATION` operations; pending tool-call IDs, actual cooldown eligibility, billing/usage uncertainty and current permissions/budgets/epoch. Canonical observed state wins if it contradicts the narrative in memory.

Council **explicitly tells the model that its provider connection/session was interrupted** and that its context was reconstructed, then lets the **same original logical agent** resume its existing Step 8/ADR-45 inner and outer loops autonomously. Ordinary recovery does not require the user to resolve a troubleshooting dialog, approve a retry, reselect a model, start a new project or reinterpret an otherwise valid strategic approach.

The two intellectual memory views are **not** re-summarized by a new memory agent. Use the **already compacted** working state as-is when suitable; supplement it with new committed graph neighbors and operation receipts **on this recovery event**, not on every routine tool call. A recovery-only compact summary may be regenerated under normal bounded-compaction policy if truly needed for the available context, not automatically for every transient network event.

## 2. Exact restart and continuation order

1. **Detect and persist real interruption.** The trusted provider gateway records the disrupted model request's identity, model/adapter/profile version, actor/epoch, provider response/continuation IDs if received, and its actual observed outcome. A lost reply is **not proof the model never ran or wasn't billed**; retain uncertain usage reservations and `UNKNOWN` where appropriate. Preserve brokered tool intents/outcomes without fabricating provider/tool response receipts.
2. **Restore authority before context.** Use existing Step 7 whole-member admission and Step 5 canonical state to verify same logical member, run/phase/contract generation, sandbox/workspace, current user grants, credential/egress scope, cost/token budgets, current epochs and pending external operations. The model's prior summary cannot grant tool authority.
3. **Recover actual work and memory.** Load the latest **existing** bounded working packet and private workspace notes. Retrieve **current, relevant, access-scoped graph records** (including newer substantive findings that were persisted promptly under ADR-50); check source/version and index event watermarks, and read canonical records directly if projection freshness is insufficient. Add a **small ledger-derived operation delta** for tool/provider calls since the packet. Preserve original outer hypothesis and the current inner task, and explicitly surface unresolved uncertainty.
4. **Choose provider-safe continuation.** If the selected **same authorized provider/model/profile** has a genuinely recoverable native continuation handle and valid original tool IDs, use its adapter's supported continuation format and synchronize with the latest permitted observations. Otherwise, construct a **fresh session for that same model profile** using a bounded factual context/manifest and the restored memory, graph evidence and true operation receipts. Never invent provider session state, replay opaque hidden reasoning, transplant a native handle to another provider, pretend a prior tool-result reply reached the model, or silently switch vendors/models.
5. **Notify the model in ordinary continuation context.** E.g. `Your previous provider connection was interrupted. You are the same logical Council member. Your current objective, outer strategy and inner task are restored from the latest compacted working memory, with newer relevant graph evidence and verified operation results below. Completed work is already recorded; some actions are pending/unknown. Continue your existing task and use the normal tool broker for future work.` This is an **informational recovery notice**, not a claimed recovered transcript or instruction that bypasses current user/owner policy.
6. **Resume autonomous work after safe dispatch admission.** The agent decides whether to continue, investigate, correct or request a new action through its existing nested loop. The trusted broker **still independently checks every operation** and does not replay successful tool calls. Resume blocked only as necessary for real pending dependencies, current grants/permissions, provider availability, finite resource/budget limits or unreconciled consequential effects.

**While provider is unavailable:** member may safely yield under **existing Step 7 scheduler** and be resumed when actual provider/admission readiness permits; no agent spinning, hot-polling, unconditional frequent retry, new recovery agent, new timer/queue or new MCP server per model. The ADR-48 **3–7-minute cooldown applies to transient MCP tool services**, not automatically to every lost model inference connection. Provider rate/Retry-After and Step 5 retry uncertainty stay separately enforced.

## 3. Multiple proposed tools and disconnects

For a prior model output proposing `Tool A`, `Tool B`, `Tool C` (ADR-46 dispatches within the turn sequentially):

| Observed ledger state | Recovery policy |
| --- | --- |
| A executed and **confirmed SUCCEEDED** | Reuse its original recorded result; **never rerun A** simply because provider connection dropped. |
| B executed and **confirmed SUCCEEDED** | Same: preserve its original operation/call/result identity; do not re-execute. |
| C **only proposed, not dispatched** | Keep proposal/pending intent distinguishable from a real effect; do **not auto-execute** it during resumption without current phase/epoch/grant/dependency checks and valid native continuation or a new model-authored request. |
| C **dispatched but returned no trustworthy observed outcome** | Preserve `UNKNOWN_PENDING_RECONCILIATION`; reconcile consequential effect before retry, and do not falsely report FAILED or SUCCEEDED. |
| Previous model continuation response may have run but was lost | Preserve provider request/usage uncertainty; never fabricate that the model consumed the prior tool results or that a charge was zero. |

If provider protocol requires one batched response covering all proposed tool-call IDs, the adapter must either supply **accurate observed/denied/not-executed statuses only where that native protocol supports them**, or stop the native continuation safely and reconstruct a fresh same-model session. Do **not** invent success for missing tool results or re-dispatch side effects simply to satisfy a provider wire shape. Exactly-once external effects are not assumed.

## 4. Privacy, spending and efficiency

- Preserve **same original member/worker-parent identity** and existing Council governance. The restored session is *not* a sixth member, a newly invented opinion or a default alternative provider. Current model-profile assignment stays unchanged without separately authorized switch.
- Keep graph retrieval, compacted notes, operation delta, cache and continuation manifest bounded to the correct **member, source grants, run, epoch and authorized frozen checkpoint**. No other member's unpublished graph or sealed reviews; no raw credentials or hidden model reasoning.
- The packet may be stale; newest **verified observations and source-linked graph changes** override it. The graph is evidence, **not** proof that the external action succeeded when canonical Step 5 outcome is UNKNOWN.
- No per-operation model summarization; no need to update compacted memory for every tool use. On **actual recovery**, fetch only relevant new evidence and receipts and supply one bounded coherent context. The new model inference naturally incurs ordinary context/input token cost under existing approved limits, but no separate model-memory pass or additional stateful service.
- Model-provider requests/usage continue to use current Step 5/7 reservations and explicit uncertainty. No implicit user approval for higher spend or altered data egress, and no user confirmation for routine in-scope recovery.

## 5. Future acceptance evidence — designed, NOT RUN

| ID | Scenario | Required result |
| --- | --- | --- |
| P9-51 | Provider stream disconnects mid-member work | Interruption and provider request uncertainty recorded; existing same member preserved, no invented tool/response success |
| P9-52 | Latest compacted packet predates material graph finding | Resume context includes relevant newer authorized graph evidence and canonical tool delta, not a silently stale picture |
| P9-53 | Completed tools A/B, undispatched proposed C | A/B are not re-executed; C stays undispatched until safely validated or requested; IDs and outcomes remain distinct |
| P9-54 | Potential external write's acknowledgement lost | UNKNOWN blocks unsafe dependent retries until observed reconciliation even if resume/cooldown time passes |
| P9-55 | Provider-native session handle valid | Correct same-model native tool result IDs and provider continuation, no fabricated prior receipt |
| P9-56 | Original provider session cannot be resumed | Fresh session for same approved model with explicit interruption notice, bounded compacted memory, graph, ledger and unchanged logical agent identity |
| P9-57 | Provider missing/usage uncertain | No arbitrary MCP 3–7-minute rule for model transport, no hot polling; actual usage reservation and provider cooldown/availability honored |
| P9-58 | Previous packet claims completion, ledger says pending/UNKNOWN | Canonical ledger wins; agent sees actual uncertainty |
| P9-59 | Source grant revoked or another member's private evidence present | Unauthorized retrieval/late tool delivery denied; no leakage through reconstructed context or caches |
| P9-60 | Resume would require unapproved new provider, budget or egress | No automatic switch, permission expansion, user routine troubleshooting prompt or invented PASS |
| P9-61 | Repeated provider drop and same work retries | No duplicate consequential external effect, double finalization, phantom reviewer or strategic forced reset |
| P9-62 | Normal tool calls without interruption | No forced graph retrieval, memory compaction or extra LLM summarizer after every action |

**Completion boundary:** Only the **Step 9 provider-interruption recovery policy** is owner-approved here. Exact provider adapter, DTO/continuation, availability, testing and Step 11 retrieval integration remain implementation-time design/verification work. **Step 9 overall IN DESIGN; Step 10 partly designed; Step 11 IN DESIGN. Runtime implementation NOT STARTED; live provider, MCP, crash, privacy, cost and acceptance tests NOT RUN.**
