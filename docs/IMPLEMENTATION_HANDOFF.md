# Implementation handoff

## Status and authority

This is a handoff for a later explicitly authorized implementation. The current delivery is a documentation repository, not an application. The owner approved the design and requested that it be placed in a new repository.

Read [the complete design](APP_DESIGN.md) first, then the [PostgreSQL data model](POSTGRES_DATA_MODEL.md) and [Part 4 typed interaction/state contracts](TYPED_INTERACTION_CONTRACTS.md), and [AGENTS.md](../AGENTS.md) next. The complete design remains authoritative over this operational summary. Later owner instructions may change the scope; record such changes rather than silently interpreting this handoff as permission for unrelated work.

The older single-lead swarm starter is not a valid implementation baseline. Do not import its fixed managerial structure, coding-first assumptions, dashboard, or runtime as if they implement the approved council.

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

Implement checkpoint execution around each Council member's own repository. Between checkpoints, peer repos are private. At checkpoint entry, temporarily grant participating peers read access, record each repo's exact opening commit, and allow peers to inspect/clone/test the visible repositories without write access. Keep authoritative candidate repositories frozen during checkpoint review; verification may use frozen/disposable copies, and implementation commits resume only after checkpoint closure. At checkpoint close, revoke reciprocal access and return branches to private development while preserving what they legitimately learned. Implement peer discussion through the per-deployment Checkpoint Communication Gateway: ephemeral checkpoint sessions, checkpoint-scoped credentials, no direct sandbox-to-sandbox route, durable transcript, and hard shutdown of the session/routes when the checkpoint ends. The Orchestrator defines what each checkpoint represents and its expected milestone maturity. Agents signal when their own branch has reached that milestone; runtime mechanically opens and closes reciprocal repository access according to the checkpoint contract.

Implement budget reservations, branch limits, delegation limits, progress checks, and a protected review allowance. Schedule whole Council-member work environments under host capacity rather than centrally scheduling their private internal tasks. When a member reaches a semantic checkpoint, freeze/record its checkpoint state, release its scarce work slot, and prevent it from advancing past the barrier until all required members reach that same checkpoint and the checkpoint review closes. After the barrier opens, do not require all five sandboxes to execute simultaneously: rotate the same logical member sandboxes through available slots, durably queue checkpoint traffic/actions for inactive members, and reschedule a previously-DONE member if a new required action targets it.

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
