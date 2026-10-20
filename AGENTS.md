# Instructions for agents working in this repository

## Authority and current stage

This is an approved-design repository, not an implemented application. Read `docs/APP_DESIGN.md` in full before proposing or implementing changes. Then read `docs/POSTGRES_DATA_MODEL.md` and `docs/TYPED_INTERACTION_CONTRACTS.md`; read `docs/IMPLEMENTATION_HANDOFF.md` next. The latest explicit owner instruction is authoritative; supporting handoff notes do not silently override the complete design.

The initial authorization was to create a repository and publish the approved design. It was not an instruction to build the application. Do not start application implementation solely because this file exists. A later explicit implementation request authorizes work within its stated scope; do not then ask for redundant confirmation.

## Preserve these design commitments

- Peer investigators govern the council. Do not introduce a single lead/supervisor/judge with unilateral intellectual authority above it.
- The Project Orchestrator is deliberately narrow: it owns canonical prompt generation, small prompt/clarification memory, transformation of raw user replies into stable agent-ready instructions, and a versioned **project-specific semantic phase/checkpoint plan** presented for user approval. It does not intellectually judge milestone quality, become a solution designer, winner selector, hidden judge, or unilaterally govern peer-review/publication protocol. Each Council member declares its own CHECKPOINT_READY.
- Council members and workers may originate questions to the user. The raw user reply must never flow directly back to the requesting agent: it passes through the Project Orchestrator, which may improve form but not substance, then returns a processed answer. Local clarifications remain local where appropriate; project-wide requirement changes propagate consistently to affected branches.
- Every member investigates, delegates, challenges, and revises. Members own investigations, not conclusions they must defend.
- The core is domain-agnostic and must support a complete non-coding investigation with no terminal tool.
- DeepSeek is the initial default, not a globally hard-wired provider. Support per-seat and per-worker model overrides, safe session migration, and provider-specific data permissions.
- The same-model council must be labeled honestly. A new session is not a new independent reviewer.
- Keep independent unpublished branches private across retrieval, graph queries, context packets, caches, and exports. Communication occurs only through the versioned checkpoint policy or an approved adaptive checkpoint, with explicit publication scope.
- Runtime events are authoritative for observed execution. Agent-submitted semantic relationships remain attributed, reviewable interpretations.
- Preserve the Part 4 action-linked state invariant: no externally meaningful state/activity may be implemented as a label only. Follow the registered trigger -> behavior -> interaction/UI -> command -> event -> transition/recovery contract. Durable interaction requests, not activity labels, cause blocking user decision surfaces.
- Keep evidence support separate from council agreement. Preserve contrary evidence, minority positions, uncertainties, and source lineage.
- Treat assumptions as first-class records. Preserve joint premises and alternative supporting routes. Do not equate citations with proof, chronology with causation, or different documents with independent evidence.
- Keep claim revisions append-only. Upstream changes trigger reassessment, not automatic declarations that all dependent claims are false.
- Use durable records, bounded context packets, ordinary search, graph-assisted retrieval, checkpoints, and summaries together. Do not put the full graph into every prompt or promise unlimited/lossless context.
- Perform the six-month-plus premortem as a hypothetical review now. Do not invent future observations or silently schedule future runs.
- A final report assembler has editorial authority only. It may not erase unresolved objections or silently pick the winner of a factual dispute.
- Require scoped permissions for tools and provider changes. Keep credentials outside model prompts, browser state, generated code, and ordinary logs.
- Account for retries, failures, child agents, and parallel reservations in budgets. Preserve the user's approved per-phase token/cost ceilings and protected checkpoint/review/finalization allowance. Exhaustion leaves the member BUDGET_EXHAUSTED / INCOMPLETE, never CHECKPOINT_READY, /done, or forced consensus. Propose, but never impose without approval, the configurable 70/25/5 budget split; use nonbinding uncertain token forecasts only for planning.
- Step 7 schedules whole member environments in fixed 1->5 seat order when capacity frees; do not impose mandatory periodic private-work slices, fixed reasoning-call counts, or general reasoning deadlines. Individual provider/tool operations still require safety timeouts. Default remote concurrency starts at two per provider (subject to stricter actual limits), local inference at one until verified safe; use resource-vector admission and preserve host headroom.
- Bring Your Own API Key or compatible local inference is the MVP; provider bills the user directly and Council owns no prepaid token wallet. Provider secrets remain outside all agent-controlled sandboxes and are reachable only through authorized, revocable runtime bridges. Council budget limits govern its own dispatch, not final provider invoices.
- For executable projects, execution isolation is transparent to the agent. The agent acts as though it owns a normal machine and controls everything visible inside its environment, including destructive changes. The runtime owns only the invisible isolation/lifecycle boundary and must prevent escape, cross-branch access, protected credential access, or direct canonical-state mutation. Host matching is opt-in.
- In Match My PC mode, treat the approved Environment Contract as the boundary. Do not collect unrelated host data, infer permission from mere device/software presence, or silently upgrade compatible/bridged behavior to exact verification.
- Never give an agent or ordinary Council process unrestricted administrator, Docker-daemon, or kernel access. Elevated host operations go through the typed local privileged broker and only within approved capability scope.
- Match My PC does not authorize modifying the real host. Host software/configuration/driver/service changes require separate explicit permission and must be auditable and cleaned up or rolled back where practical.
- Treat the accepted reproducible project environment as part of the deliverable. Do not leave Council agents, provider credentials, agent/local or external Git credentials, hidden Council control mechanisms, or orchestration-only tooling in the user's final runtime.

## Implementation discipline when implementation is authorized

Reuse established runtime and continuation mechanisms where appropriate. Karpathy's autoresearch and the Ralph pattern are conceptual references, not instructions to copy coding-specific scope, permission-bypass flags, scalar optimization objectives, or indefinite execution. Verify current upstream behavior and licensing before reuse.

Implement and test canonical records and backend authorization before relying on a graph visualization. Make the three graph questions in the README executable product behavior, not decorative UI.

Do not import the earlier single-lead starter as the baseline. Do not create a separate graph or memory system that can silently disagree with the investigation ledger. Avoid adding a dedicated graph database, vector database, Redis, or Kubernetes until demonstrated requirements justify it and the design change is recorded.

Use the approved build sequence and acceptance criteria. Test deterministic invariants separately from repeated model-dependent evaluations. Distinguish local unit results, simulated providers, live provider runs, sandbox runs, and deployment verification.

Do not report a feature as implemented, a test as passed, a repository as pushed, or a service as deployed without concrete evidence. Record unverified assumptions and blockers plainly.

## Repository hygiene

Do not commit secrets, environment files, private research inputs, generated runtime records, credentials, caches, or production exports. Use synthetic or explicitly authorized fixtures for tests. Do not add an open-source license on the owner's behalf without authorization.

Keep documentation aligned with implemented behavior and record substantive deviations. Avoid unrelated refactors and dependencies that turn the investigation product into a generic coding-agent shell.

## October 13, 2026 architecture amendment

Read docs/ARCHITECTURE_DECISIONS.md and docs/architecture_contract.json alongside the amended specifications. The owner's **newer ADR-17 private local checkpoint snapshot policy supersedes the old public-GitHub default** and applies to generated member source, not to this Council source repository. Preserve five fixed members, sealed independent reviews, externally isolated peer verification, **member-declared semantic milestones with user-approved phase token/cost ceilings (no mandatory periodic private-work slices)**, conservative reservation accounting, commit-safe event replay, and separate communication/verification/acceptance records.

A documentation edit can be SPECIFIED without being IMPLEMENTED or VERIFIED. Do not close a runtime step from prose, a generated schema, static checks, mocks, or a successful push. Implementation completion requires code and scoped evidence; verification requires executed tests with recorded environment and results. Existing accepted design sections do not imply that later amendments or application work are complete. No application implementation is authorized merely by this maintenance update.


## Accepted Step 8.1 — optional controlled experimentation (October 14, 2026)

Read `docs/PART_8_AGENT_LOOP_EXPERIMENTATION_DELEGATION.md` when designing/implementing member execution. Inside the persistent member's ordinary ACT loop, an agent may **optionally** conduct a Karpathy-style `HYPOTHESIS -> CHANGE/ALTERNATIVE -> TEST/CHECK -> OBSERVE -> KEEP/REVISE/DISCARD/INCONCLUSIVE -> RECORD` experiment. This does not add an independent intellectual supervisor, required experiment count, universal score, or fixed reasoning deadline. The member chooses its investigation and authors interpretation/readiness.

Persist hypothesis, exact baseline/change and environment/test inputs, measured or qualitative results, failures/regressions, and member dispositions with Step 6 source/provenance lineage. Agent-created exploratory tests are not a substitute for protected acceptance checks. A worker can perform a parent-authorized experiment under the parent's capabilities, branch and budget, but cannot approve parent readiness or cross-peer changes. During checkpoint `/work`, frozen authoritative candidates remain read-only and only disposable verifier environments execute tests. Failed/inconclusive experiment records survive if code changes are reverted.

**Step 8 remains IN DESIGN**; Steps 8.2 and 8.2a now settle sandbox-local worker autonomy **and Docker-based worker-file persistence**. No new Council per-worker recovery system or mandatory worker merge protocol remains to design. Member action/observation schemas and final phase/checkpoint gates remain open. These approvals do not authorize or claim runtime implementation.

## Accepted Step 8.2 — no internal worker cap; Docker controls the sandbox (October 14, 2026)

A permanent Council member can create **as many nested AI worker agents or ordinary child processes as it chooses** inside its own sandbox. There is no **Council-level worker count cap, depth cap or global worker scheduler**. Do not revive a "simple worker/delegation depth limit" in MVP. The five Council logical seats and admission queue operate on whole member sandboxes, not on each worker process.

All processes share the parent's **aggregate sandbox** CPU, memory, PID, disk and permitted GPU/device limits, and any provider/gateway calls charge the parent-approved phase token/cost ceiling. They inherit only the parent or narrower permissions, cannot reach other members' unpublished data, and do not obtain raw BYOK keys or Docker Engine socket access. A separate child Docker container, if needed, is provisioned only by a trusted scoped broker and counted against the same aggregate member resources.

The **trusted host-side Resource Monitor** uses Docker Engine container stats plus OOM/die events, not Windows Resource Monitor or agent-supplied metrics. Start with configurable **2–5s** sample intervals, monitor **80%/90%** assigned-sandbox-RAM pressure and new **broker-mediated** heavyweight admissions, keep separately measured adjustable ~20% host RAM headroom, and separately monitor WSL2 VM RAM, free disk/volume/log growth and optionally NVIDIA GPU/VRAM via NVML. Docker-supported **cgroups hard memory/CPU/PID limits** enforce the aggregate boundary; telemetry and thresholds cannot guarantee prevention of sudden OOM/crashes. Council can safely quiesce/recover the entire sandbox, not individually intercept every arbitrary local worker fork.

Monitor operates outside sandbox control with narrowly scoped host Docker access; never bind-mount the daemon socket into a member or worker container. Stale/unknown metrics stop *new* unsafe admissions but do not retroactively mark existing work failed/successful. OOM/crash/cleanup is reconciled under Step 7, with durable same-logical-member recovery and no fabricated CHECKPOINT_READY.

**Design only:** Step 8.2 worker/resource policy ACCEPTED; Step 8 overall IN DESIGN. No Docker monitor, agent worker runtime, SQL schema migrations or resource-pressure test is implemented or verified by this specification edit.

## Accepted Step 8.2a — Docker-native worker workspace persistence (October 14, 2026)

The Council **does not manage every local worker's life/restart/recovery**. Each of five logical members owns a private, durable **named Docker volume** or specifically approved bind mount for project files, private Git, worker notes, saved plans and results. Stop/recreate can remount those files into a fresh member sandbox after identity, mount/permission, resource and execution-epoch checks.

Important boundaries:

- Docker restart starts a new container process. **It does not restore in-memory AI worker execution**. Saved worker progress and how to resume/retry it is an autonomous member concern; unsaved process state can be lost. Container writable layers and tmpfs alone are not durable across recreation.
- **Do not add** Council per-worker resurrection/lease/orchestration machinery, mandatory process checkpointing/CRIU or an independent child scheduling system merely for internal workers. Existing trusted canonical evidence, spend, user approvals and external operation/UNKNOWN reconciliation still apply.
- **Do not** enable unconditional Docker restart policies for deliberately inactive/checkpoint-ready, PAUSED or BUDGET_EXHAUSTED members; they must be re-admitted under the existing Step 7 **whole-member** resource/authority/checkpoint guards.
- Do not share one member's private volume with another. Member-local persistence is not permission to publish peer state, skip checkpoint safety, bypass raw-credential isolation or delete archives before verified retention closure.
- Docker storage/restart correctness and isolation checks are pending Step 10 implementation and test execution. **No runtime worker restoration is marked implemented**.

This completes the **worker persistence design decision**, not Step 8 or Step 10 runtime implementation.

## October 14, 2026 design-stage closure of Steps 3–5

Steps 3, 4 and 5 have completed **design specifications** (see the October 14 closure sections of docs/POSTGRES_DATA_MODEL.md, docs/TYPED_INTERACTION_CONTRACTS.md and docs/PART_5_TRANSACTIONS_IDEMPOTENCY_CONFLICTS.md). The Council application, database migrations, provider/host interactions, runtime tests and evaluation results remain NOT STARTED / NOT RUN.

- One project-lifetime isolated PostgreSQL per trusted Council deployment; exactly five logical member seats; branch-private/source-linked context; separate immutable user approvals; customer-local approved immutable snapshot manifest with scoped read-grant/revoke operations and observed access checks; all-five sealed reviews, atomic reveal, communication obligations and version-bound DONE; Git evidence validation before teardown.
- Typed command schemas and actor permissions are authoritative. **Authenticate and authorize, then deduplicate a same-key/same-hash command before applying new-command stale-state/transition guards.** An identical successful approval replay must not launch a second run or be rejected solely because the first changed the target version.
- Lock deployment event-clock first and use deterministic aggregate/budget order. Commit canonical state, external-operation intent, event, outbox and result atomically; dispatch local snapshot/grant/revoke, optional customer-authorized external Git/provider/Docker effects only after commit. Reconcile unknown effects; never infer a successful snapshot grant/revocation or optional external Git visibility transition, cancellation, refunded usage, or final archive from a requested action.
- The runtime does not intellectually judge CHECKPOINT_READY, turn BUDGET_EXHAUSTED into completion, reveal sealed reviewer text early, or erase disagreements. State/UI labels do not constitute real authorization or passing tests.

Implementation completion requires code references and actual test evidence. A documentation update alone may only say DESIGNED.

## October 15 owner-approved Steps 3–5 unified trust and command-only safeguard (ADR-19/20/21; design only)

Read [docs/STEPS_3_TO_5_DEPLOYABLE_ARCHITECTURE_2026_10_15.md](docs/STEPS_3_TO_5_DEPLOYABLE_ARCHITECTURE_2026_10_15.md) before changing Step 3–5 schema, commands, checkpoints, IRC protocol, file transfer, data egress or host isolation. The customer approved one unified logical trusted Council control application, but host Docker authority, data/database/secret access and member sandboxes MUST have separate enforceable security boundaries.

hosted **OpenAI Moderation API** policy reasoning is a **mandatory semantic policy inspection layer** for content exchanged through approved gateway boundaries, while deterministic identity/capability/recipient/manifest/network/egress/budget checks retain final authorization. A classifier ALLOW cannot override denied authority; classification failure blocks new affected semantic boundary operations. moderation API egress/rate-limit capacity remains a design/deployment admission question. No silent model bypass, claim that binary content is examined by text-only models, or assertion that model moderation guarantees security.

Members only ask for/receive approved peer content via narrow **typed commands**; they cannot select arbitrary files from host filesystems and push/send/upload/attach them to other members. The trusted gateway resolves opaque selected snapshot object IDs, authorizes and returns bounded content. File/artifact transfers must be distinct from chat messages and never automatically include/trigger follow-up text messages. Later commentary, if permitted, is a new independently authorized chat command. Keep sealed reviews and immutable checkpoints. No direct agent-to-agent network or other member volume mounts.

**These are design-only changes** for the full Council method (five independent candidates, sealed evidence-grounded reviews, structured challenges, trusted verification, source provenance/graph, contextual lessons, honest blockers); no SQL migrations, implementation, runtime tests or benchmark/evaluation runs are authorized by this edit. Steps 2–5/8/10/11 remain in design where pending.

## October 14 owner supersession: local Git and contextual failures (ADR-17/18)

**Read** [docs/LOCAL_REPOSITORY_AND_KNOWLEDGE_RETENTION.md](docs/LOCAL_REPOSITORY_AND_KNOWLEDGE_RETENTION.md) before planning ANY repository/checkpoint/retention/reuse implementation. The owner's newer policy **replaces** prior default GitHub PUBLIC checkpoint and cross-customer learning assumptions. Each Council member owns its sandbox-local Git; the trusted host gateway shares only approved selected read-only frozen snapshots with peers during authorized checkpoints. No external source hosting or public publication is mandatory. Keep existing sealed reviews, five-member barrier, branch isolation, Docker worker autonomy, budget/UNKNOWN operation semantics and approved source permissions.

All source, proprietary project reconstruction packages and customer-specific recipes stay customer-controlled and are only retained per consent/retention policy. A vendor/global memory cannot receive customer-derived patterns without separately approved **specific content/audience, privacy/IP/license screening**. A previous failed approach is **FAILED_IN_CONTEXT** evidence, not a universal ban or silent filter; retrieve applicable working strategies first, then attach contextual failure warnings/suggested tests. Compare versions, workload, environment, constraints and known root cause; preserve member freedom to retest. Success evidence is also context-bound, not proof of a universal winner.

Steps 2–5 had prior design-closed status **only under the now-superseded publication policy**, so their local snapshot/permission/retention integration is REOPENED IN DESIGN. Step 11 ranking policy is still IN DESIGN; no actual Git gateway, storage migrations, source processing, customer-data export, cross-customer knowledge system or runtime tests have been performed.


## October 15 accepted Step 8.3 and Orchestrator planning library (ADR-23/24)

Before changing the runtime agent-loop architecture, consult [Step 8.3 completion/readiness](docs/STEP_8_3_MEMBER_PHASE_COMPLETION_AND_READINESS.md): member-authored readiness intent is **not** a mechanically verified checkpoint arrival; the trusted runtime must separately observe pinned candidate/evidence, safe freeze/suspension and resource release. A truthful member conclusion with no viable candidate does not mean successful implementation or automatically satisfy the all-five ready barrier. No hidden sixth intellectual judge, arbitrary reasoning deadline, worker scheduler or forced readiness. Preserve all approved prior Step 7/8 subdesigns.

[Orchestrator development-method library](docs/ORCHESTRATOR_DEVELOPMENT_PATTERN_LIBRARY.md) provides **optional, source-tagged, versioned local patterns** to propose better user-approved *semantic* checkpoint outcomes. No match means requirements-derived planning, never fabricated references or blocked project setup. Do not use it to mandate implementation details, choose peer solutions, change intellectual authority, absorb private branch reasoning or bypass Step 11 retention/opt-in. Reuse existing plan/contract records and application components.

**Status:** ADR-23 Step 8.3 owner-approved policy, ADR-24 planning-library owner-approved design direction. Step 8.4/8.5 and exact wire DTOs still IN DESIGN. Runtime NOT IMPLEMENTED, tests NOT RUN.

## October 16 owner-approved Step 8.4: one final integrated artifact in every domain (ADR-25)

Follow [docs/STEP_8_4_COLLECTIVE_SYNTHESIS_AND_FINAL_INTEGRATION.md](docs/STEP_8_4_COLLECTIVE_SYNTHESIS_AND_FINAL_INTEGRATION.md). The product goal is **NOT** automatically five final implementations + majority vote/winner selection. Five genuinely independent investigations compare what each did **better and why** in sealed-review/discussion, synthesize one **evidence- and artifact-bound blueprint**, and a **single separate non-voting Integration/Synthesis LLM** produces ONE cohesive final result in its own scoped workspace. The **same five original members independently and sealedly review the actual integrated result again**. This is **domain neutral**: applications/code, research syntheses, experiments, engineering designs, documents and other authorized Project Contract outputs. Do not require five completed products where prototypes/partial investigations suffice, or call a concluded negative result a working candidate.

Do not give the integrator a sixth seat/vote or original members' writable Git access. Its permissions and budget are separately authorized after final comparison checkpoint access revocation. Preserve evidence, source lineage, dissent and version-specific real verification; material changes to integrated result require affected re-review. Premortem is performed on the actual integrated result and frozen provisional report, then user review and verified export/cleanup. No invented citations/data/results, no automatic majority truth, no automatic final user acceptance. The previously proposed 70/25/5 review/finalization split must not silently fund substantial integration; user explicitly approves a suitable budget.

**Architecture only** — owner-approved policy, exact DTO/DDL/transaction/adapters still IN DESIGN, application implementation NOT STARTED, tests NOT RUN.

## October 16 Step 8.4 approved integrator, budget, re-review and sealed premortem (ADR-26–29)

See [Step 8.4 §9](docs/STEP_8_4_COLLECTIVE_SYNTHESIS_AND_FINAL_INTEGRATION.md). The non-voting Integrator can make attributed, bounded technical/methodological trade-offs only within the authorized Blueprint/Project Contract; material changes to permissions, scope, data egress, budget or acceptance criteria require user approval. Record alternatives, evidence, dissent, compatibility, rationale, provisional uncertainty and exact output revisions.

The former 70/25/5 **setup default** is superseded for integrated final deliverables. The new default behavior is to **propose** five distinct protected, customer-approved spending scopes—private work, checkpoint comparison, integration/synthesis, five-member post-integration verification + premortem, and orchestration/report/export—without any universal default percentage. Integration requires its own protected scope and minimum protected next-step review capacity. No pool borrowing without approved immutable policy revision.

First integrated version receives five real sealed independent reviews. New *substantive* versions receive five fresh sealed delta reviews when dependency impact is supported as local, otherwise full five-member reviews. Proven non-substantive equivalence may retain only specific justified old applicability, never invent a passed updated test. The six-month-plus premortem is a **separate five-member sealed** round against one frozen integrated artifact and provisional report pair; atomic all-five reveal, no fabricated future facts, material-change impact invalidation. Keep same five original reviewers; integrator has no vote.

**Design-only change; exact Step 3/4/5 schema and runtime test contracts still IN DESIGN; implementation NOT STARTED, tests NOT RUN.**

## October 16 approved ADR-26 refinement — Council owns integrative choice of direction

**Never delegate high-level approach selection anew to the Final Integrator.** The original five members remain the intellectual authority and produce an evidence-grounded, versioned **Council Decision Register** embedded in their Blueprint. Preserve actual pre-discussion sealed positions when present and final positions, why they changed, source/evidence overlap, selected recommendations, minority objections, and genuinely unresolved cases. Member convergence has **rebuttable extra qualitative weight** as a preference/tie signal but is not mathematical voting correctness, independent proof or a veto. A verified minority counterexample can outweigh majority preference.

Integrator is a separate **non-voting implementation/synthesis execution agent** and **follows the Council recommendation by default**. Material divergence requires explicit evidence/compatibility, versioned IntegratorDeviation record, actual result-version linkage and transparent five-member post-integration review. Model confidence/pretraining alone is not authorization to silently substitute a different plan. Existing User Contract/egress/budget/retention gates and five-member sealed review remain unchanged. [ADR-26](docs/STEP_8_4_COLLECTIVE_SYNTHESIS_AND_FINAL_INTEGRATION.md#91-adr-26--bounded-intellectual-discretion-for-the-final-integrator). Still DESIGN only, no implementation/tests.

## October 16 approved Step 8.5A Blueprint handoff (ADR-30/31)

The five original peers, **not a report model or control-plane classifier**, authentically author the material comparative recommendations, changes and objections during existing checkpoint discussion using typed actions, preserving original full transcripts/evidence. The Blueprint's Council Decision Register is assembled/validated from those attributed immutable records. Never infer consent or a 5/5 recommendation from silent members, suppress supported minority objections, or make the Integrator select direction anew.

A Blueprint **DRAFT is not executable**. Mechanical `FROZEN` hash/source/contract integrity is distinct from **EXECUTABLE HANDOFF**: current legitimate FIVE original member /done and closeout/obligation frontier, no pending required /work, actual checkpoint closure and *independently verified source-read grant/route revocation* are prerequisites. Force-incomplete closure is NOT an authorized Integrator handoff. Disputed or deferred substantive objections can be faithfully carried with genuine member disposition but not turned into solved evidence. Separately authorize fresh integration source grants, budget, model and sandbox. Existing Step 3/4/5 runtime and schema implementation remains not started. [Step 8.5A](docs/STEP_8_5_STRUCTURED_COUNCIL_BLUEPRINT_HANDOFF.md).

## October 16 approved Step 8.5B — final integrator durable identity and verified review handoff (ADR-32–35)

[Step 8.5B](docs/STEP_8_5B_FINAL_INTEGRATOR_EXECUTION_AND_RECOVERY.md) is authoritative owner-approved **architecture-only** design: single stable **non-voting logical Integrator** with isolated customer-owned persistent workspace, current epoch, bounded parent-scoped workers/tool calls and separately approved protected integration budget; it is **not** a sixth peer or another service. Whole-agent Docker recreation does not preserve live worker/process stacks. Integrator can restart as same logical identity only after safe actual-effect/UNKNOWN reconciliation.

Integrator `OUTPUT_READY_INTENT` is **model-authored**; trusted backend separately confirms exact content-hashed software/non-code artifact, source/provenance/reconstruction, fenced writes/whole-agent suspension, reconciled consequential effects and observed resource release before `INTEGRATED_OUTPUT_VERIFIED`. No output verification based on model assertion, no automatic protected test PASS, no read of mutable integrator workspace by peers. The new read-only version-pinned integrated output is independently sealed-reviewed by the SAME **five original members**, not the integrator; correct review/closeout/grant revocation precedes separate integration revisions. ADR-28 delta/full and ADR-29 premortem remain mandatory as applicable. Preserve Step 8.5A Blueprint genuine closure, Step 5/7 budgets/UNKNOWN and customer-local privacy rules.

No implementations, migrations, evaluations or runtime tests have occurred. Step 8 still IN DESIGN.

## October 16 approved combined Step 8.5C+D and lightweight API submission lanes (ADR-36–40)

Read [joint 8.5C+D source of truth](docs/STEP_8_5C_8_5D_COMMAND_STATE_RECOVERY_AND_FINALIZATION.md) before changing final-stage transitions. Use ONE existing trusted typed command/event/state mechanism with exact Blueprint, output, five-member sealed review, frozen artifact/report premortem, final package/acceptance and observed archive/teardown version identities. Maintain original Council's five seats and integrator's non-voting execution-only role. Do not conflate report drafting, authored ready intent, mechanically verified artifact, protected test PASSED, completed peer review, user acceptance or delivered `RunCompleted`.

**Owner-added queues:** implement only when application build is expressly authorized: small bounded keyed queue lanes **inside existing internal trusted API** to serialize same-aggregate simultaneous submissions. Never sleep to avoid matching timestamps; independent seats' submissions remain separate. The queue is not a security, durable acknowledgment, cross-instance locking or committed-order authority; **existing** canonical PostgreSQL lock/event-clock/idempotency/expected-version/seat-uniqueness rules hold and no new Redis/third-party queue or global bottleneck is required. Do not acknowledge an in-memory-only queue entry as durable. Keep protected budgets, operation-class-specific UNKNOWN effects, stale epochs, honest blockers and verified customer-local archive/ref cleanup.

**Approved SPECIFICATIONS ONLY** — Step 8.5C/D policy approved, precise executable DTO/DDL/transaction/queue runtime and fault-test work IN DESIGN, no implementation/test run.

## October 15 owner correction ADR-22: OpenAI Moderation API is hosted

**Authoritative:** [docs/OPENAI_MODERATION_API_CORRECTION.md](docs/OPENAI_MODERATION_API_CORRECTION.md) supersedes all earlier local-model/OpenAI safeguard assumptions. Use `omni-moderation-latest` through OpenAI's hosted `/v1/moderations` only after the customer's *specific data-category/endpoint egress permission*. No local GPU/weights, no custom guard model, no unapproved upload of company code, and do not use moderation as deterministic authorization, DLP, prompt-injection defense or file scanner. No silent fail-open. Keep unified trust, five member autonomy, command-only file results, checkpoint consent/revocation, truthful design-only status. No implementation/tests.


**October 16 owner correction — simplify ADR-40:** The previously proposed separate small keyed internal API submission queues are **SUPERSEDED**. Reuse Step 7's existing low-spec whole-agent resource queue, Step 5's PostgreSQL idempotency/transaction/seat uniqueness/event ordering for simultaneous submissions, and Docker named-volume/container lifecycle for infrastructure persistence. The existing Council runtime—not Docker alone—handles epoch/budget/permission gates and uncertain external operation results. Do not build extra API queue layers or a new recovery manager. [Authoritative lean Step 8.5C+D](docs/STEP_8_5C_8_5D_COMMAND_STATE_RECOVERY_AND_FINALIZATION.md). ADR-36–39 unchanged. **Design only; implementation NOT STARTED, tests NOT RUN.**

## October 19 design reconciliation (no runtime implementation)

Read [Steps 2–8 reconciliation](docs/STEPS_2_TO_8_CROSS_STEP_RECONCILIATION_2026_10_19.md) as the authoritative cross-step contract alongside the latest ADRs. Historical mentions of 70/25/5, public Git default, local moderation inference, separate internal API submission queues, original-candidate final acceptance or five-member unanimity requirements are **superseded**, not build tasks. Default final acceptance requires the exact integrated artifact+report/package and user approval. One persistent non-voting Integrator is not a member seat; all five authentic original members independently review the exact result. Software/non-code artifacts use their appropriate immutable manifest. User-approved five protected budget scopes replace a fixed ratio. Steps 2–5/8 remain IN DESIGN; code and runtime tests NOT STARTED/NOT RUN.


## October 19 — exact v1 interface specification and truth-in-status

Steps 2–5 and 8 **have completed their v1 architecture/interface specification**, using [Step 2 snapshot/transfer](docs/STEP_2_SNAPSHOT_TRANSFER_CONTRACT_V1.md), [Steps 3–5 relational/typed/transaction contracts](docs/STEPS_3_TO_5_EXACT_INTERFACE_CONTRACT_V1.md), [Step 8 action/finalization contracts](docs/STEP_8_ACTION_AND_FINALIZATION_CONTRACT_V1.md), and [verification scenarios](docs/STEP_2_TO_8_VERIFICATION_MATRIX_V1.md). Previous language describing these exact interfaces as design-open is superseded **only at the v1 design specification level**; historical descriptions remain for decision provenance. No physical PostgreSQL migration, compiled DTOs, provider/domain adapter, actual grant probe, Docker implementation, running application or runtime/security/concurrency/model test was performed. **Implementation NOT STARTED; tests NOT RUN.** Implementation-time capacity, model/provider capability and specific customer Contract configurations are intentionally not locked by this architecture design. ADR-40 extra submission queues remain superseded.

## October 19 — Step 9 accepted provider/MCP architecture (design only)

Use [Step 9 v1 specification](docs/STEP_9_PROVIDER_ADAPTER_AND_SHARED_MCP_CONTRACT_V1.md). Implement one trusted provider-neutral model gateway, with initially DeepSeek, OpenAI and Anthropic adapter targets, optional qualified local model, per-original-member and separate Orchestrator/non-voting Integrator settings, provider-native tool/reasoning continuation, verified capability profiles, BYOK scoped secrets, data-egress consents, five user-approved spend pools and no silent model fallback. **Never create a dedicated MCP server per AI model**: model adapters normalize tool requests/results while Council's existing authenticated trusted tool broker and MCP client(s) mediate registered tool-service servers. MCP services can be shared across different models, but authorization always remains per actor/seat, grant, phase, customer and epoch; never give any sandbox direct MCP server credentials or bypass the broker using remote-provider hosted tool features. MCP tool discovery is untrusted metadata, not authority. External effects and provider costs stay under Part 5 operations and UNKNOWN reconciliation, Step 7 admission and immutable provenance. **Step 9 IN DESIGN — these are provisional interface proposals and agreed principles, not a completed operational design. Implementation not started and all qualification scenarios NOT RUN.**

## October 19 — ADR-43 supersedes optional Karpathy experimentation

The owner approved [mandatory substantive-work evidence-feedback](docs/STEP_8_KARPATHY_FIRST_AGENT_LOOP_AMENDMENT.md) as Council members' **normal operating loop**, including substantive work done by workers or Final Integrator under their existing permissions. Prior paragraphs describing experiments as *optional* are historical only for the core loop. Specific empirical tests are still context-dependent, and trivial actions do not require dummy experiments; when checking is unavailable mark NOT_RUN/BLOCKED/INCONCLUSIVE honestly. Existing Step 8 five-peer sealed checkpoints, member-authored readiness, non-voting Integrator, user acceptance, source consent, budgets and read-only verification /work remain. Step 9 gateway is deterministic routing/authorization plus applicable moderation, NOT an AI experiment supervisor. Step 8 **IN DESIGN** for exact operational binding; no implementation/testing.


## October 19 ADR-44 — approved feedback operating rules and checkpoint self-review

[Binding policy](docs/STEP_8_ADR44_FEEDBACK_CYCLE_AND_CHECKPOINT_SELF_REVIEW.md): every substantive Council approach uses hypothesis/approach, action, appropriate check, real observation or honest limitation, member-authored KEEP/REVISE/DISCARD/INCONCLUSIVE, durable evidence and self-directed repetition. Existing Step 6/8 records suffice; no extra experiment scheduler, quality judge, test per trivial action, fixed iteration quota or invented PASS. **Before every normal intermediate or final checkpoint, the original parent member must author an immutable, exact-version self-review** covering current objective/approach, observed evidence, unsupported assumptions, defects, unperformed checks and why it considers the version ready for *peer review*. Reference the report in existing readiness intent and freeze it for authorized peer access. Backend verifies only original-member authorship, presence, correct run/phase/generation and target hash; it does **not** judge intellectual sufficiency. Blocked/exhausted/incomplete work cannot fake review/readiness. The nonvoting Integrator similarly provides a versioned self-check with output-ready intent; actual checks and five genuine independent peer reviews remain distinct. **Policy APPROVED; exact runtime binding IN DESIGN; implementation NOT STARTED; tests NOT RUN.**


## October 20 ADR-45 approved nested member-loop policy

For substantive Council-member work, follow [ADR-45](docs/STEP_8_ADR45_NESTED_STRATEGY_EXECUTION_LOOPS.md): an **outer strategic approach/hypothesis/meaningful outcome-validation loop** encloses an **inner task execution, checking and repair loop**. Do not manufacture a new high-level hypothesis or outer disposition for each tool call, tactical correction or worker task. Continue meaningful intermediate checks; escalate early if evidence fundamentally undercuts the strategy; preserve exact material observations, conditional failures and truthful missing tests. Retain the original five-member autonomous reasoning model, parent-authorized workers, non-voting Integrator, ADR-44 exact-version self-review and all existing permissions/budget/checkpoint rules. This is an approved design rule, **not runtime implementation or test verification**.


## October 20 Step 9 ADR-46 — model tool sequence and cross-member MCP isolation

Follow [the approved tool isolation/ordering contract](docs/STEP_9_ADR46_TOOL_CALL_ORDERING_AND_MCP_ISOLATION.md): a model may propose several tool calls, but dispatch is **sequential within each model's current tool turn** for the MVP, preserving native IDs and observed results; no fabricated success or unsafe continuation after an UNKNOWN consequential effect. Concurrent **different-member** tool requests, including same registered read-only MCP tool, are permissible only with proven independent actor/customer/seat/credential/grant/target/cache/result scopes and backend resource admission. Do not use process-global mutable selected user/repo or an unrestricted shared session; split MCP clients/servers by isolation boundary or disable unsafe sharing. Protect conflicting external writes with resource-specific target gates/preconditions through existing broker/Step 5 operations—not database locks held across network I/O—and do not add another global queue, MCP-specific scheduler or model-specific MCP servers. **Step 9 remains IN DESIGN; no implementation or executed acceptance tests.**
