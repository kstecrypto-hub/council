# ADR-51 — Step 9.3 lightweight model tool-interface compatibility probe

**Owner approved October 21, 2026.** This closes the **Step 9.3 probe-method policy**, not all Step 9 operational design. **Policy APPROVED; gateway/adapter/probe harness implementation NOT STARTED; no remote provider/local inference/probe/security/runtime tests RUN.** See [Step 9 gateway and MCP contract](STEP_9_PROVIDER_ADAPTER_AND_SHARED_MCP_CONTRACT_V1.md), [ADR-47 model-neutral peer selection](STEP_9_ADR47_OPEN_ENDED_PEER_MODEL_SELECTION.md), [ADR-46 tool ordering/isolation](STEP_9_ADR46_TOOL_CALL_ORDERING_AND_MCP_ISOLATION.md), [ADR-48 error handling](STEP_9_ADR48_AUTONOMOUS_TOOL_ERROR_FEEDBACK_AND_COOLDOWN.md), [Step 5 durable operations/budgets](PART_5_TRANSACTIONS_IDEMPOTENCY_CONFLICTS.md) and [Step 10 execution boundary](MVP_SCOPE_BY_STEP.txt).

## 1. Purpose — protocol compatibility, NOT intelligence or permission scoring

Major API models commonly offer tool calling, and many instruction-tuned local models can use a compatible inference runtime/parser. Council should **not** develop a heavyweight intelligence benchmark, ranking service, model chooser, or general-purpose “is this model smart enough?” gate.

Step 9.3 asks only whether the **selected, exact model + versioned provider adapter** actually communicates using Council's supported tool-call and result-continuation protocol. Local model compatibility depends additionally on **actual runtime, served model/quantization, chat template and tool parser**, which may differ despite the model-family name. Provider-advertised features alone do not prove the chosen adapter works.

- **Model technical capability:** supported native/adapter tool call syntax, arguments, call identity, provider-specific result continuation and small failure-result continuation; read-only declared context/output/feature limits and reported usage.
- **Member intellectual autonomy:** no model-quality score, task-complexity classification or restriction on which hypothesis/code/problem an agent may attempt.
- **Execution/security:** Step 10's sandbox lets an agent choose local work within its bounded environment; the existing Step 5/9 broker and external isolation enforce access to credentials, MCP/network/other-member/private/host resources **outside** its authorized sandbox. A successful probe is not an authorization grant and does not add a separate sandbox policy system.

## 2. Small deterministic simulated-tool protocol

Council's **existing trusted model gateway**, when explicitly configuring a model/profile or when a relevant version changes, runs an isolated, low-cost *synthetic* tool conversation against that **actual provider/model/adapter** using provider-native tool messages. It supplies a temporary, local `council_probe_echo` tool schema; **no Git, database, customer source, real MCP service, filesystem or external side-effect tool is invoked**. The fake tool is a built-in, deterministic harness result, not a new service, queue or Council agent. A probe definition cannot be exposed as an ordinary member tool or credential.

**Success path (one real model tool loop):**

1. Using an approved tiny token/spend cap and probe-scoped context, ask the model to call `council_probe_echo` with `{"value":"12345"}`. Normal provider-native tool calling is used, not freeform shell, simulated assistant prose or an invented tool-call object.
2. The versioned adapter returns an authentic structured provider tool proposal. Council checks **tool ID, real provider tool-call ID, exact tool name, parseable schema-valid arguments and original-request attribution**. If the model writes “I called the tool” as prose, that **does not pass**.
3. The fake tool receives the permitted argument and returns a freshly generated **unguessable challenge nonce that was not included in the model's input**, e.g. `{"received":"12345","nonce":"<random-challenge>"}`. No customer data or live service access is needed.
4. Council builds the *matching native provider* tool-result message using the **original tool-call identity and protocol-required session/response state**, then asks the same model session to output a plainly checkable short marker such as `PROBE_OK:<nonce>`.
5. Trusted deterministic code compares the response marker with the nonce **actually sent in the tool result**, and checks tool-call ID/order/session/protocol fields; **no second LLM judge or subjective intelligence evaluation**.

**Error path (separate equally small tool loop):**

- Expose an equally harmless fake error tool (or return a fake error for a probe invocation), and deliver a trusted tool-result payload `{"status":"FAILED","error_code":"SYNTHETIC_FAILURE","nonce":"<fresh-unseen-challenge>"}`.
- Verify native tool-result continuation accepts that attributed failed result and the model identifies the correct error/nonce using a fixed test marker such as `PROBE_ERROR:<nonce>:SYNTHETIC_FAILURE`. No real network error, MCP cooldown, retries, privileges or host side effect should be induced by this synthetic failure.
- Passing proves **this protocol fixture worked for this exact versioned configuration**, not that the model will intelligently troubleshoot all future errors, that all agent tool results are safe, or that provider capability can never regress.

Keep fixtures small and compatible with provider-specific native syntax; do not demand one universal wire protocol or a cross-vendor transplant of hidden reasoning/session handles. If a provider requires a batch of tool results, the adapter must respect its native correspondence; the MVP probe only proves the specific basic path exercised, not untested batch or multi-tool concurrency cases.

## 3. When and how to record results

Run the above **on initial model configuration/onboarding and on a relevant changed version/profile**, not before every agent call. Relevant changes include the model/API protocol or adapter version, provider tool-continuation format, and for local inference the actual model/quantization/runtime/template/tool-parser combination. A transient provider outage may produce `INCONCLUSIVE` and ordinary authorized recheck later; it is **not** proof that the model family fundamentally lacks tools. Protocol mismatch marks that exact capability unsupported for the selected configuration until corrected/rechecked; leave unrelated text-only capability available.

In the **existing versioned Step 9 capability registry** record enough provenance to avoid false guarantees: provider and exact model identifier/revision where available; adapter version; local serving runtime/model/quantization/template/parser identity when applicable; probe fixture version, time, observed native call/result IDs or secure references, success/error probe outcomes, limited failure classification, usage/cost, and nonsecret evidence/hash. The registry may separately record vendor-advertised context, output, images, structured responses, reasoning flags and reported limits. These are **declared/observed interface capabilities**, not a general skill score. Unknown or stale feature claims remain unknown/need recheck. Do not add new ontology tables, model-performance evaluators or periodic provider polling for this.

Remote probes **use actual paid model inference**, so they require current user-approved BYOK/configuration, per-call token/cost reservations and provider data-egress policy just like ordinary gateway calls. Keep tests low cost; never assume they are free. Local probes use the same customer-approved execution and measured resource/headroom limits. Failure may be due to adapter bug, runtime parser/template mismatch, model output variability, timeout, quota or incompatibility; record what was *observed* without asserting intellectual incapacity.

**Do not use the tool-compatibility probe as an alternate external permissions gate.** Once configured, an agent may attempt whatever reasoning/work it chooses inside its authorized isolated sandbox. Ordinary MCP and host-side access remains enforced by the trusted broker and sandbox boundary even if the model passed the probe. Do not add a Council-specific per-agent restriction layer.

## 4. Future acceptance scenarios — specified, NOT RUN

| ID | Case | Required observed result |
| --- | --- | --- |
| P9-40 | Supported adapter emits native echo tool request | Exact registered fake tool name, valid arguments, original call IDs observed; no actual MCP/host action |
| P9-41 | Fake tool provides fresh unseen nonce | Native result continuation succeeds and model echoes that exact nonce; no plaintext fake tool-call success |
| P9-42 | Fake error tool returns FAILED with code and nonce | Correct attributed failed result delivered; small deterministic response indicates failure without fake success |
| P9-43 | Model only narrates “I called a tool” | Probe does not pass because no structured native call occurred |
| P9-44 | Local runtime/chat template/tool parser mismatch | Version-specific failure, no claim that all models in the family lack tool calling |
| P9-45 | Provider timeout/rate limit during probe | Inconclusive/UNKNOWN as appropriate, observed cost reservation retained and no unsafe duplicate dispatch |
| P9-46 | Model/API/adapter or local runtime/template/parser changes | Existing versioned probe result no longer silently certifies the changed configuration |
| P9-47 | Ordinary subsequent model tool operation | No per-action probe/model scoring/extra memory-model tokens; real broker still authorizes external effects |
| P9-48 | Model tries a difficult task inside its sandbox | Qualification does not judge intelligence, ban strategies or impose new intellectual restrictions |
| P9-49 | Probe reports success but actual MCP tool has revoked grant | Real Step 9/10 broker denies external tool action despite model interface compatibility |
| P9-50 | Registry lists multiple vendors/model variants | No main/default model, no five-entry catalog cap, original five seats remain unchanged |

**Completion boundary:** These are planned **future integration tests**, NOT executed evidence. ADR-51 completes the owner decision on the *lightweight 9.3 probe method* only; Step 9 still requires owner review of concrete provider-native workflows, credential/egress/cost handling, connector isolation, switching and local execution before the overall design can be marked DESIGNED. **No implementation, executed provider or local model probe, reliability data or token-efficiency claim.**
