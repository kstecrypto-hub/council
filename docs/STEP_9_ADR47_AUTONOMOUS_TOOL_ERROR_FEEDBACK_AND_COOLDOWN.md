# ADR-47 — Autonomous tool-error feedback and service-scoped retry cooldown

**Owner approved October 20, 2026.** Step 9 **recovery-policy design approved**, Step 9 overall **IN DESIGN**. This document records approved behavior only. No application, tool broker, MCP server, recovery timer, provider adapter, database migration, or runtime evaluation was implemented; all tests **NOT RUN**.

Authoritative alongside [Step 9 gateway/MCP contract](STEP_9_PROVIDER_ADAPTER_AND_SHARED_MCP_CONTRACT_V1.md), [ADR-46 tool isolation/ordering](STEP_9_ADR46_TOOL_CALL_ORDERING_AND_MCP_ISOLATION.md), [Step 5 external-effects and idempotency](PART_5_TRANSACTIONS_IDEMPOTENCY_CONFLICTS.md), [Step 7 resource/recovery contracts](PART_7_MEMBER_SCHEDULING_RECOVERY_RESOURCES.md), and [ADR-45 nested reasoning loops](STEP_8_ADR45_NESTED_STRATEGY_EXECUTION_LOOPS.md).

## 1. Approved operating model

**Routine recovery belongs to Council, not a user approval dialog.** Failed tool calls return a **small standardized, attributed tool result** to the same reasoning member/worker/Integrator through its native provider continuation. The model chooses to correct arguments, investigate, select another permitted method or request a retry in its **existing inner execution loop**. The trusted runtime does not prescribe an intellectual fix.

The **trusted broker** independently determines whether the call is authorized, whether a known outcome permits retry, whether an external effect remains uncertain, whether an MCP service/account is cooling down, and whether existing budget/resource and phase permissions admit the next attempt. An error result is not a high-priority system prompt and cannot elevate privileges.

**No routine user prompts or user confirmation for tool failure/retry, backoff or ordinary troubleshooting.** Existing owner-approved Project Contract, budgets, data-egress consents, permissions and scope remain unchanged. If additional authority would be required, **do not invent or silently grant it**: return `BLOCKED` with the actionable limitation, let the member continue other authorized work or honestly record an incomplete outcome. This policy does **not** repeal existing explicit user authority for an actual new requirement, changed permissions, protected budget top-up or external action.

**No arbitrary hard ceiling on agent retry attempts** for a recoverable problem. An agent may reattempt after cooldown, repair or reconciliation as long as the action remains safe and authorized and available time/phase/budget/resource limits allow. This is **not** unconditional infinite automatic polling, unlimited provider spending, mandatory perpetual attempts, or permission to repeat forbidden/uncertain effects.

## 2. Error categories and agent-facing behavior

| Observed class | Model-facing outcome | Next-action rule |
| --- | --- | --- |
| Deterministic local/code/argument/test failure (e.g. Python NameError, invalid tool argument, failed test) | `FAILED`, concise actual error, permitted correction hint | **No infrastructure cooldown required**. Agent may correct/replan and submit a **new authorized, changed** call promptly. Repeating the identical bad arguments is not useful and need not be dispatched. |
| Temporary MCP service or connection overload, rate limit, known transient upstream failure | `RETRY_LATER` with scoped service, next eligible retry time and explanation | **3–7 minutes initial cooldown** (180–420 seconds) before safe retry; longer server `Retry-After` wins. Repeated transient problems use increased backoff and rate/admission limits. No arbitrary attempt-count cutoff; agent may select other work while waiting. |
| Provider/model inference transport failure before complete model reply | Record uncertainty and provider-native recovery status in canonical operation, not a fabricated tool reply to a model that is absent | Existing Step 5/7 reservation, epoch, safe continuation/retry rules apply; a missing model response cannot be given an imaginary tool result. |
| Known failed external write with evidence of **no** effect | `FAILED` or `RETRY_LATER` when service is transient | Retry or repair only under current authorization, target preconditions and idempotency/operation receipt semantics. |
| Tool timeout, partial response, lost ACK or crash after possible consequential write | `UNKNOWN_PENDING_RECONCILIATION` or `BLOCKED`, with no claim of failure | No duplicate dispatch solely because 3–7 minutes passed. Existing Step 5 verifier/probe reconciles the original effect; retry only after a **proved non-effect** or a provably safe idempotent continuation. Dependent operations remain blocked; unrelated permitted work can proceed. |
| Denied permissions, revoked grant, prohibited egress, unapproved tool, protected budget exhaustion | `BLOCKED` with the specific nonsecret reason | No cooldown makes this permitted. Do not resubmit identical forbidden effect to bypass policy. Agent can try **different authorized work** or report the limitation; changes to authority are outside this retry policy. |
| Persistent MCP state/credential/isolation defect | `BLOCKED` or `RETRY_LATER` only when a safe transient recovery path is observed | Never keep using shared unsafe state. Preserve ADR-46 member isolation, and isolate or disable affected connection/server when required. |

A model's preferred next action is a **request**, not an execution permit; every attempt gets current per-call validation. Do not convert a failure into false PASS/KEEP or let routine faults force an outer strategic rethink. Material evidence against the approach may still escalate under ADR-45.

## 3. Cooldown defaults and ownership

- **Initial transient MCP cooldown: configurable 180–420 seconds** for the affected MCP integration/endpoint and relevant tenant/account/credential scope, not all Council members globally. Select a value in that interval by a simple stable configuration or bounded jitter; never retry *earlier* than 180 seconds under the default policy.
- **Respect a provider/server-required longer delay** (`Retry-After` or equivalent), and apply longer backoff after repeated transient failures. Recheck tool health, permission epoch, grant, source target, budget and Step 7 resource admission before each attempt; a timer expiry is **not an authorization grant**.
- **Do not pause unrelated tools or tenants** because one scoped service is cooling down. An agent may do independent tasks or safely yield its existing Step 7 whole-member slot. Other members may still use an independently healthy isolated service/account scope.
- **Reuse the existing operation record, attempt history and next-eligible retry timestamp**, outbox/claiming mechanism and existing host scheduler. **No new service, agent queue, retry supervisor, experimental scheduling mechanism or timer database is authorized**. Do not keep a model or Docker worker actively spinning/sleeping simply to watch the clock.
- **Preserve the Step 7 distinct container/host recovery policy** (including its finite infrastructure-restart retry guidance). The owner's **no arbitrary tool-attempt cap** applies to agent-directed **safe tool correction/transient MCP retry**, not infinite Docker resurrection or privileged host remediation.
- Repeated retry attempts **consume relevant approved budget/operation capacity** unless same-charge idempotency is actually proven, and cannot borrow protected review or other scopes. If exhausted, mark `BUDGET_EXHAUSTED / INCOMPLETE`, not an invisible top-up or success.
- A cooldown does **not** eliminate external effect uncertainty, prove a network cancellation, grant access or authorize a previously disallowed retry.

## 4. Minimal trusted tool-result format

The trusted broker constructs a bounded error result, mapped through the matching provider adapter to the exact originating `model_request_id` and `provider_tool_call_id`:

```json
{
  "tool": "approved_tool_id",
  "status": "RETRY_LATER",
  "error_code": "MCP_TEMPORARY_UNAVAILABLE",
  "summary": "Service temporarily unavailable",
  "retry_allowed": true,
  "retry_after_seconds": 300,
  "retry_not_before": "server-derived timestamp",
  "guidance": "Retry this scoped service after cooldown, or continue other permitted work.",
  "operation_id": "original scoped operation reference"
}
```

Fields `retry_allowed`, `retry_not_before` and `guidance` are **trusted runtime interpretations of the verified observed effect and policy**, not instructions supplied verbatim by an untrusted MCP tool. User-visible/audit state retains full error class, actual attempts, budget, current pending effects and blockers; **normal debug noise need not interrupt the user**, but material uncorrected limitations must remain reportable and cannot be hidden in final artifacts.

Status `RETRY_LATER` is a **presentation/admission classification** layered on current canonical `FAILED/BLOCKED/UNKNOWN` and `next_retry_not_before` operation records. It must **not** silently invent a new canonical success status or overwrite the exact Step 5/9 effect truth. The broker still reports actual tool status and any known uncertainty; native provider continuation must respect ADR-46 call ID/order constraints.

## 5. Future acceptance tests — ALL NOT RUN

| ID | Scenario | Required outcome |
| --- | --- | --- |
| P9-30 | Python syntax/runtime error or bad tool arguments | Actual concise failure, model may repair immediately; no mandatory 3–7-minute wait |
| P9-31 | MCP overload/rate limit | Service/account-scoped retry_not_before 180–420 s or longer server-requested delay; no earlier dispatch |
| P9-32 | Two seats use unrelated tool integrations while one cools down | Unaffected authorized independent work proceeds; no new global bottleneck |
| P9-33 | Transient failures repeat without arbitrary fixed retry count | Extended backoff and existing hard budgets/permissions/resource caps respected; no busy-loop or infinite privileged restart |
| P9-34 | External non-idempotent write times out, ACK lost, delayed success | UNKNOWN stays; reconcile before any retry regardless of elapsed cooldown |
| P9-35 | Revoked credential, forbidden egress or exhausted budget during cooldown | Revalidation denies retry; agent cannot gain user authority from failure text |
| P9-36 | MCP error text contains malicious 'ignore policy' instructions | Sanitized bounded error remains untrusted data; no priority/prompt injection |
| P9-37 | Model provider fails before tool-error continuation can be delivered | Canonical operation/recovery state retained; no fabricated model receipt |
| P9-38 | Model/tool context rollover and out-of-order retry results | Correct original actor/epoch/call ID delivery, no double dispatch or cross-member leakage |
| P9-39 | Repeated failures without user interaction | No automatic routine user-approval interaction; important unresolved blockers accurately surfaced in authorized progress/final report |

Tests are specified only: live MCP/provider behavior, rate limits, authorization, idempotency, saved timers, resource usage, concurrency and failure injection must be measured later during explicitly authorized implementation/verification.

## 6. Scope boundary

**ADR-47 policy APPROVED and documented.** Step 9 overall remains **IN DESIGN** pending remaining owner-reviewed operational details. **Implementation NOT STARTED, tests NOT RUN.** Do not mark tool recovery, concurrency isolation, or performance as operational solely because a Markdown design was pushed.
