# Implementation handoff

**October 13, 2026 amendment:** [decision/status index](ARCHITECTURE_DECISIONS.md). Requirements below are specifications; application implementation is NOT STARTED and runtime tests are NOT RUN.

## Status and authority

This is a handoff for a later explicitly authorized implementation. The current delivery is a documentation repository, not an application. The owner approved the design and requested that it be placed in a new repository.

Read [the complete design](APP_DESIGN.md) first, then the [PostgreSQL data model](POSTGRES_DATA_MODEL.md) and [Part 4 typed interaction/state contracts](TYPED_INTERACTION_CONTRACTS.md), and [AGENTS.md](../AGENTS.md) next. The complete design remains authoritative over this operational summary. Later owner instructions may change the scope; record such changes rather than silently interpreting this handoff as permission for unrelated work.

The older single-lead swarm starter is not a valid implementation baseline. Do not import its fixed managerial structure, coding-first assumptions, dashboard, or runtime as if they implement the approved council.

## Model billing and credentials — MVP versus deferred

MVP requires **BYOK for all remote providers** (or compatible local models that need no remote API key). The user connects their own API credentials and approves Council's project/phase token-and-cost allowances. The provider bills the user directly. Do not build a prepaid Council wallet, token reseller, or Council-paid provider account as an MVP dependency. Council budget reservations restrict Council-originated calls; they are not a guaranteed cap on a provider's final invoice, especially for uncertain/late usage or non-Council calls on the same key.

Raw BYOK secrets must remain in trusted per-user/deployment credential storage, never in agent-controlled containers, project artifacts, repositories, normal logs or browser persistence. Expose scoped model-call capabilities through the trusted bridge only; support rotation/revocation and fail closed on unauthorized credential access. BYOK lowers Council's billing exposure but does **not** make key handling automatically secure.

**Deferred option, explicitly retained for a later product decision:** optional Council-managed inference billing, prepaid service credits/wallet, and/or per-token markup. This requires separate provider-commercial, payment-processing, metering/reconciliation, fraud/chargeback/refund, taxation/compliance and financial-risk design. Do not label it specified, implemented, or required in the MVP. Any platform subscription is separate from provider API payments.

## Product outcome

Build accountable parallel investigations, not an agent chatroom. The three defining graph capabilities are:

1. Trace conclusions depending on a specific source or assumption, including alternative supporting routes and affected report sections.
2. Explain claim narrowing using actual claim versions, a recorded challenge, relevant evidence, and the revision decision.
3. Trace apparently independent findings to shared original evidence, retaining unresolved provenance rather than guessing independence.

Use ordinary searchable records, evidence, checkpoints, and short handovers alongside the graph. Do not imply that a graph removes finite context windows.

## Ordered milestones

### A. Foundation

Establish canonical versioned records, scope/authorization checks, immutable source versions, observable execution events, and typed graph relationships. Implement the Part 5 transaction contract: atomic canonical mutations + events/outbox, scoped idempotency, expected-version conflict rejection, durable external operations with UNKNOWN reconciliation, and lease-token protected task completion. Implement the Part 4 command/event envelopes, State Contract registry, scoped lifecycle/activity projections, durable interaction requests, and stale/idempotent user-action guards as foundation primitives rather than UI-only features. Keep assumptions, grouped premises, and alternative support paths explicit.

Implement the Project Orchestrator boundary first: user conversation -> versioned canonical project prompt -> durable PROJECT_CONTRACT_APPROVAL interaction -> explicit user decision -> stable prompt delivered consistently to Council members. The approval interaction must expose Approve & launch, Request changes, Reject current approach, and Cancel project with the exact transition semantics in TYPED_INTERACTION_CONTRACTS.md. Council members/workers may originate questions to the user, but raw user replies must return through the Orchestrator before the processed answer reaches the requesting agent. The Orchestrator also derives the initial project-specific semantic checkpoint plan from the canonical prompt. This milestone planning must not become solution supervision.

Implement the PostgreSQL-backed task queue with leases and reconciliation. Add provider adapters and a configurable capability registry. Use synthetic/prepared evidence before connecting live sources.

Exit condition: the three graph questions work against deterministic fixtures; authorization also applies to traversal, source snippets, search, context assembly, and exports. A council cannot start without an approved Project Contract, and recorded tool failure cannot be mistaken for a successful check.

### B. Working council

Implement equal council seats, independent private investigation branches, dynamically commissioned workers, targeted cross-examination, revisions, coverage records, and bounded minority investigation. Implement the Step 6 provenance contract so evidence, assumptions, analysis, claims, challenges, revisions, and support groups remain traceable to exact sources/tests/repos/environments while runtime-observed relationships stay distinct from agent-authored interpretations.

Implement the following checkpoint boundary; it replaces the former collaborator-access flow.

**LOCAL-FIRST REDESIGN (ADR-17):** Each Council member owns a customer-controlled local Git repo/worktree inside its sandbox. The trusted host-side repository gateway exports a selected, immutable, pinned, hash-verified **read-only snapshot** at an approved checkpoint; authorized peers receive only this frozen snapshot, not the original repository history/admin credentials or writable member workspace. No GitHub account or internet-public repository is needed.

The gateway records the snapshot/manifest, authorization, read-grant and exact delivered recipient scope in canonical Council control records. A failed or UNKNOWN snapshot export/grant blocks SEALED_REVIEW until observed and reconciled; closing revokes temporary peer routes/grants and checks isolation before private revision. A public or remote Git backend is optional and separately customer-authorized. Even local source requires separate permission for egress to remote LLMs/APIs. Full source control is customer-owned. Reference [LOCAL_REPOSITORY_AND_KNOWLEDGE_RETENTION.md](LOCAL_REPOSITORY_AND_KNOWLEDGE_RETENTION.md).

Checkpoint sequence: all-five arrival barrier -> verify local pinned frozen snapshot scope -> grant scoped peer read-only access -> SEALED_REVIEW -> shared REVIEWING -> CLOSING -> verified temporary access/route revoke -> CLOSED/private revision.

During SEALED_REVIEW each member independently submits an immutable assessment bound to the checkpoint, candidate SHAs, reviewer identity, evidence, objections, and proposed tests. The gateway withholds peer assessments and shared debate until every required member has submitted. Reviews remain in scoped canonical storage, never in a public repository or shared retrieval cache before reveal. Protected checkpoint/review token/cost budgets apply; a missing or budget-exhausted reviewer cannot be counted as done and blocks reveal or leaves it explicitly incomplete/aborted. No fabricated fifth assessment. No fixed skeptical personas or forced disagreement are required.

Executable peer tests use a separate disposable verification environment, never a reviewer's persistent branch environment. It has pinned read-only inputs and isolated scratch storage; it cannot write member repositories, continuation files, protected acceptance definitions, or control-plane state. Provider/admin credentials and unrestricted network access are absent. The requester still chooses and interprets the test. A trusted runner records actual snapshot/environment/harness hashes, command, execution outcome, and exported output hashes. Candidate-supplied tests remain distinguishable from protected acceptance checks. Recorded execution is evidence of what ran, not automatic proof of methodological adequacy.

Communication completion, verification coverage, candidate readiness, and user acceptance are separate records. DISPUTED or DEFERRED can satisfy a response obligation without resolving the underlying risk or passing an acceptance criterion. Required checks remain NOT_RUN, BLOCKED, FAILED, or PASSED with evidence; an explicit policy waiver is recorded separately and is never a test pass. Forced closure records incomplete review and outstanding obligations.

MarkCheckpointCommunicationDone carries checkpoint_generation, processed_message_sequence, and expected_obligation_version. Under the same checkpoint lock/version guard used to accept messages/actions and close the checkpoint, reject stale declarations, unanswered required obligations, unprocessed required messages, or active verification work. A relevant accepted message or new required action invalidates the affected DONE certificate and reactivates that member. Delivery to a socket is not evidence of processing. Internal bookkeeping alone must not endlessly invalidate completion. Close atomically only after current certificates cover the current review/obligation frontier; record ceiling-forced closure distinctly.

The UI and final review expose communication_closed, verification_coverage, candidate_readiness, and acceptance_decision independently. An incomplete candidate may be presented for an informed user decision where the existing contract allows it; presentation or acceptance does not alter failed/unperformed verification.

Implement budget reservations, branch limits, delegation limits, progress checks, and a protected review allowance. Schedule whole Council-member work environments under host capacity rather than centrally scheduling their private internal tasks. When a member reaches a semantic checkpoint, freeze/record its checkpoint state, release its scarce work slot, and prevent it from advancing past the barrier until all required members reach that same checkpoint and the checkpoint review closes. After the barrier opens, do not require all five sandboxes to execute simultaneously: rotate the same logical member sandboxes through available slots, durably queue checkpoint traffic/actions for inactive members, and reschedule a previously-DONE member if a new required action targets it. When a member releases a slot, quiesce and persist the sandbox's durable project/environment state, stop the execution container to free compute, and later reconstruct the same logical sandbox. Do not persist temporary provider/checkpoint/peer-access credentials as durable sandbox state; reissue them only when currently authorized. For crash recovery, revoke the dead member's execution bridge epoch before restart/resume, cancel known in-flight external calls where supported, reconcile unknown outcomes, validate the reconstructed sandbox from outside the agent boundary, then issue a fresh bridge epoch and capabilities.

For executable projects, default to Council-managed isolated project environments rather than host cloning. Branches may add authorized packages, runtimes, services, and configuration as part of their candidate. Capture those changes in reproducible environment definitions and require a clean rebuild plus applicable acceptance checks before a candidate is treated as reproducible.

Host matching is optional and only used when the Project Contract explicitly requires host-specific behavior. Implement it as Project-Contract-scoped profiling -> sanitized versioned Host Profile -> proposed Environment Contract -> explicit user approval -> common host baseline for all branches plus candidate-specific overlays. Record required capabilities as exact, compatible, bridged, or unavailable.

Keep the main Council application unprivileged. Implement a separate local privileged broker that requests elevation only when a specific Match My PC capability requires it. On Windows, use on-demand UAC/admin approval for the broker rather than requiring the whole app to run as Administrator. The broker must expose typed allowlisted operations and must not provide agents with a generic admin shell, unrestricted filesystem access, raw Docker-daemon access, or kernel control.

Treat host matching and host mutation as separate permissions. Installing or changing software, services, drivers, system configuration, or non-project files on the real host requires explicit additional authorization, audit records, and cleanup/rollback behavior where practical. Detect material drift in Project-Contract-relevant host capabilities and invalidate affected exact-match verification until revalidated.

Support custom user-supplied environment definitions as another optional path. Keep unrelated host files, credentials, browser state, caches, applications, and projects unavailable by default.

Keep host-aware executable scheduling separate from logical council membership. Queue local builds/tests/tools according to CPU, memory, disk, GPU/device, and sandbox limits instead of oversubscribing the user's computer.

The accepted project environment is part of the deliverable. Remove Council agents, provider credentials, agent/local Git access credentials, hidden Council control mechanisms, and orchestration-only tooling from the delivered runtime. Persist the reproducible project/environment definition and required project data.

Before destroying the Council deployment, export the accepted project plus a compact reusable learning package to Git for the owner's future Council runs. Preserve useful final architecture, capabilities/stack metadata, important successful and failed approaches, acceptance/test results, reusable patterns, and prior-project reuse links where relevant. Do not preserve the Council PostgreSQL database merely as history.

After the accepted project and Git learning archive are verified, delete the Council control PostgreSQL volume, runtime/session state, checkpoint machinery, temporary peer copies, caches, credentials, and disposable sandbox residue. A database that belongs to the accepted product itself is project data and is not the Council control database.

Exit condition: a non-coding investigation completes without a terminal, valid minority objections survive, administrative voting cannot promote evidential status, checkpoint visibility follows policy, more logical agents than local execution slots can make progress safely, and an executable candidate can be rebuilt cleanly from retained definitions. In Match My PC mode, the approved Environment Contract is reproducible/auditable, privileged operations remain broker-mediated, host mutation cannot occur implicitly, and material host drift invalidates stale exact-match claims.

### C. Continuity and review

Implement persistent logical agents with versioned sessions, bounded context packets, graph-assisted retrieval plus ordinary search, safe checkpoints, and pending-operation reconciliation.

Add provisional synthesis, independent six-month-plus premortem, reopened checks, final review dispositions, and versioned reports with editorial-only assembly authority.

Exit condition: forced rollovers preserve old objections and current claim versions; missing graph edges can be overcome through underlying search; a premortem scenario never becomes an observation.

### D. Interface and hardening

Build the views defined in section 11, including per-agent model dropdowns, context/session inspection, graph filtering, bounded expansion, edge provenance, original evidence viewer, and accessible table alternatives.

Add safe model migration, provider-specific data permissions, usage inspection, recovery, export, retention, and backup restoration checks.

Exit condition: the UI exposes recorded facts rather than an invented activity narrative. Exported claims remain traceable to permitted retained evidence. Interrupted workers and reconnecting clients reconcile state correctly.

### E. External evidence integrations

Connect authorized sources and a RAG adapter through the same evidence and capability contracts. Retrieval returns source-level evidence, context, scope, and limitations, not an unquestionable generated answer.

Exit condition: branches can perform independent searches, inspect original material, and seek counterevidence without granting source text instruction authority or expanding permissions.

## Verification expectations

Section 17 of the complete design is the acceptance suite, not a claim that tests already exist or pass. Add deterministic tests for runtime invariants and repeated evaluations for model-dependent behavior.

Separate test-provider runs from live DeepSeek requests. Separate local script execution from actual sandbox integration. Report which verification was performed and which was unavailable.

Compare graph-assisted continuation with a strong searchable-record baseline containing the same underlying information. Compare council performance with a capable single-agent baseline before claiming improvement.

## Implementation-time decisions that remain open

The design specifies behavior without pretending every parameter is settled. Resolve and document the exact model identifiers and capability checks, version pins, budget amounts and review-reserve allocation, context sizing and retrieval ranking, evidence-policy profiles, source adapters, secret-store implementation, and deployment configuration when work starts.

These open choices do not authorize replacing the peer council with a supervisor, removing provenance, or broadening the product into an unrestricted coding/deployment agent.

## Reporting a completed implementation step

Describe the behavior delivered, affected records and boundaries, tests actually executed, known limitations, and next unfinished milestone. Do not equate more messages or graph nodes with a better investigation. Do not label proposed work as implemented.

## Step 8.2a accepted — rely on Docker-native member persistence, not worker recovery infrastructure

- Provision stable isolated **named Docker volume(s)** (or explicitly authorized persistent bind mounts) for each Council member's private workspace, Git state, worker-generated results/notes/progress and reproducible project configuration; volume ownership must remain pinned to the logical member, not a disposable container ID. Ensure safe mount scopes, backup and authorized final cleanup; no sibling member can mount the private volume.
- Whole member sandbox is stopped/recreated to free host resources. Mounted volume files survive as long as retained, but container writable layer and tmpfs are not durable across recreation, and Docker **does not restore running subagent processes or in-memory model state** on restart. The member (not a Council manager) decides how to relaunch/skip/repeat local worker tasks from persisted files. If a worker never saved its state, restarting that worker may repeat the work.
- **Do not build a Council per-worker restart table/daemon, process snapshot/CRIU integration, scheduler, arbitrary worker count/depth cap, or mandatory worker result/merge orchestration.** The existing Council canonical operation/evidence records remain required for consequential effects and claims; a resumed member cannot blindly redo UNKNOWN provider/tool calls.
- Deliberately stopped checkpoint-ready, PAUSED or BUDGET_EXHAUSTED sandboxes must not auto-restart. Do not set unconditional Docker `always`/`unless-stopped` restart behavior which bypasses the Council slot scheduler, budget/permission gate, phase barrier, execution epoch or resource checks. Council's trusted whole-member backend controls start/stop/recreate, reacquires existing volume after validating mount identity/isolation, reconciles external outcomes and issues a fresh authorized bridge epoch.
- Required Step 10 implementation evidence remains: Docker named-volume persistence after container recreation and OOM, unauthorized sibling mount denial, correct intentionally stopped behavior across Docker daemon restart, repair/resume without duplicate external side effects, and final archive/volume cleanup safety. These tests are **NOT RUN**.

This closes the **ordinary worker persistence and restart design choice** at the policy level. It is **not** proof that a live worker can resume its CPU instruction pointer, or that a Docker-backed Council runtime has been implemented.

## Step 8.2 accepted — sandbox-local worker autonomy and trusted resource monitoring

The owner approved that a Council member can create **any number and depth of internal subagents, worker processes and tasks** inside its own sandbox, subject to that sandbox's aggregate host resource limits, branch security and approved provider token/cost budget. **No separate global internal-worker scheduler or worker-count/depth quota.** The five Council logical seats and the Step 7 whole-member sandbox admission schedule remain unchanged. Local workers are not automatically Docker containers; agent sandboxes do not receive the Docker socket.

**MVP monitor and enforcement handoff:** implement one trusted deployment/host-side Resource Monitor reading Docker Engine `GET /containers/{id}/stats` and container OOM/die/lifecycle events for CPU, RAM, PID/thread count, network and block I/O across the **whole** member container. Apply supported Docker/cgroups hard memory/CPU/PID limits. Sample roughly **every 2–5 seconds** initially with freshness tracking and configurable thresholds: at ~80% of container assigned RAM warn and restrict additional **broker-mediated heavy admissions**; near ~90% deny new heavy brokered work and durably quiesce the entire member if pressure continues. This **does not prevent** an arbitrary agent-created process from exhausting RAM between samples; OOM kill/crash/recovery is real and must be observed, fenced and reconciled rather than called completion.

In addition to per-container stats, measure **host RAM headroom** (initial adjustable ~20%), Docker Desktop/WSL2 Linux VM memory/swap separately on Windows, free disk/volume/log and workspace quotas rather than mistaking block I/O for free space, and allowed NVIDIA GPUs through NVML/`nvidia-smi` if supported. GPU metrics and enforced per-container VRAM caps cannot be assumed to exist; use conservative allocation when unavailable. The monitor is trusted software outside agent control; no direct unrestricted Docker daemon API/socket inside any candidate/member sandbox. Optional separate child-containers must go through trusted scoped broker provisioning and aggregate parent accounting, not uncontrolled Docker-in-Docker.

**Failure boundaries:** missing/stale metrics => no **new** heavy work admission without reliable evidence; do not mark a running agent FAILED just for one missed sample. Prolonged pressure => stop new broker admissions, throttle, safe whole-sandbox quiescence, backend-confirmed resource release. OOM/crash => record incident/epoch, retain UNKNOWN external effects and proceed through the existing three-retry Step 7 recovery, preserving logical member identity/phase and unaffected Council seats. No thresholds claim to guarantee no crashes.

**Scope/status:** accepted **Step 8.2 resource/worker policy** and **Step 8.2a Docker volume persistence**. The parent member owns all ordinary worker restart/merge choices; no central worker recovery architecture remains to specify. Step 8 remains **IN DESIGN** for exact member action protocol and final-phase/checkpoint/termination conditions; implementation and runtime tests remain **NOT STARTED / NOT RUN**.

## Step 8.1 accepted — nested member reasoning and optional Karpathy-style experiments (October 14)

The member's existing general-purpose agentic loop can optionally perform a Karpathy/autoresearch-inspired experiment **under ACT**: `HYPOTHESIS -> CHANGE/ALTERNATIVE -> TEST/CHECK -> OBSERVE -> KEEP/REVISE/DISCARD/INCONCLUSIVE -> RECORD`, then return to the same member loop. This is an **optional workflow** chosen by the member, not a fixed procedure after every action, a second AI supervisor, scheduler, quality scorer, or coding-only optimizer. For research/noncoding work, `TEST/CHECK` may be evidence comparisons, counterexamples and assumption checks rather than numerical benchmarks.

The experiment/attempt ledger must preserve attributable hypothesis, baseline and changed source/repo SHA or alternative, versioned test/data/environment inputs, durable operation IDs, results/failures/regressions, units/measurement conditions or qualitative evidence, limitations, and the member's own KEEP/REVISE/DISCARD/INCONCLUSIVE disposition. Failed/reverted code need not be retained, but the **evidence and experiment outcome record** remains. Agent-edited exploratory tests never replace trusted protected acceptance tests.

Delegated workers may run an authorized branch-local experiment using the parent's capabilities and phase token/cost allowance. They return evidence/results to the parent; they cannot mark the parent CHECKPOINT_READY, publish peer-private work, or silently merge changes. **Step 8.2 fixes no arbitrary internal worker count/depth cap or separate Council scheduler**; Step 8.2a establishes member-owned Docker volume files as the ordinary worker recovery boundary. Exact per-member action/observation and final/phase transition contracts remain to design, not a special Council per-worker restart manager.

At a checkpoint, sealed review and private local pinned snapshot scope/read-only rules still apply. `/work` uses disposable **verification-only** sandboxes: no authoritative candidate edits or pushes, and no overriding protected evaluation. Subsequent private revisions wait for verified checkpoint closure. Experiments survive session rollover under the same logical member, and a budget limit cannot force intellectual completion.

**Design status:** only Step 8.1 is accepted, with [the working Part 8 specification](PART_8_AGENT_LOOP_EXPERIMENTATION_DELEGATION.md). **Step 8 remains IN DESIGN; runtime implementation NOT STARTED and tests NOT RUN.** The remaining Step 8 areas are action/worker lifecycle, delegation ceilings, final candidate/termination transitions, and checkpoint integration.

## October 14 Steps 3–5 design closure (implementation explicitly pending)

Steps **3, 4 and 5 are DESIGNED**, and their authoritative normative closure sections are [Part 3 §20](POSTGRES_DATA_MODEL.md), [Part 4 §26](TYPED_INTERACTION_CONTRACTS.md) and [Part 5 §16](PART_5_TRANSACTIONS_IDEMPOTENCY_CONFLICTS.md). Application code, migrations, test execution and provider/sandbox integration remain **NOT STARTED / NOT RUN**.

Implementation order once explicitly authorized:

1. Define/version the temporary per-deployment `council_core` and `council_runtime` migrations with exact five-seat uniqueness, same-run foreign-scope constraints, append-only immutable versions, branch/RLS policies, command receipts and committed event clock. Add checkpoint arrivals, approved full public-history manifests and externally observed transitions, sealed reviews/reveal, transcript/action/obligation/frontier/DONE, budget accounts/operation attempts, scoped clarification lineage, archive validation.
2. Generate typed v1 command/event/result schemas and the State Contract registry from Part 4. Enforce user/Orchestrator/member/runtime authority. Retried commands with same scoped key/request hash return the saved authorized result **before** stale/transition guards; do not repeat effects. Reject cross-branch scope, changed hash, stale version, and unauthorized transitions.
3. Implement Part 5's one-transaction aggregate + operation-intent + event-clock + outbox + receipt, ordered locks and idempotent runtime queue. Make local snapshot export/grant/revoke, optional explicitly approved external Git/provider/Docker actions and customer-owned permitted Git archive export separate durable operations, reconciled against observed truth. Do not claim external success on request/timeout. Keep resource/budget reservations until safe settlement.
4. Exercise **deterministic failure-injection tests** before connecting real models: simultaneous budget callers, idempotent approval retry after run advances, lower-position outbox delayed publication, disconnect/reconnect SSE, sealed fifth-review/reveal race, /done vs new required action, full repo-public and failed-private transitions, old bridge/lease tokens, and accepted Git archive restore/reference closure. Testing one stub or static schema does not prove runtime correctness.
5. Only then integrate Step 8 agent-loop policy, Step 9 provider/local-model adapters, Step 10 verified sandbox isolation and Step 11 memory retrieval/promotion, preserving the above authorization, evidence and transaction boundaries.

**Do not mark any Part 3–5 runtime item IMPLEMENTED or VERIFIED until code references and executed scoped test evidence are available.** No database schema, endpoint, or production workflow has been deployed by this design-specification task.

## October 14 completed Step 7 design handoff (specification only)

The accepted Part 7 design is [PART_7_MEMBER_SCHEDULING_RECOVERY_RESOURCES.md](PART_7_MEMBER_SCHEDULING_RECOVERY_RESOURCES.md). Its **design** status is DESIGNED. No queue/scheduler, budget provider adapter, container backend, safety checker, DB migration, or runtime test has been implemented or run by completing this document.

- Show the user a **configurable starting split of 70% private development, 25% checkpoint/review, and 5% orchestration/finalization**, with equal *monetary* development shares across the five members as a proposal (not equal tokens). Require explicit approval of hard run, per-member/per-phase token/cost caps and protected reserves. BYOK bills user through the external model provider; no Council wallet.
- Initial inference limits: at most **two remote calls per provider** (always subordinate to provider/account rate limits) and **one local inference job** pending tested safe model/runtime/hardware concurrency; do not add a second intellectual scheduling policy. The existing fixed seat order applies when sandbox slots become free.
- Initial host RAM headroom target **around 20%**, adjustable upward from observed OS/runtime needs; check VRAM separately, stop new admissions under pressure, and confirm released resources before slot reuse.
- Infrastructure recovery default **three retries after initial failure with 5/30/120 second delays**; on exhaustion mark the required member BLOCKED with durable state. Use operation-specific timeouts with provider/tool overrides, not reasoning deadlines or mandatory private-work slices.
- Before each external request, obtain Part 5 **transactional event clock lock first**, then deterministic **run -> spend pool -> member/phase** budget locks, validate token and currency ceilings and capacity, and atomically commit the operation + idempotent reservation + outbox. External dispatch occurs only after commit; settle definite usage, retain uncertain reservations, and require fresh authorization for retries.
- PauseRun = ACTIVE with `QUIESCING_FOR_PAUSE` activity until durable quiescence and verified resource release, then PAUSED; ResumeRun revalidates all authority/resource/operation guards; StopRun enters STOPPING and becomes CANCELLED only after adequate cleanup (else FAILED/incomplete). User candidate acceptance and final Git archival remain distinct from Stop.
- `BUDGET_EXHAUSTED / INCOMPLETE` means a phase did not reach agent-declared readiness. It neither clears an all-five checkpoint barrier nor allows the Orchestrator/runtime to judge intellectual completion. User-approved budget extension creates a new version; rejection leaves a truthful partial/blocked state.
- Optional project/phase token estimates are uncertain, non-binding ranges, never defaults for spending approval; if no historical support, show insufficient data.

**Implementation dependency boundary:** Part 3 must supply canonical budget/resource/recovery records and constraints; Part 4 must expose appropriate typed commands, activities, events, and transitions; Part 5 provides atomic reservations and unknown-outcome reconciliation. Step 9 owns provider/local-model compatibility, pricing, token-metering and rate adapters. Step 10 owns the Docker sandbox checker, volume durability, and proved resource release. Their code and runtime acceptance tests remain pending; none are implicitly completed by this architecture approval.

## October 13 implementation ordering and open work

Finish the per-member/per-phase token/cost budget admission and exhaustion-as-incomplete behavior, blocked-member handling, operation-specific recovery, atomic reservations, and commit-safe event replay before large UI work. Implement disposable verifiers and sealed review next, then exercise a one-slot five-member run with phase-budget exhaustion, authorized top-ups, forced restarts, and concurrent completion/message races.

The Orchestrator defines a semantic phase plan; each member works until its own CHECKPOINT_READY, genuine blocking, or authorized per-phase token/cost exhaustion. No mandatory periodic work slices, fixed iteration counts, or reasoning deadlines. If budget is exhausted first, preserve the incomplete phase and let the user authorize a top-up or cancel; do not force readiness, /done, or acceptance. Keep checkpoint/review reserve separate. Use provider/tool safety timeouts only for potentially stalled individual operations. Optional overall-project and per-phase token/cost forecasts are explicitly uncertain planning ranges calibrated to historical evidence where available, never hard limits or automatic top-ups.

Checkpoint milestones specify outcomes/evidence to review, not a preferred sequence of solution components unless the user required those components. For example, require a reproducible baseline and measured failure modes rather than requiring every retrieval design to add reranking and fusion.

Processed clarifications retain links to source user statements, scope, semantic strength (preference, requirement, permission, prohibition, or unresolved ambiguity), and the exact contract revision. Raw answers remain retained for authorized audit/user confirmation, not delivered directly to agents. Material ambiguity and consequential changes to permissions, spending, publication, or requirements require the appropriate explicit confirmation. Ordinary faithful rewording does not add an Auditor bottleneck.

Branch-local clarification context stays branch-local in the Orchestrator's memory, retrieval, caches, and later normalization, not just in outgoing messages. Only approved project-wide revisions enter shared clarification context. The Orchestrator still has no solution-selection or intellectual supervisory authority.

Pre-register tasks, model/tool permissions, total budget, evaluation method, trial count/variations, and reporting rules. Compare: (A) a strong single agent with the comparison budget; (B) five independent attempts with a fixed external evaluation/selection procedure and no peer discussion; (C) five members with sealed review, discussion, and revision; and (D) targeted ablations such as without sealed review or graph-assisted retrieval. Use the same protected evaluation procedure where applicable, retain unsuccessful trials, and report cost-matched quality separately from wall-clock latency/resource use.

Measure defects uniquely found through peer review, valid corrections incorporated, regressions introduced after review, unresolved required checks, and total spend including review. An evaluation procedure scores experimental outcomes; it does not replace the user's authority to accept a delivered candidate. Static documentation checks are not evidence that Council improves quality. Live evaluation and statistical conclusions remain NOT RUN.

See ARCHITECTURE_DECISIONS.md and architecture_contract.json for amendment status. Documentation checks do not complete runtime steps. Step 7 design and proposed defaults are specified; its adapters, schema migrations, lifecycle wiring, backend enforcement and runtime tests remain NOT STARTED / NOT RUN. Step 8 still needs the full agent loop/termination policy; Step 11 still needs concrete memory selection, archive promotion, and validation implementation.

## Owner-approved October 14 local-first/source-retention redesign and failure-memory fix

- **Source storage:** native Git on customer-controlled machine/server by default. Forgejo/self-hosted enterprise Git adapter can be chosen later; no mandatory hosted Git account, automatic public repository, vendor source upload, or per-member remote Git administrator credentials. Git supplies version control; Council PG supplies checkpoint permissions/messages/provenance; local object/artifact storage supplies immutable selected read-only snapshots. See [the new authoritative decision](LOCAL_REPOSITORY_AND_KNOWLEDGE_RETENTION.md).
- **Checkpoint:** replace former `PublishCheckpointRepositories` and `MakeCheckpointRepositoriesPrivate` default semantics with `PublishCheckpointSnapshots` (verified hash + scoped grant) and `RevokeCheckpointSnapshotAccess` (verified access/route closure). This is a design change, **not** already implemented API. Keep all-five sealed assessments, peer communication checks, and verification-only `/work` unchanged. Do not expose whole Git history/refs unless specifically authorized. Keep UNKNOWN external-effect accounting/reconciliation.
- **Retention:** customer controls whether to retain accepted project source, environment/recipe and evidence locally. A vendor/shared general library may contain independently permitted patterns; it must not incorporate customer-derived material without **specific informed customer permission and privacy/IP/licensing review**, and must never assume acceptance/public checkpoint means release.
- **Memory ranking:** prioritize prior **working approaches** that fit new objectives and constraints; failed approaches remain `FAILED_IN_CONTEXT` warnings/test ideas, not prohibitions merely because a previous case was similar. Compare versions, configuration, workload, scale, constraints and demonstrated failure mechanism. An agent may retest even a close match. Success likewise cannot be presumed universal. Step 11 details remain **IN DESIGN**.
- **Truthful status:** earlier Step 2–5 design baseline was coherent for public GitHub; ADR-17 reopens its affected interfaces for local snapshot/consent changes. Local gateway implementation, UI, SQL migrations, consent enforcement, memory retrieval and all live tests are **NOT STARTED / NOT RUN**. Do not claim Steps 2–5 remain fully closed under a superseded source sharing policy.
