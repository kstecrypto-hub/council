# ADR-47 — Equal reasoning peers, no main LLM, open-ended model pool

**Owner approval: October 20, 2026.** This overrides historic DeepSeek-first/uniform-model setup assumptions. **Policy APPROVED; Step 9 overall IN DESIGN; implementation, actual provider qualification and runtime/comparative tests NOT STARTED / NOT RUN.**

## Fixed Council membership is not a model catalog limit

- Five **original logical Council members** are intellectually equal and independently accountable, with the same original-five checkpoint and sealed review obligations. No LLM is the main/lead Council reasoning model, and no provider can acquire special intellectual authority.
- The qualified provider/model catalog has **no arbitrary cardinality limit**: register five, ten or more currently supported LLM choices through validated adapters as demanded. A provider requires implemented, role-compatible tools, cost reporting, credentials and permitted egress to become usable. An unqualified entry is not a runnable model.
- Model count is **not** original seat count. Workers may use separately authorized qualified models; Orchestrator and Final Integrator have independent, non-voting configuration identities. Adding LLMs does not silently change five-member governance.

## Normal startup and permitted exceptions

1. Normally configure a **different capable, qualified, explicitly user-approved reasoning model for each original seat** from currently available choices. High-performing and task-suitable depends on current evidence and actual feature tests; no frozen "top five" ranking, brand preference or automatic scalar judge is authoritative.
2. No default DeepSeek, GPT, Claude or other provider/model is imposed globally or inherited silently by every original member. Provider-neutral workspace/run suggestions may assist configuration but cannot create an unapproved same-model Council.
3. An intentional same-model setup (such as a controlled evaluation) is permitted **only by explicit user choice** and must be clearly labeled, never described as diversity of model training. Different names are not proof of independent training or factual correctness.
4. Freeze and attribute each actual model/adapter/profile for every inference/tool operation. Keep BYOK secrets, per-actor permissions and source/egress grants, approved cost/token limits, native tool continuations and checkpoint-safe switching. No unapproved automatic fallback or cross-vendor hidden reasoning-state transfer.
5. OpenAI, Anthropic, DeepSeek, xAI/Grok, Moonshot/Kimi and future providers are **examples rather than exclusive or already-qualified integrations**. A model/provider is added only after its selected API/runtime/adapter has passed necessary compatibility checks.

Reuse the existing Step 9 provider-neutral gateway and Step 5/7 operation and budget controls; no new main reasoning model, selector-agent, model-ranking microservice, extra Council seat, MCP server per LLM, or new queue is authorized.

## Future acceptance evidence — ALL NOT RUN

- Five distinct qualified models selected on five original seats, with correct independent model attribution, permissions and sealed reviews; no main provider.
- Registry containing ten or more model entries without an arbitrary catalog cap, while unqualified tool-dependent models cannot dispatch.
- Explicitly chosen same-model control is visibly labeled; unapproved/default same-model inheritance is rejected.
- No silent DeepSeek/vendor fallback when a needed adapter, credential, tool continuation or egress permission is absent.
- Real provider-specific continuation, cost/UNKNOWN, credential, MCP isolation and switching tests; comparative same-model/different-model/single-agent baselines under comparable tasks and budgets.

**Status: APPROVED DESIGN ONLY. No runtime implementation, integration, security tests or superiority claim.**
