# ADR-22 — OpenAI Moderation API (hosted), not local GPT-OSS

**Owner correction:** October 15, 2026. The intended guard is OpenAI's **Moderation API**, invoked through a normal authenticated HTTP API call. It is NOT local gpt-oss-safeguard; no local safeguard model, downloaded weights, or moderation-specific GPU/VRAM requirement. This supersedes the earlier ADR-20 model/deployment choice while retaining unified trust and command-only peer access. **Status: accepted architecture correction; exact integration remains IN DESIGN. Implementation NOT STARTED; tests NOT RUN.**

## 1. Actual service and deployment

The customer-hosted unified Council backend uses a trusted **ModerationAdapter** module to call **POST https://api.openai.com/v1/moderations** with model **omni-moderation-latest**, a separately provisioned OpenAI API key, internet connectivity and strict outbound-network authorization. No separate local inference worker is required.

OpenAI documents the endpoint as **free to use for OpenAI API users**, but it still has rate/token limits, can time out and requires internet/API credentials. Free does not mean unlimited or locally hosted. It returns **flagged**, category flags and category scores, and supports **text and images**. It does not directly classify audio, video, arbitrary binary files, complete Git repositories or compressed archives as file objects.

Official references: https://developers.openai.com/api/docs/guides/moderation ; https://developers.openai.com/api/docs/models/omni-moderation-latest ; https://help.openai.com/en/articles/4936833-is-the-moderation-endpoint-free-to-use ; https://developers.openai.com/api/docs/guides/your-data

## 2. Enterprise confidentiality

**A Moderation API call sends its input to OpenAI.** Customer-owned local Git prevents vendor-hosted repository copying by default, but does not prevent this separate outbound data flow. The customer's versioned policy must **explicitly authorize the OpenAI moderation endpoint AND the data category/payload being transmitted before the request**. A primary model-provider BYOK key is not consent for sending proprietary code, company records, evidence or logs to OpenAI. If required hosted moderation conflicts with the customer's no-egress policy, report the conflict and **block the affected content flow** until separately approved policy changes or compatible alternatives exist. Never silently skip required moderation or upload disallowed company source.

## 3. Scope and limitations

The user wants relevant member-to-member content to pass moderation. Apply it to **eligible, authorized semantic text/image ingress and egress**, such as user inputs, peer messages, sealed assessment text at the permitted reviewer boundary, relevant generated content and tool outputs. Do NOT mistake source-file byte transfer or binary/large artifact streams for text-only moderation. For permitted code excerpts/images, the exact authorized contents may be submitted where policy allows; no automatic whole-project upload, and no claim that unsubmitted content was moderated.

OpenAI Moderation is a **content-safety classifier**, not a customizable arbitrary-policy reasoning model. It is **not** proof against prompt injection, credential leaks, malware, proprietary-code exfiltration, incorrect source code, or unauthorized filesystem/network access. Interpret API outputs through **separate deterministic, versioned application policy**. A non-flagged result never grants permissions. Retain deterministic identity/epoch, read grants, frozen manifest hashes, resource/budget guards, data-egress authorization, constrained networks, and specific file scanners as needed.

## 4. End-to-end gated operation

1. A Council member issues a typed command through the existing narrow trusted gateway, never sending arbitrary peer files, attachments or raw peer Git paths.
2. The unified control application authenticates the caller/epoch, checks authorization, checkpoint generation, recipient, permitted snapshot objects, and the **specific company content-egress authorization for the Moderation API**.
3. Only if the data is eligible and the external transfer explicitly allowed, a trusted adapter sends the text/image input to OpenAI with a protected API key. Apply bounded rate-limit admission, retries/backoff and timeouts.
4. The adapter receives the moderation classification. Council's own versioned policy maps categories/scores/flagged to **ALLOW, BLOCK, REVIEW**; outages, 429s, unsupported modality or prohibited company egress yield **UNAVAILABLE/RATE_LIMITED/EGRESS_DENIED**, never an implicit ALLOW.
5. Store minimal project-scoped decision metadata: command or content hash where permitted, classification flags/scores, effective moderation model, local policy version, company egress permission reference, result, and attempt status. Do not store entire company source or secret keys in shared audit logs.
6. The trusted gateway performs/delivers the separately authorized action. File read results remain a distinct **artifact-only envelope**, with no appended or automatically following chat messages. New chat requires an independent authorized SendCheckpointMessage command. No direct member-to-member transfer.

Moderate **semantic messages or approved content excerpts**, not every file-transfer chunk, Docker statistic or committed SQL event. API usage is free but rate-limited and subject to latency. Caching identical classifications by exact content hash + policy revision + model + recipient scope may be considered, but never cache authorization or bypass current checkpoint permissions.

## October 15 owner approval: provider-neutral moderation adapters (Option B)

**Approved without reopening earlier Council architecture decisions.** Council's unified trusted control application must use a **moderation-provider adapter interface** rather than hard-code the whole authorization design to one hosted provider. The **default first implementation** is OpenAI's hosted Moderation API (`omni-moderation-latest`). A company can instead select an **explicitly supported, approved customer-controlled/self-hosted moderation provider** when policy forbids sending content outside its trust boundary. This does **not** require building a local provider immediately; its implementation/verification status remains NOT STARTED/NOT RUN.

**Small stable interface:** a moderation request identifies source/destination scope, permitted input modality, required policy revision and correlation/content identity. An adapter returns provider ID and version, normalized `ALLOW / BLOCK / REVIEW / UNAVAILABLE` (derived using versioned application policy), provider-specific raw categories/scores where available, input coverage, actual execution outcome and minimum permitted audit metadata. Avoid pretending unlike providers have identical classifications or confidence scales; a missing or unexamined input is **UNCLASSIFIED**, not ALLOW.

**Deployment selection:** customer/deployment policy specifies the chosen moderation backend, supported modalities, legal egress conditions and approved processing boundary. The command gateway checks deterministic permissions and any required outbound-data consent **before invoking** a provider. No automatic failover to OpenAI when a company's local provider fails; it could leak prohibited data. If the chosen provider is unavailable, unsupported for required material, or not installed, mark the affected flow BLOCKED/REVIEW/UNAVAILABLE and expose the reason rather than silently skipping moderation. Deterministic filesystem/network, authorization, secret and snapshot-integrity checks remain independent of moderation.

**Not a new architecture discussion:** existing five-member independence, IRC-inspired typed command-only peer exchange, customer-owned Git, sealed review, PostgreSQL canonical state, transactional operations, UNKNOWN recovery, model/provider billing and retention rules remain unchanged. Only the moderation backend boundary is generalized. Precise DTOs/provider-compatibility verification belong to later specification and authorized build work; there are **no tests or implementation now**.

## 5. Required Step 3–5 design reconciliation

**Step 3:** Replace local safeguard model GPU/capacity assumptions with customer-approved OpenAI moderation configuration, credential reference, request/attempt records, category results, deterministic disposition, egress consent and rate-limit state. **Step 4:** Define typed moderation-required semantic boundaries and provider result handling separately from authorization; preserve five independent members, sealed reviews and command-only peer file reads. **Step 5:** Store durable external moderation intents and outcomes, only dispatch after authorized company egress checks, reconcile rate limits/timeouts, and never label failure as a successful guard check. Keep normal operation idempotency, canonical event ordering, budget, revocation/UNKNOWN and customer-owned archive guarantees.

**Still open:** data/category consent UX, provider-key setup and account limits, category-to-local-policy thresholds, latency/retry/caching and oversized inputs, unsupported media, treatment of enterprise no-egress installations, and the precise meaning of the separate earlier file-followed-by-messages wording. **Do not implement code or perform tests at the architecture stage.**
