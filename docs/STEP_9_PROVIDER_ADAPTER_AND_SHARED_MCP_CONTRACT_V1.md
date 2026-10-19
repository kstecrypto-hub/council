# Step 9 — Model providers, unified gateway and shared MCP/tool contract v1

**Owner-approved architecture decisions: October 19, 2026. Status: DESIGNED as a v1 specification only. Implementation NOT STARTED; provider compatibility, security, runtime and MCP integration tests NOT RUN.** This specification implements the design intent of [Step 9](MVP_SCOPE_BY_STEP.txt), [models and provider controls](APP_DESIGN.md), [Steps 3–5 atomic/typed operations](STEPS_3_TO_5_EXACT_INTERFACE_CONTRACT_V1.md), [Step 7 budgets/resources](PART_7_MEMBER_SCHEDULING_RECOVERY_RESOURCES.md), [Step 8 action protocol](STEP_8_ACTION_AND_FINALIZATION_CONTRACT_V1.md) and [local-source consent](STEP_2_SNAPSHOT_TRANSFER_CONTRACT_V1.md). **It does not create a working model gateway, MCP server, adapter, provider connection, or any tested provider compatibility claim.**

## 1. Approved decisions and non-goals

1. **One trusted model gateway**, with narrow provider adapters for DeepSeek, OpenAI and Anthropic as the initial remote MVP scope; compatible customer-approved local inference is an optional fourth adapter subject to real host, context and tool compatibility. Additional providers require adapter qualification, not a Council redesign. No exact model IDs or vendor-specific guarantees are presumed current without implementation-time validation.
2. **Per-original-seat configuration**, inheritable by workers with explicitly authorized per-worker overrides. The Project Orchestrator and persistent non-voting Final Integrator each have separate configuration identities and chargeability scopes; neither becomes a sixth reviewer. Do not invent model-company independence when the user selects the same model for all five.
3. A **small capability registry with measured checks**, not an unbounded automatically trusted model catalog or vendor-claim-as-proof.
4. **BYOK/direct provider billing** for remote inference; compatible local models need no remote provider key. Secrets belong to trusted secret storage, never an agent sandbox, Git, chat, log, client persistence or model prompt. Five user-approved protected spend scopes remain in force; the deprecated 70/25/5 default is not reintroduced.
5. **Explicit checkpoint-safe switching**, separately authorization-checked and versioned. The MVP need not provide live arbitrary-turn migration UI. No silent provider/model fallback and no arbitrary provider reasoning-state transplant.
6. **No extra agent queues, new intellectual supervisor, automatic model scoring, managed Council token wallet or speculative provider-specific orchestration.** Step 7 retains whole-agent slot scheduling and provider/local-inference admission limits; Step 5 retains operation idempotency, UNKNOWN reconciliation and transactional budget reservations.
7. **One shared Council tool/MCP infrastructure, not one MCP server for each LLM.** Step 9.3 capability checks decide whether a model can use a tool-call protocol; the gateway plus trusted tool broker/MCP client does the actual translation and execution. No agent/model gets a direct, unmediated network connection or privileged credential to an MCP server.

## 2. Minimal architecture and placement

Logical data flow:

\`\`\`text
Council actor (Member 1..5 | Orchestrator | Final Integrator | authorized worker)
  -> existing typed Council bridge (authenticated actor + current epoch/Contract)
  -> trusted Model Gateway (source/data/egress authority, phase spend admission)
       -> selected Provider Adapter (OpenAI | DeepSeek | Anthropic | supported Local)
       <- normalized model output / tool-call proposal / metering
  -> existing trusted Council Tool Broker (never executing from model text alone)
       -> native vetted tool adapter OR Council-managed MCP client
             -> one or more approved, scoped MCP servers (Git, database, search, etc.)
       <- scoped observed tool result / denial / UNKNOWN
  -> selected Provider Adapter continuation (same native session protocol)
  -> existing Step 5 event/operation ledger and Step 6 evidence provenance
\`\`\`

**Placement:** model gateway, credential resolver, MCP client/connection management and privileged tool broker live outside all agent-controlled containers in the **existing trusted control application**. A provider adapter is code/module, **not a per-model MCP server or autonomous Council agent**. MCP servers are integrations representing *tool services*, not models. A tool service may require a separate MCP server instance/connection per customer, tenant, scoped user, source or session **if isolation demands it**; that is not a separate server *per AI model*. Some tools may use native trusted adapters without MCP at all. Standardize their admission/evidence surface through the same broker.

**Remote-provider-native hosted tool features:** do not allow a provider's direct connector/MCP/internet tool path to bypass Council's data-egress, tenant, audit, spend or exact-source permissions. Either route tool execution back through Council's trusted broker or mark that native hosted tool capability **unsupported for sensitive Council operations** pending a separately authorized gateway-controlled architecture. Exposing a remote model to an MCP server is never automatic consent for source egress.

## 3. Configuration, inheritance, actor identity

**Resolution order for Member/worker:** workspace default -> run default -> original member seat override -> member worker-class/default override -> expressly authorized individual worker override. For **Orchestrator** and **Final Integrator**, use their own run-scoped configuration, with workspace/run fallback where approved, not an inherited sixth-seat setting. Version every resolved profile; store \`effective_model_profile_revision\`, inheritance/source, \`provider_id\`, exact \`model_id\`, \`adapter_version\`, compatible \`context_profile\`, required capabilities, approved tool/data policy, sampling/reasoning options and provider secret **reference** (never secret bytes). Model settings belong to a logical actor; session instance IDs/epochs may change across context rollover without changing author attribution.

- Freeze the effective model profile for each **authorized model operation**. Attribute resulting proposal, decisions, tool requests, evidence, token/cost outcome and provider call IDs to the actual model+adapter+configuration version. No retroactive re-attribution after a setting change.
- Initial selections may all use DeepSeek **only if the user chose/approved that setup**. Show clearly \`same-model Council\` rather than an implied five-model diversity; equally preserve same-company/different-model and different-provider configurations truthfully.
- A provider/account credential is bound to authorized \`(customer, deployment, provider, allowed roles/scopes)\` and its current revocation generation. Workers inherit authority **no broader than their parent**; they never inherit raw keys or global MCP server permissions.
- User-selected default tool access still requires source-specific consent, per-recipient grants, current role and exact content/retention purpose. Passing a language model's capability test does not make previously forbidden tools or data allowed.

## 4. Unified Model Gateway v1 request, response and continuations

Canonical request **design DTO** (fields mandatory unless marked optional):

\`\`\`text
ModelRequestV1 {
  request_id: uuid, command_id: uuid, run_id: uuid,
  actor_kind: ORIGINAL_MEMBER|WORKER|ORCHESTRATOR|FINAL_INTEGRATOR,
  logical_actor_id: uuid, parent_member_id?: uuid, execution_epoch: bigint,
  phase_id: uuid, phase_generation: bigint, contract_revision_id: uuid,
  model_profile_revision_id: uuid, provider_id: string, model_id: string,
  conversation_snapshot_ref: opaque_customer_local_ref,
  allowed_data_classes: string[], approved_model_egress_policy_version: uuid,
  exposed_tool_manifest_id?: uuid, required_capabilities: string[],
  limits: { max_input_tokens?, max_output_tokens, max_cost_minor_units,
            rate_admission_class, tool_loop_max_consequential_effects? },
  budget_scope: MEMBER_WORK|CHECKPOINT_COMPARISON|INTEGRATION|
                POST_INTEGRATION_VALIDATION_PREMORTEM|ORCHESTRATION_REPORT_ARCHIVE,
  correlation_id: uuid, parent_operation_id?: uuid,
  idempotency_key: string
}
ModelObservationV1 {
  request_id, provider_id, model_id, model_profile_revision_id, adapter_version,
  actual_provider_request_id?, continuation_handle_ref?,
  status: SUCCEEDED|BLOCKED|FAILED|UNKNOWN_PENDING_RECONCILIATION,
  output_ref?, normalized_content_parts[], proposed_tool_calls[],
  stop_reason: COMPLETED|TOOL_CALLS|MAX_OUTPUT|CONTENT_FILTERED|PROVIDER_STOP|
               INTERRUPTED|UNKNOWN,
  usage: { input_tokens?, output_tokens?, cached_input_tokens?,
           reasoning_output_tokens?, units_source: PROVIDER|LOCAL_ESTIMATE|UNKNOWN,
           is_final: boolean },
  cost: { pricing_revision_id?, reserved_minor_units, settled_minor_units?,
          currency, uncertainty: NONE|ESTIMATE|UNKNOWN },
  timing: { started_at, ended_at?, provider_latency_ms? },
  provider_metadata_ref?: opaque_restricted_ref,
  event_position?, error_code?, raw_response_hash?
}
\`\`\`

Actual providers' HTTP bodies, SDKs, streaming chunks, tool-call shapes, cache hints, reasoning-mode settings, tool result injection and provider-request IDs remain **adapter-private** and must not be forcibly converted to a pretend universally supported option. The common contract promises only fields actually observed; unknown token usage, cost or finality remains explicitly \`UNKNOWN\`, not zero or PASS. Store only permitted provider metadata and relevant usage; do **not** turn private reasoning traces, hidden chain of thought, prompt transcripts or provider-specific continuation blobs into Council peer evidence or a final “explanation.”

**Supported adapter functions (design signatures):**
- \`discoverModels(account_scope) -> untrusted_catalog_snapshot\`: optional; discovered IDs are not by themselves approved capability entries.
- \`validateProfile(profile, required_caps, current_customer_policy) -> verified|blocked|unknown with evidence\`.
- \`buildRequest(ModelRequestV1, current_authorized_context, exposed_tools) -> provider_wire_request\`.
- \`execute/stream(provider_wire_request, secret_capability, operation_id) -> provider_parts, provider_request_id, usage, uncertainty\`.
- \`parseToolProposals(parts) -> normalized_proposals\`: tool requests are **untrusted proposed actions**, never executable just because the provider returned them.
- \`buildToolContinuation(previous_same_provider_session, broker_observed_tool_results) -> provider_wire_request\`; preserve provider-required native tool-call IDs, roles, ordering and opaque continuation state **within the same provider/model session**.
- \`classifyErrorAndRetryability(raw_error, headers, wire_state) -> deterministic_classification\`.
- \`normalizeUsageAndPricing(...) -> actual|estimated|unknown\`; separately attributed cached/reasoning tokens where provider reports them.

**Provider continuation rule:** DeepSeek thinking-mode/tool-result specifics, OpenAI response/tool-call IDs and Anthropic message/tool blocks are each handled by the **matching versioned adapter**. The gateway must not drop native continuation fields needed for correct follow-up, nor expose those opaque fields to other members. This is a correctness requirement with explicit future integration tests, **not a claim that any listed vendor currently offers a particular model feature.**

**Tool-loop guard:** One response may propose zero/multiple calls. The broker authenticates, authorizes, logs and executes each individually under current scope, not from a raw freeform string. If any consequential tool is UNKNOWN, reconcile or block dependent continuation; do not hallucinate a succeeded result. The model consumes the observed typed tool result or explicit denial; it cannot authorize a hidden second action.

## 5. Registry, compatibility, cost and real capability gates

Small versioned model registry row:
\`provider_id, model_id, adapter_version, verified_at, credential_scope_ref, pricing_revision_id?, region/data-residency constraints?, context_window?, max_output_tokens?, accepts_tools?, parallel_tools?, structured_output?, image_input?, tool_result_continuation?, reasoning_mode_profile?, usage_reporting?, caching_profile?, supports_provider_request_id?, stop_reason_map?, probe_evidence_refs, customer_data_permissions, status=UNVERIFIED|QUALIFIED|DEGRADED|REVOKED\`.

Separate **vendor-advertised**, **configured policy**, and **actually verified** capability fields. Discovery alone cannot mark QUALIFIED. Required model capabilities are task-specific; Step 8 member ACT with tools requires confirmed native tool-call and result-continuation behavior; a local **text-only** model can be allowed for explicitly text-only support work but must not be silently assigned tool-dependent Council execution or counted as qualifying for all members. Non-code projects may require other capabilities; no mandatory image support for every role.

Initial adapter qualifications (not pre-certified):
- **DeepSeek adapter**: test current model ID, ordinary and reasoning-mode tool continuation including restart, usage and price reporting, context limits, rate/timeout, privacy/egress and refusal handling.
- **OpenAI adapter**: test selected currently supported model ID, applicable tool-call/continuation interfaces, reasoning options when truly supported, usage/cache reporting, request idempotency where supported and source/egress constraints. The hosted **Moderation API** is a *separate approved safeguard capability*, not an implicit substitute for tool permissions.
- **Anthropic adapter**: test tool-use/result ordering, prompt-cache/usage fields when supported, extended reasoning/continuation when supported, context/output limits, request identity, consent and cost guards.
- **Local-model adapter**: choose a customer-approved local inference backend only after confirming **actual selected model/runtime/quantization/context/tool loop** compatibility; measure RAM/VRAM and host headroom. Step 7 initially allows **one shared active local inference job**; that cap is for the shared gateway, not internal worker population. Do not claim that any given GPU can support any unspecified model or context.

For any high-impact mismatch, mark \`UNVERIFIED\` or \`DEGRADED\`, not silently substituting another provider. Treat late vendor changes to model behavior, tokenizer/cost formulas or request policies as versioned registry revisions requiring requalification of affected features. Honor provider-specific throughput, account limits, rate-limit headers/Retry-After and measured dynamic concurrency. Step 7 approved **up to two remote in-flight calls per provider** initially; lower ceilings may be needed. Do not invent deterministic latency, output size or reasoning quality.

### Exact budget policy and usage settlement

Every remote/local model call:
1. Resolve actor, parent, current approved Contract/policy/credential/egress/model profile and **one** of the five protected chargeability scopes.
2. Check model context and output ceiling, precompute a conservative authorization bound using input size, maximum allowed output, chosen provider pricing revision, cached-token treatment **only where the bounded bill can be justified**, and any currency assumptions; reserve against Step 5 run, pool, member/phase or Integrator ceilings under canonical event-clock-first locks. If cost cannot be bounded, reject for new approval/configuration instead of assuming cost=0. Local models still consume explicit token and resource caps.
3. Commit operation intent/reservation/event/outbox **before** provider dispatch. Provider requests and MCP/tool effects occur outside SQL locks.
4. Settle final provider-reported usage/cost with exact version/source and uncertainty labels. Incomplete streams, missing usage or connection loss preserve reservations/UNKNOWN liability until reconciled; cached tokens/reasoning tokens are separate when available. Council budgets limit **its authorized dispatch**, not all charges to user's external provider account.
5. On provider rate-limiting, use existing operation retry policy (initial Step 7 infrastructure retries, configurable), **only** where retry is safe after detecting probable/actual dispatch and idempotency conditions. A lost response is not automatically evidence that request was not billed. No additional per-key/API queue.

## 6. Shared MCP/tool infrastructure — precise ownership

**Answer to the owner's explicit Step 9 question:** **NO PER-MODEL MCP SERVER IS REQUIRED.** Capability registry (9.3) verifies whether each model can express/read tool calls; the unified gateway translates those native calls. **Council's existing trusted tool broker acts as the single policy and execution entrypoint** and its MCP client(s) communicate with approved MCP **tool servers** as needed. A server corresponds to an integration/tenant/scope, not to an LLM vendor or individual model. One vetted Git/DB/search tool integration can serve all five Council original seats, the Orchestrator and the Final Integrator **with distinct independent per-actor permissions**.

A native Council tool and an MCP tool have the same *trusted admission boundary*, but are not required to have the same transport. Normative tool registration:
\`{tool_id, tool_origin=NATIVE|MCP, server_registration_id?, server_identity, server_scope, operation_name, schema_version, schema_sha256, tool_description_hash, effect_class=READ_ONLY|IDEMPOTENT_WRITE|NONIDEMPOTENT_WRITE|EXTERNAL_PAYMENT_OR_EGRESS, accepted_data_classes, permitted_actor_roles, permitted_run_and_phase_scopes, requires_user_approval, egress_destination, idempotency/reconciliation_strategy, observed_health_version}\`.

Tool publishing/execution steps:
1. **Trust-on-register**: an admin/customer policy explicitly approves connector/server identity, origin and scopes. MCP discovery/list-tools is **untrusted metadata**; descriptions, schema updates, prompts/resources from MCP servers never grant privileges or expand the agent's prompt authority. Pin an approved schema/content hash and fail capability-closed on unexpected change until revalidated. Existing client/server transport auth is scoped; no direct model credential.
2. **Per-model exposure**: construct a *filtered* \`ExposedToolManifestV1\` for the current actor, phase, allowed current grant/source/data classes, model-adapter capability and user approval. Expose only the tools the **specific member** can use, even though the same server is reused across members. Do not expose raw server-origin text as high-priority instructions.
3. **Proposal normalization**: provider adapter parses its native tool proposal into \`ToolProposalV1 {model_request_id, provider_tool_call_id, approved_tool_id, schema_sha256, canonical_arguments, expected_run, parent_actor_ref, phase, command_id, idempotency_key}\`. The provider cannot nominate an unlisted MCP server, new endpoint, forbidden file path, arbitrary credentials or root authority.
4. **Broker authorization**: independently authenticate current trusted Council actor/epoch, contract, allowed resource/source/recipient, per-tool effect class, explicit user policy, data egress, moderation where applicable, cost/usage budget, and external-effect reservation. An MCP tool's advertised capabilities or prior model ALLOW are *never* sufficient.
5. **Observe results**: broker dispatches a typed, bounded call to the approved tool/MCP server; a trusted observed result includes \`operation_id, attempt_id, approved_tool_id, schema_sha256, content_hash, effect_status, provenance, source_grant_epoch, egress_destination, uncertainty\`. MCP tool error/timeout/partial result is explicitly FAILED/UNKNOWN; model summaries are not observed effects. Unknown consequential MCP writes require Step 5 effect-specific reconciliation before retry.
6. **Return to provider**: convert the broker's observed result/denial into the selected model's native tool-result syntax with exact originating tool-call identity, respecting adapter-native ordering/continuation. Do not auto-send a peer chat message, leak a credential, attach private data to another member, or promote an MCP-provided prompt to a system instruction.
7. **Closure and revocation**: cancel/fence active tool authorizations when source grants expire or checkpoint review closes. Verify external access revoke where required, and maintain outcome/UNKNOWN records as Step 2/5 require. Existing Step 7 scheduler controls whole-agent execution; **no MCP-specific agent scheduler, duplicate per-model server fleet or new queue**.

**MCP client sessions are not equivalent to model sessions.** Multiple scoped MCP client connections or isolated server instances might be necessary for different customer secrets/permissions; this is correct and does **not** contradict one shared Council tool architecture. Any server-specific OAuth credentials remain in the trusted connector secret boundary and are never inherited by models/workers; all source/data egress through remote MCP is separately consented.

**Tool protocol fallback:** if a model lacks functioning native tool calling, Step 9.3 must mark the capability unavailable and Council must not fake tool use from untrusted prose or execute unparsed commands. An explicitly approved, independently verified restricted mediation mechanism may be designed later; not part of MVP. A model may participate in approved text-only reasoning/reviews if its specific role requires no tool operations, but cannot be deemed general-purpose tool-capable.

## 7. Provider loss, model switching and cross-provider consent

**Normal continuity** uses provider-native session/continuation with the *same* model profile version; do not assume reasoning or cache state is portable across providers. Context rollover follows Step 11 bounded evidence/continuation packets but never changes logical seat, material authored opinions or provenance.

**Switch request v1:** \`QueueModelSwitch {actor_id, effective_model_profile_revision, proposed_provider/model/adapter, requested_checkpoint_generation, reason, required_capabilities, current_source_egress_policy, expected_model_profile_revision, user_approval_id}\`. It is a **user-authorized configuration revision**, not permission for a model or Orchestrator to switch itself.

- **Prepare**: before exposing the new model, verify current credential/provider account, updated data-egress consent and new jurisdiction/destination, capability probes, model version, context profile, pricing/pre-dispatch limits, user-approved five-pool budget and expected phase/checkpoint scope.
- **Safe boundary**: during initial MVP, only apply when the current actor is *not* in the middle of unresolved model/tool/provider effects, sealed assessment, result-ready freeze, running verification or an active checkpoint discussion obligation. It can be queued to an actual verified checkpoint or another trusted quiescent **phase boundary**, after old epoch is fenced and authorized grants/transport are updated. A normal checkpoint's read-grant revocation remains obligatory.
- **Handover**: create a scoped, content- and provenance-hashed factual handover from permitted canonical sources, decisions/objections, work artifacts, pending unknown effects and next obligation. Do not pass opaque private reasoning blobs, assumed incompatible provider IDs, private member information, undisclosed peer sealed reviews or raw external credentials.
- **Apply**: atomically version the logical actor's effective model profile and new session epoch, retain old model profile/usage attribution as immutable history, reissue only new current authorized capabilities, then resume **the same logical member/integrator**.
- **Failure**: if the new model is invalid, not permitted, lacks required tools or uncertain cost, keep the original safe state or block with explicit user-visible cause. Automatic model/provider fallback remains **not authorized in the MVP**; a later fallback policy would need explicit opt-in, data-consent boundaries and cost authorization.

Initial MVP can ship with selection **at run start** and the ability to record/defer switch intent safely; automatic mid-stream migration and a fine-grained switching UI are **deferred**, as the existing Step 9 scope permits. A switch must never silently change one of the five original reviewers, fabricate independent opinions or turn a different provider into an extra member.

## 8. Exact qualification, tool/MCP security and failure scenarios — planned, NOT RUN

| ID | Scenario | Expected outcome |
| --- | --- | --- |
| P9-01 | Each supported remote adapter parses ordinary reply and native tool-call continuation | Correct attributed normalized tool proposals, stop/usage handling, provider-native continuation |
| P9-02 | DeepSeek reasoning, OpenAI tool continuations, Anthropic tool results (current supported model versions) | Versioned adapter retains required opaque native fields; no fabricated universal reasoning format |
| P9-03 | Same registered MCP Git tool exposed to Member 1 and Member 2 with different grants | One broker/server integration, independently enforced read scopes, no cross-seat workspace leakage |
| P9-04 | Tool server advertises new tool/schema or malicious text in description | No automatic permission escalation; deny/requalify registry schema; no prompt-authority promotion |
| P9-05 | Model emits raw shell, unlisted tool ID, forbidden peer path or fake \`actor_id\` | No execution; policy authorization comes only from current trusted session/manifest |
| P9-06 | Model has text generation but no demonstrated tool-call continuation | Mark unsupported for tool-dependent Council ACT, may qualify only for permitted text-only roles |
| P9-07 | MCP server timeout after potentially consequential write | Step 5 UNKNOWN and reconciliation, no blind duplicate write/provider charge |
| P9-08 | Remote model timed out after billable call, actual usage unknown | Retain conservative reservation; do not mark cost=0 or assume provider request cancelled |
| P9-09 | Same provider key shared across workers, but worker asks forbidden tool | Worker cannot expand parent/source/tenant permissions or access raw secrets |
| P9-10 | Initial five seats use identical model, Orchestrator and Integrator have different models | Correct six/seven configuration actor attributions, **five reviewer seats only**, explicit same-model Council label |
| P9-11 | User requests model change mid-active tool loop or sealed review | Queue/reject until safe boundary; never transplant raw provider state or invalidate existing five review identities |
| P9-12 | Provider switch would send confidential customer files to a newly selected provider | Require current distinct approved data-egress consent; BYOK alone insufficient |
| P9-13 | Model known but context/output/tool capability check fails | Block only affected operation; no silent fallback or fake QUALIFIED label |
| P9-14 | Cached tokens or reasoning tokens not reported by provider | Correct unknown/conditional accounting; no assumptions about provider billing |
| P9-15 | Five budget pools: Integrator attempts to debit reserved five-review budget | Reject without borrowing; retain correct run/parent and provider limits |
| P9-16 | Approved local backend has insufficient VRAM for requested context/tool model | Block/degrade capability; maintain Step 7 one-job initial cap and measured host headroom |
| P9-17 | MCP tool response contains attempted instructions and secret exfiltration URL | Treat as untrusted tool data, apply deterministic provider/tool/source egress checks; cannot become authority |
| P9-18 | Provider or MCP credential revoked or data grant expires between proposal and execution | Deny new tool dispatch and dependent continuation, preserve audit and reconcile uncertain work |

**Verification rule:** These are **design acceptance cases, not executed tests**. A real PASS needs actual adapter+gateway+MCP tool instance and authenticated run, provider version/date, fixture, observed event/receipt evidence, output hash, rate/usage accounting and negative access probes where appropriate. Provider docs/model availability must be checked again at implementation time. Council runtime, native tool adapter, MCP client/server connections, provider contracts, UI, pricing/live token-metering and all tests remain **NOT STARTED / NOT RUN**.

## 9. Design versus implementation completion boundary

**DESIGNED** means the approved v1 ownership, actor inheritance, provider interface, registry fields, shared tool/MCP boundary, preflight authorization and cost handling, switching gates, failure semantics and verification matrix above are specified. It **does not** mean OpenAI, Anthropic, DeepSeek or a local engine has been connected, that any current model actually passed tool-use probes, that an MCP server was installed, or that a safe live inference cost/profile exists.

Implementation next requires selecting exact currently available model/SDK/HTTP versions, secret storage, customer egress/provider choices, actual tool integrations, any customer-approved local runtime and measured resources, migrations, adapter code, capability probes, event/usage settlement and the tests above. Implementation and runtime tests are a **separately authorized later task** under the unchanged Council plan.

## Official MCP protocol reference (implementation-time check)

The [MCP 2026-07-28 host/client/server architecture](https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/docs/specification/2026-07-28/architecture/index.mdx) confirms that a host can manage **multiple clients**, with **each individual client connecting to one server**. This is a **host-to-tool-service** relationship, not a unique client/server pair mandated for every language model. An authorized shared tool server can be reused through Council-managed scoped client connections without transferring a member's permissions to another member. Use the [current MCP authorization specification](https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/docs/specification/2026-07-28/basic/authorization/index.mdx) for transport-specific scoped credentials; keep STDIO/HTTP credential behavior distinct. Provider adapters remain unrelated to the one-client-to-one-server MCP relationship. Confirm the latest compatible MCP SDK/protocol version at actual implementation time.
