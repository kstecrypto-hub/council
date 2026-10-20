# ADR-46 — Sequential per-model tool execution with concurrent, isolated shared-MCP access

**Owner approved: October 20, 2026.** **Step 9 operational subdesign APPROVED; Step 9 overall IN DESIGN** until the remaining provider/capability, credential, failure and switching workflows are reviewed. **No gateway, MCP server, broker, SQL migration or runtime implementation was created; security, provider, concurrency and integration tests NOT RUN.**

This ADR supplements [Step 9 gateway/shared MCP](STEP_9_PROVIDER_ADAPTER_AND_SHARED_MCP_CONTRACT_V1.md) and the existing [Step 5 transactional operation ledger](PART_5_TRANSACTIONS_IDEMPOTENCY_CONFLICTS.md), [Step 7 scheduling](PART_7_MEMBER_SCHEDULING_RECOVERY_RESOURCES.md), [Step 2 local snapshot isolation](STEP_2_SNAPSHOT_TRANSFER_CONTRACT_V1.md) and [Step 8 nested strategy/execution loops](STEP_8_ADR45_NESTED_STRATEGY_EXECUTION_LOOPS.md). It does not authorize extra queues, extra model supervisors, extra LLM-specific MCP servers, or broad tool parallelism.

## 1. Owner-approved execution policy

1. **The reasoning model plans its own tool needs and dependencies.** A member/authorized worker/Integrator decides the tasks and desired tool sequence within current Council permissions and its Step 8 loops. A model proposal is not a grant of tool authority.
2. **Default to sequential tool execution within one model's ordinary tool turn.** Even if its provider emits multiple tool-call proposals in one response, the trusted gateway/adapter preserves the correct native IDs and proposal order, while the existing trusted broker admits and dispatches **at most one of those tool operations at a time for that turn**, revalidating permissions, grants, resource limits, budget and consequences before each. Independent model members/turns need not be serial globally.
3. **Respect provider-native continuation contracts.** Collect exact authenticated outcomes for each proposed tool ID, including explicit FAILED / DENIED / NOT_EXECUTED / UNKNOWN-dependent status where necessary, and build a provider-native continuation only when its protocol and safety conditions allow. Do not claim a partial call batch completed; never supply another tool's result to the wrong ID. If a later proposed operation depends on an unknown/unsafe earlier effect, block it and reconcile that dependency rather than blindly dispatching. If the provider requires every proposed tool call to receive a result, return accurate typed denial/blocked results as permitted or safely stop the turn rather than fabricate a successful execution.
4. **Do not implement one global tool-call queue or a generic parallel execution planner.** Reuse Step 7's existing capacity/concurrency admission, Step 5's transaction/operation receipts, outbox, idempotency, external-effect reconciliation and existing provider limits. A per-turn sequence is a local dispatch policy, not an extra durable queue/service. True simultaneous tool execution **inside the same model turn is deferred** unless a future, separately reviewed requirement and provider/resource/isolation tests justify it.
5. **Allow safe concurrency across different Council members and authorized workers** when independent work permits it. The fact that two members invoke the *same tool name or MCP service* does not by itself require globally serializing them. This remains subject to CPU/provider/resource caps, tool-server behavior, actual isolation, current source grants and resource conflict controls.

## 2. What 'one shared MCP' means

**One shared Council policy/tool infrastructure**, not one unrestricted MCP server, connection, session, credential or mutable global scope. Tool servers represent approved integrations. The Council-controlled broker and MCP host/client layer are in the trusted boundary; AI agents and models cannot connect to privileged MCP servers directly, select arbitrary tool-server addresses or read server credentials.

- A tool **registration**, its approved schema and policy can be shared across models and Council seats.
- An MCP client connection, server process or credential **must be partitioned by tenant/customer, external account and tool scope wherever necessary**. If the server is stateful, has a mutable selected user/repo/workspace, or cannot prove per-request isolation, use a dedicated scoped instance/connection (including per-seat isolation if required) or disable sharing. Never rely on a request label alone to constrain a privileged stateful backend.
- MCP protocol transport/session mechanics are **not** substitutes for Council's independently enforced per-call authorization and recipient isolation. Pin protocol/SDK versions during implementation and validate actual server behavior.
- No special *per-model* MCP server is required just because a different DeepSeek/OpenAI/Anthropic/local model calls the same approved tool.

## 3. Per-call binding and delivery isolation

**Trusted identity, not model-supplied identity**: the broker derives customer/deployment, run, logical actor/seat and worker-parent, phase/Contract generation, execution epoch, source grant, tool registration/schema version, approved target resource, origin model request/provider-native tool-call ID, operation/idempotency ID, cost/egress/credential scope and authorized result recipient from its authenticated context and canonical records. Model-provided user/seat/tenant/path/token values are untrusted arguments, never an authority source.

For every operation:

1. **Preflight each dispatch independently**: validate actor epoch, exact grant/recipient, tool and approved target, operation class, credentials/tenant, budget/capacity, moderation where applicable, data-egress policy and current version. Scope target objects with server-controlled handles or validated resource IDs rather than peer-selected file paths.
2. **Commit scoped operation intent before external effect**, using the Step 5 canonical transaction lock order; release database locks before external I/O. Tie dispatch and observed result to the immutable originating call/actor/grant/target. Concurrent reservation claims must not overspend.
3. **Bind response to original requester**: use exact operation ID + native call ID + actor/turn/epoch + grant and allowed output recipient. Asynchronous completions, retries, timeouts and cancellation replies cannot be routed by 'last caller', mutable global session data or whichever conversation is active.
4. **Recheck permission before result disclosure**: revoked/expired grant, changed phase, old epoch or wrong actor prevents late results from reaching a new or unauthorized context; quarantine/record the outcome for reconciliation and permitted audit, rather than erasing the billable or consequential external effect.
5. **Scope all mutable state and caches**: no process-global active member, current repo, last result, shared agent conversation, cross-tenant auth cookie or unpartitioned result cache. Cache by strict identity/grant/target/version scope when safe, otherwise disable caching. Avoid tool logs and telemetry disclosing secrets or cross-member private data.
6. **No implied member-to-member information sharing**: the same server may read different private workspaces for different members, but no original member may see another's unpublished source, graph, worker output, review or tool responses outside separately authorized immutable checkpoint snapshots.

**If an MCP implementation cannot pass these isolation requirements, no concurrent shared use of that instance is permitted.** Split scoped connections/instances as necessary; if separation still cannot be guaranteed, deny the affected tool until corrected.

## 4. Concurrency and external write conflicts

| Case | Default admission and dispatch |
| --- | --- |
| Same member/model turn proposes multiple calls | Sequential per-turn, preserving original native tool IDs and accurate partial/blocked outcomes |
| Members 1 and 2 call same approved read-only tool on different authorized objects | Concurrent when implementation proves per-call isolation and capacity permits |
| Members call same read-only tool against a single approved immutable object | Concurrent when result recipient/grant isolation and version pinning hold |
| Calls write disjoint resources | May proceed concurrently under existing Step 5/7 authority and target constraints |
| Two calls can write or modify the **same** resource/version | Use existing broker/Step 5 scoped admission/idempotency and resource-version conflict guards to prevent unsafe overlap; serialize competing **effects for that target** if no demonstrably safe external compare-and-swap/concurrency mechanism exists |
| One effect fails, returns UNKNOWN, or partially commits | Preserve an honest operation outcome, prevent dependent unsafe dispatch/continuation/retry until effect-specific reconciliation; independent unrelated work may continue |
| Same service but poorly isolated credentials, process globals or caches | Do not share it concurrently; partition by tenant/account/seat or disable until isolation passes |

**Important implementation boundary:** PostgreSQL transaction locks protect Council's **own canonical admission and operation state**, but do not magically serialize a remote Git/database/payment tool after the transaction commits. Resource-specific in-flight claims/leases, validated preconditions, connector-supported atomic operations or safe broker-side serialization must actually protect conflicting **external** effects. Reuse the existing operation ledger and broker—not a new global queue. Never hold deployment event-clock/database locks while waiting on remote MCP I/O. Do not invent an unconditional 'exactly once' guarantee when the remote service cannot provide it.

## 5. Future required acceptance scenarios — NOT RUN

| ID | Scenario | Required observation |
| --- | --- | --- |
| P9-19 | One model proposes multiple tool calls in one output | Sequential per-turn dispatch; correct original call ID/order; no hidden parallel effects |
| P9-20 | Provider requires native batch tool-result continuation | Accurate native result mapping including blocked/failed calls or explicit safe stop; no fabricated success |
| P9-21 | Two seats concurrently read via the same Git/search MCP registration | Correct per-seat resource, grant, call IDs, output recipients and no cross-seat source or cache leakage |
| P9-22 | Many interleaved same-tool calls, slow out-of-order replies and retries | Only originating authorized request receives matching result; stale/late result cannot cross epochs |
| P9-23 | Stateful MCP server uses process-global current repo/user or reused account credentials | Concurrent sharing denied; scoped instance/connection separation or disabled tool |
| P9-24 | Two members write the same external resource at the same time | One safe target-bound admission/conflict outcome or externally validated compare-and-swap; no lost update or unsafe overlap |
| P9-25 | Independent writes to different targets/read-only requests | Can progress concurrently without a global tool-server lock where admitted |
| P9-26 | Grant revokes between tool dispatch and slow reply | No unauthorized late result delivery; externally uncertain operation and cost preserved honestly |
| P9-27 | Timeout after non-idempotent MCP write | No blind retry; UNKNOWN persisted, dependent effects gated until reconciliation |
| P9-28 | Worker supplies forged actor, arbitrary peer path or tool-server target | Broker derives true identity/target from authenticated context and denies expanded access |
| P9-29 | Result-cache collision and adversarial tool response content | No cross-member disclosure or prompt-authority promotion; stale/mis-scoped cache bypass blocked |

Tests must include a **real chosen MCP implementation** under concurrency, credential revocation, out-of-order completions, stateful server behavior and negative access checks—not only unit mock assertions or static docs. Historical old Step 9 P9-01..18 tests remain planned, unexecuted. A pushed ADR is not passing implementation or verified isolation.

### Owner-approved October 20 ADR-48 failure-feedback refinement

[ADR-48](STEP_9_ADR48_AUTONOMOUS_TOOL_ERROR_FEEDBACK_AND_COOLDOWN.md) supplies the model-facing error feedback and recovery policy for ADR-46 ordered tool results. The broker maps `FAILED`, `RETRY_LATER`, `BLOCKED` and `UNKNOWN` honestly to the original tool-call IDs; `RETRY_LATER` is only a trusted presentation/admission classification, not a new canonical success state. For transient MCP outages the scoped initial cooldown is **3–7 minutes**, with longer provider-requested wait/backoff when necessary. A corrected deterministic Python/tool argument error needs no such cooldown. Unsafe consequential UNKNOWN effects must be reconciled before repeating, and denied authority is not overcome by waiting. No new scheduler/queue or routine user retry prompt, and independent members' healthy services do not globally pause. Step 7 finite infrastructure restart limits remain distinct from the absence of an arbitrary cap on agent-directed *safe tool* retries. **Approved design; all runtime tests NOT RUN.**

## 6. Status and next Step 9 discussion

**Policy approved, architecture text committed when pushed.** Step 9's remaining provider-native tool continuation variants, qualification registry, multi-account credential isolation, budget/error handling and model switching still require owner-reviewed operational scenarios. This amendment does **not** mark Step 9 fully designed, implemented, or tested.
