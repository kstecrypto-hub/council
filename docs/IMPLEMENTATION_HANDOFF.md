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

Each of five fixed logical Council members owns its candidate repository under its own GitHub identity. Between checkpoints it is private. At an approved checkpoint the trusted runtime makes the member repositories **public on GitHub**, records exact frozen commits and observed visibility, and later makes them private again before private development resumes. Peer collaborator grants are not the publication mechanism. Reviewers never receive another member's write or administration credentials.

Public means internet-wide publication, not merely access for Council peers. Approval must cover all repository content/history and other surfaces made public, including logs, releases, and artifacts where applicable. Secrets, personal/private inputs, unapproved intellectual property, and sealed reviews must stay outside the published repository. A publication manifest records approved refs/history, content hashes, scope, and authorization; checking only the latest checkout is insufficient. A failed safety check blocks publication. A confidential project that cannot authorize this exposure cannot use this publication mode; do not silently publish it or silently substitute a different protocol.

Once published, copies and public forks cannot be recalled by making the original private. The private transition protects later unpublished work, not already disclosed information. Runtime-controlled outbound access, repository writes, comments/issues, caches, and retrieval must not provide hidden inter-member communication outside the checkpoint protocol. Public read access is not write access, and visibility is not a frozen-snapshot guarantee: record/pin approved SHAs and enforce the write freeze outside member control.

Visibility changes are durable external operations. OPENING cannot declare publication successful until observed state is verified. Partial/unknown publication blocks review and is reconciled; any real exposure is recorded even after rollback. On closing, terminate communication authority, make repositories private, verify visibility and required isolation controls, and only then permit new private commits. A failed private transition keeps affected work blocked. This policy applies to generated member repositories, not to the Council source repository itself.

Checkpoint sequence: all-five arrival barrier -> freeze and publication safety checks -> public repositories -> SEALED_REVIEW -> shared REVIEWING -> CLOSING -> confirmed private visibility -> CLOSED/private revision.

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

The accepted project environment is part of the deliverable. Remove Council agents, provider credentials, agent GitHub credentials, hidden Council control mechanisms, and orchestration-only tooling from the delivered runtime. Persist the reproducible project/environment definition and required project data.

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

## October 13 implementation ordering and open work

Finish the per-member/per-phase token/cost budget admission and exhaustion-as-incomplete behavior, blocked-member handling, operation-specific recovery, atomic reservations, and commit-safe event replay before large UI work. Implement disposable verifiers and sealed review next, then exercise a one-slot five-member run with phase-budget exhaustion, authorized top-ups, forced restarts, and concurrent completion/message races.

The Orchestrator defines a semantic phase plan; each member works until its own CHECKPOINT_READY, genuine blocking, or authorized per-phase token/cost exhaustion. No mandatory periodic work slices, fixed iteration counts, or reasoning deadlines. If budget is exhausted first, preserve the incomplete phase and let the user authorize a top-up or cancel; do not force readiness, /done, or acceptance. Keep checkpoint/review reserve separate. Use provider/tool safety timeouts only for potentially stalled individual operations. Optional overall-project and per-phase token/cost forecasts are explicitly uncertain planning ranges calibrated to historical evidence where available, never hard limits or automatic top-ups.

Checkpoint milestones specify outcomes/evidence to review, not a preferred sequence of solution components unless the user required those components. For example, require a reproducible baseline and measured failure modes rather than requiring every retrieval design to add reranking and fusion.

Processed clarifications retain links to source user statements, scope, semantic strength (preference, requirement, permission, prohibition, or unresolved ambiguity), and the exact contract revision. Raw answers remain retained for authorized audit/user confirmation, not delivered directly to agents. Material ambiguity and consequential changes to permissions, spending, publication, or requirements require the appropriate explicit confirmation. Ordinary faithful rewording does not add an Auditor bottleneck.

Branch-local clarification context stays branch-local in the Orchestrator's memory, retrieval, caches, and later normalization, not just in outgoing messages. Only approved project-wide revisions enter shared clarification context. The Orchestrator still has no solution-selection or intellectual supervisory authority.

Pre-register tasks, model/tool permissions, total budget, evaluation method, trial count/variations, and reporting rules. Compare: (A) a strong single agent with the comparison budget; (B) five independent attempts with a fixed external evaluation/selection procedure and no peer discussion; (C) five members with sealed review, discussion, and revision; and (D) targeted ablations such as without sealed review or graph-assisted retrieval. Use the same protected evaluation procedure where applicable, retain unsuccessful trials, and report cost-matched quality separately from wall-clock latency/resource use.

Measure defects uniquely found through peer review, valid corrections incorporated, regressions introduced after review, unresolved required checks, and total spend including review. An evaluation procedure scores experimental outcomes; it does not replace the user's authority to accept a delivered candidate. Static documentation checks are not evidence that Council improves quality. Live evaluation and statistical conclusions remain NOT RUN.

See ARCHITECTURE_DECISIONS.md and architecture_contract.json for amendment status. Documentation checks do not complete runtime steps. Step 7 still needs defaults, adapters, state wiring, and tests; Step 8 still needs the full agent loop/termination policy; Step 11 still needs concrete memory selection, archive promotion, and validation implementation.
