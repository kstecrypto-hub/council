# ADR-53 — Step 9 credentials, MCP-mediated external access and adaptive authorization-based spending

**Owner approved October 21, 2026.** This amends the Step 9 provider gateway and Step 7 funding/admission defaults together. **ADR-53 policy APPROVED; Step 9 overall IN DESIGN, Step 7 prior scheduling/phase architecture remains DESIGNED as amended, Step 10 sandbox-network implementation IN DESIGN/PARTLY DESIGNED. No credential vault, operator billing, MCP enforcement, sandbox network rules, provider adapters or real usage tests have been implemented or run.**

Supersedes **BYOK-only pilot and mandatory fixed per-member/per-phase hard token/cost caps** wherever the earlier [Step 9 contract](STEP_9_PROVIDER_ADAPTER_AND_SHARED_MCP_CONTRACT_V1.md), [Step 7 controls](PART_7_MEMBER_SCHEDULING_RECOVERY_RESOURCES.md), [roadmap](MVP_SCOPE_BY_STEP.txt), [data model](POSTGRES_DATA_MODEL.md), or [application design](APP_DESIGN.md) describes those as the exclusive current policy. Retain **five protected project-specific spend scopes**, atomic Step 5 reservations, real owner/operator authority, no silent budget overrun, UNKNOWN provider charges and `BUDGET_EXHAUSTED / INCOMPLETE`. Related: [ADR-46 MCP isolation](STEP_9_ADR46_TOOL_CALL_ORDERING_AND_MCP_ISOLATION.md), [ADR-47 equal peer models](STEP_9_ADR47_OPEN_ENDED_PEER_MODEL_SELECTION.md), [ADR-48 autonomous tool retry](STEP_9_ADR48_AUTONOMOUS_TOOL_ERROR_FEEDBACK_AND_COOLDOWN.md), [ADR-51 technical model probe](STEP_9_ADR51_LIGHTWEIGHT_MODEL_TOOL_COMPATIBILITY_PROBE.md), [ADR-52 interrupted inference recovery](STEP_9_ADR52_PROVIDER_INTERRUPTION_CONTEXT_RECONSTRUCTION.md), [Step 5 operation ledger](PART_5_TRANSACTIONS_IDEMPOTENCY_CONFLICTS.md), and [local source control](LOCAL_REPOSITORY_AND_KNOWLEDGE_RETENTION.md).

## 1. Credentials: operator-owned pilot by default; optional user-provided keys

Council supports two explicit remote-provider credential funding modes **without a new wallet, reseller payment processor or inference-credit business layer**:

| Mode | API credential and provider account | Actual inference provider bill | Admission and exposure policy |
| --- | --- | --- | --- |
| `OPERATOR_FUNDED` (pilot default) | Council deployment/operator provides its own approved API keys/accounts | **Operator** is billed by the provider | Operator-approved aggregate run/user/account exposure and usage limits; users never receive the operator's secret or the ability to move its scope |
| `USER_BYOK` (optional) | User supplies a supported provider credential scoped to the user/deployment | **User** is billed directly by the provider | Explicit user choice/authorization for external provider, data egress and available budget; tool and provider grant scopes remain independent |
| `LOCAL_MODEL` | No remote inference API key | No third-party model API bill; local compute/resource cost still exists | Existing Step 7 resource/token controls and user/deployment policy |

Resolve a **credential reference and funding owner** for each approved actor/provider/model run-profile using the existing trusted gateway, with correct per-account tenant/seat/role/run boundaries. A worker inherits no broader rights or budget than its parent. Keep actual provider account charged distinct from optional future customer-facing pricing; the pilot has **no token wallet, hidden token markup, compulsory BYOK setup or payment ledger**.

Never silently substitute an operator key after a user's BYOK key fails, nor switch the funding owner, account, provider, egress destination or billing liability on reconnect/retry. An explicitly authorized profile change requires current grant/consent and safe continuation boundary; real usage is attributed to the key/account that actually dispatched it. Operator-funded per-user/run limits protect against one run consuming every account's capacity; BYOK records the user's actual provider account reference without displaying key bytes. Different customers cannot access one another's key or usage.

## 2. Credential security: n8n-inspired pattern, original implementation unless code license cleared

Adopt the useful **credential-encryption design** from n8n, **not n8n as an executing Council dependency**. Council is intended as a closed-source product. Architectural inspiration is permitted; **closed-source status alone does not grant the right to copy arbitrary n8n source code into a commercial product**.

Use **existing trusted control-plane and PostgreSQL storage** for an encrypted, scoped credential record, or a deployment-supported secret store where available. A conventional authenticated-encryption/envelope pattern is suitable: encrypt each sensitive credential under a versioned data-encryption key; protect that key with a separately held deployment/master key, **not stored beside the ciphertext in the same database**. Design for authenticated integrity, random per-record nonce as required by chosen library, rotation/revocation, separated encryption-key backups, minimal process-memory exposure, audited reference access, metadata-only UI and secret redaction from logs, tool payloads, model context, Git, archives, agent-owned Docker volumes and telemetry.

**Implementation choice is deliberately open:** use a maintained, correctly licensed cryptographic library; do not invent cryptography or mandate copying n8n's file/function. If a *specific n8n snippet* is demonstrably necessary and preferable, verify the **exact source file's license, copyright notices, commercial/internal-use limits and compatibility with the closed-source distribution** before incorporating it. The n8n main-repo Sustainable Use License is **source-available/fair-code rather than an unconditional OSI open-source grant**; the purpose here is design reuse, **not authorization to relicense/copy code**. Do not ship an unreviewed snippet; copying is not required for ADR-53.

Reference design: n8n official [credential-key rotation documentation](https://docs.n8n.io/deploy/host-n8n/configure-n8n/security/rotate-encryption-keys) and [Sustainable Use License documentation](https://github.com/n8n-io/n8n-docs/blob/main/docs/n8n-community-license/README.md). Cryptographic primitive/provider choice, secure master-key injection, credential migration, backup restoration and commercial code reuse checks occur during Step 9/10 implementation, with tests **NOT RUN**. No additional n8n runtime, SDK/server, vault microservice, database, global credential broker or enterprise KMS is mandated.

## 3. External tools: through MCP; sandbox-internal work stays agent-controlled

**Execution autonomy inside the authorized sandbox:** each member/worker may write, read and modify permitted files, run processes and scripts, use local tools, create internal workers, perform experiments, install approved dependencies and develop its own solution without requesting Council's intellectual approval for every action. Step 10 container isolation, cgroups, permitted internal filesystem/process access and local-only services define its actual containment; no fixed tool/task taxonomy or intelligence classifier limits solutions.

**Agent-initiated external service/resource access must be mediated by the existing trusted Council tool boundary via approved MCP integrations.** Examples include external GitHub/Git remotes, internet search, websites, SaaS accounts, external databases, network package registries, user/tenant APIs, network publication and externally hosted services. A tool exposed inside the sandbox is only an authenticated, scoped request surface to the existing trusted broker/MCP client; it is not an unmediated credential or socket.

**Necessary distinct trusted exceptions are not agent network escape hatches:**
- Model-provider inference uses the existing **trusted model gateway/provider adapters** directly, not a compulsory MCP wrapper.
- Council's own host-side Docker/resource administration, local checkpoint/snapshot grant/revoke, canonical database/ledger, controlled moderation/inference calls and trusted internal operations use their **existing internal/native control-plane contracts**, not MCP for the sake of MCP.
- Sandbox-local loopback/internal processes and permitted local files can run without MCP. Merely passing through an agent-controlled local subprocess cannot turn an **external** effect into an unmediated operation.

A sandbox with normal unrestricted internet access could bypass this architecture via `curl`, Python HTTP, shell package managers or arbitrary network sockets. Therefore Step 10 must **actually enforce outbound networking/host-network isolation** at the deployment/container boundary, allowing only its approved internal agent bridge and deliberately scoped local communication. External dependencies/downloads, including PyPI/npm, go through approved mediated MCP tool/registry proxy/cache routes when needed; authorized offline/local cached packages may be installed freely. Prevent DNS, IPv6, container host network, proxy and nested-worker escapes in future implementation tests. This is a **network/credential security boundary, not an AI reasoning restriction**. Whether a particular executor/container engine can support it is part of Step 10 implementation verification; do not claim isolation already works.

MCP service credentials can be operator-owned or user-provided under **their own external-tool credential scope**, always resolved outside sandboxes. Per-call authentication, data-source consent, egress, moderation, rate/cost/operation ledger and member/tenant/phase boundaries remain as in ADR-46/48. A shared MCP registration is not one global mutable credential/session.

## 4. Cost accounting: adaptive work, protected exposure; never promise a price or outcome

Owner clarification: Council **cannot predict the true cost or guarantee success** of an open-ended investigation from a token quota. Price estimates are **nonbinding ranges or 'insufficient data'**. Tokens consumed by different models are not equivalent measures of reasoning progress. A fixed estimate or arbitrary exhausted phase token target must never be interpreted as a verified result, agent success or checkpoint readiness.

Continue **real per-call usage accounting** (provider-specific input/output, cached/reasoning units if reported, provider pricing revision, latency, local resource usage, genuine settled/unsettled and UNKNOWN cost). At dispatch, the current funding owner-approved policy sets a **finite aggregate spending exposure ceiling** per funded run/account/project and preserves the existing five independent, project-specific **protected spend pools**:

1. Original-member development (including authorized worker calls).
2. Checkpoint peer review/comparison.
3. The one nonvoting Final Integrator's synthesis/implementation.
4. Five-member post-integration validation/premortem.
5. Orchestration, report, export and archive overhead.

No universal percentage allocation, forced equal member share, prepaid balance or guarantee that any pool can complete its obligations. **Within an already authorized development pool**, use **adaptive allocation among members and semantic phases**—no compulsory separate user-confirmed *hard* monetary/token allowance for every member-phase; any member/phase cap can be **optional explicit safety control**, not a promised scope of reasoning or mandatory fixed allocation. The Step 5 protected pool boundary and run/account/call bound always remain hard admission rules, and work needing a protected other pool requires a separately authorized policy revision. The mandatory all-five checkpoint and review obligations remain intact even if some members use much more than others.

- **Spending ceiling governs risk, not reasoning quality:** a model may choose as many authorized iterations/inner-loop operations as needed within the current funded limits, instead of being forced to claim completion when a forecast is crossed.
- **Who authorizes:** operator approves operator-funded exposure/quota; BYOK user approves user-funded ceilings; user/customer still controls project/egress/requirements and any required protected budget allocation. The operator cannot promise its user an included fixed answer cost if actual complexity is unknown.
- **Before each chargeable dispatch:** canonical Step 5 reservations atomically evaluate approved run/account/pool ceiling, actual settled + outstanding conservative reservations, provider maximum output/call limits and optional tighter caps. Retain unknown dispatched liabilities and current pricing/units. Do not silently draw protected post-integration/review funds into a development member or borrow from another tenant.
- **Internal adaptive shares:** per-member/phase planning estimates and allocations can move *within the same approved pool* without repeatedly asking the user, and without raising funded exposure or changing a protected cross-pool boundary. Record the current allocation and actual member usage for visibility and attribution; no extra cost-estimating LLM required.
- **When the actual authorized ceiling cannot admit the next call:** safely preserve work and exact unmet obligations, release slot as appropriate and report `BUDGET_EXHAUSTED / INCOMPLETE`; only a new authorization for higher overall/pool expenditure or cross-protected-pool transfer permits more dispatch. No forced PASS, finalization or phantom fifth-member review.
- **Account/provider reality:** per-call conservative caps can bound **Council's approved outgoing requests**, but final provider invoices can differ due to billing lag, unreported/cache/reasoning tokens, unsettled usage, shared account activity, price changes or provider billing semantics. Use provider-side limits where available and disclose uncertainty, **not** an absolute guaranteed invoice maximum.
- Local inference still has enforceable host/operation token/context/output/resource controls; no required artificial member-phase token budget merely because a local provider reports tokens.

**No Council-owned prepaid token wallet/payment processor/inference reselling** is introduced; operator-funded pilot usage is paid to model providers from the operator's **own accounts**, not a merchant liability created by collecting and redistributing user credit.

## 5. Interaction with historical specifications (supersession)

ADR-53 specifically overrides older statements that:
- **MVP requires BYOK for every remote model seat** or **Council/operator cannot fund inference**. Now `OPERATOR_FUNDED` pilot is available/default, optional `USER_BYOK`; no funded credential is ever supplied to sandboxes.
- **Every member needs an obligatory hard per-phase token ceiling** or that a user must repeatedly extend intermediate estimate-based phase quotas. Mandatory checks now cover **approved aggregate/run/account and five protected pool budgets**, with flexible internal same-pool member/phase shares; optional member/phase limits can be configured.
- **External network access might occur via sandbox direct sockets** if an agent calls a local program. It cannot: external agent-initiated connectivity goes through approved MCP (while model-provider inference/trusted control-plane internal calls retain their direct gateway/native paths).

Do **not** delete the verified Step 5 operation ledger/idempotency/unknown liability semantics, Step 7 whole-member scheduler, five protected funding scopes, source/egress grants, Step 8 five genuine independent checkpoint reviews, or approved interruption/recovery and model-neutral catalog policy. Revise the exact DTO/budget SQL contracts at implementation time only as required to represent optional per-phase caps and credential funding owner; no code/migration is authorized now.

## 6. Future acceptance and negative cases — ALL NOT RUN

| ID | Planned scenario | Required result |
| --- | --- | --- |
| P9-63 | Operator funds two Council user runs | Provider key never enters either sandbox; operator pays provider; per-run/customer exposure prevents one user exhausting unrelated user allowance |
| P9-64 | User opts for own provider API key | User billed directly, exact user credential reference resolved, no silent operator-key failover |
| P9-65 | Encrypted credential record stolen without separate master key | No plaintext API key exposed by database backup alone; ciphertext integrity/rotation metadata preserved |
| P9-66 | Sandboxed agent/worker attempts to read another user's key or network provider directly | Denied outside trusted broker; no key in container/env/log/prompt or direct unmediated provider access |
| P9-67 | Agent uses Python/curl/npm to contact public internet | Egress prevented by actual Step 10 network boundary; approved MCP download/registry route works if authorized |
| P9-68 | Agent runs arbitrary local scripts/tests, spawns local workers | Remains possible within allocated sandbox/resources without extra Council reasoning/quality permission |
| P9-69 | Direct model inference and native checkpoint operations | Continue through gateway/trusted internal paths, not unnecessarily wrapped as external MCP tools |
| P9-70 | Model exceeds optional phase spending estimate but protected development pool has capacity | Continue within actual authorized pool/run/account cap, no spurious user prompts or forced readiness |
| P9-71 | One seat exhausts all ordinary development pool while protected review funds remain | No review-pool borrowing; block or request revised spending authority; no declaration of five-member completion |
| P9-72 | Operator-funded project reaches operator per-account exposure; BYOK user project separate | Operator-funded paid dispatch stops without unauthorized alternate-key use; BYOK scope unaffected |
| P9-73 | Provider usage delayed or UNKNOWN after interruption | Reserve conservatively; no claim that final provider invoice or model success is guaranteed |
| P9-74 | User-selected hard member/phase ceiling exists | Enforce it as a real configured constraint; absent such config, do not invent one as a mandatory default |
| P9-75 | Specific n8n source snippet proposed for closed-source reuse | Architectural pattern may be used; actual code is incorporated only after exact license/provenance/commercial-rights review |
| P9-76 | Successful long-running Council project under uncertain cost | Actual usage and evidence are attributable; cost estimates never treated as guaranteed outcome or fixed final price |

**Verification boundary:** These scenarios describe future implementation and security/finance tests. **No credential, encryption, gateway, MCP, container network, billing, quota or provider integration has been implemented or tested.** The Step 9/7 policy decision is OWNER APPROVED; exact implementation and Step 10 enforcement tests remain pending.
