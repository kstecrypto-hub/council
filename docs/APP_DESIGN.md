# Council - complete app design

**Design baseline:** approved in the project conversation on September 10, 2026.  
**Repository status:** specification only; application implementation has not started.  
**Authority:** this document preserves the approved complete design. Supporting handoff documents organize its execution and must not silently change its requirements.  
**References:** [upstream design references](REFERENCES.md). References describe source concepts, not verified behavior of this unimplemented application.

The app is a general-purpose investigation platform governed by a council of agents. Each council member develops its own analysis using sub-agents, challenges the others' work, revises its position when justified, and contributes to a shared, evidence-backed result.

DeepSeek powers everything initially. Models remain interchangeable through the UI.

The application's central feature is not the conversation between agents. It is the inspectable relationship between what they did, what they observed, what they concluded, and what subsequently changed.

| Question | Product feature |
|---|---|
| Which conclusions depend on this source or assumption? | Dependency tracing and change-impact analysis. |
| Which challenge caused this claim to be narrowed? | Versioned claims with an explicit revision history and recorded reasons. |
| Which apparently independent findings came from the same evidence? | Source-lineage tracing and shared-evidence detection. |

Everything below supports that operating model.

## Contents

1. [Product structure](#1-product-structure)
2. [Council governance](#2-council-governance)
3. [Investigation lifecycle](#3-investigation-lifecycle)
4. [Worker teams](#4-worker-teams)
5. [The investigation graph](#5-the-investigation-graph)
6. [Evidence and source handling](#6-evidence-and-source-handling)
7. [Context continuity and agentic loops](#7-context-continuity-and-agentic-loops)
8. [Models and provider controls](#8-models-and-provider-controls)
9. [Tools, permissions, and execution environments](#9-tools-permissions-and-execution-environments)
10. [The six-month-plus premortem](#10-the-six-month-plus-premortem)
11. [Complete interface](#11-complete-interface)
12. [Final-report rules](#12-final-report-rules)
13. [Backend and storage design](#13-backend-and-storage-design)
14. [Runtime reliability and resource control](#14-runtime-reliability-and-resource-control)
15. [Security, ownership, and retention](#15-security-ownership-and-retention)
16. [Application interfaces](#16-application-interfaces)
17. [Acceptance tests](#17-acceptance-tests)
18. [Build sequence and initial defaults](#18-build-sequence-and-initial-defaults)

---

## 1. Product structure

The hierarchy is:

**Workspace -> Project -> Investigation run -> Council members -> Worker teams -> Sessions and actions.**

A project groups a subject, permitted sources, and reusable knowledge. A run investigates one defined objective under a recorded configuration.

An agent is a persistent logical investigator. A session is one bounded model conversation belonging to that agent. Restarting a session does not create a new council member or erase its work.

The platform supports research, document analysis, operational investigation, system discovery, and software inspection through the same core process. Available tools and evidence requirements change with the environment.

**Coding is optional. The complete council workflow must work with no terminal or code-execution capability enabled.**

### Core architectural components

| Component | Responsibility |
|---|---|
| Council protocol | Independent investigation, cross-examination, revision, coverage review, and synthesis. |
| Worker runtime | Execute assignments, manage delegation, and maintain agent sessions. |
| Model gateway | Route each agent to its selected provider and model. |
| Capability gateway | Enforce access to sources, retrieval, calculations, and other tools. |
| Investigation ledger | Preserve actions, evidence, claims, assumptions, challenges, and decisions. |
| Graph service | Maintain and query relationships between those records. |
| Context manager | Build bounded working contexts and continue investigations across sessions. |
| Application interface | Configure, monitor, inspect, intervene, and review results. |

These are modules, not eight separately deployed services. Begin with one backend application, separate worker processes, PostgreSQL, and artifact storage.

## 2. Council governance

### Equal investigative authority

Start with three configurable council seats.

Every member has the same responsibilities: investigate the overall question, commission workers, develop an analysis, challenge other analyses, examine objections, and revise conclusions.

There is no permanent planner, skeptic, or judge. There is also no hidden lead agent above the council.

The shared instruction is:

> Develop the strongest supported account of the problem. Search for weaknesses in your analysis and others' analyses. Incorporate valid corrections regardless of their origin. Preserve uncertainty when evidence cannot resolve a disagreement.

Members own investigations, not conclusions they must defend.

### Independent beginnings

Before seeing their peers' analyses, each member produces an initial investigation plan and preliminary findings.

During this stage, its workers cannot read other branches' unpublished work. Members may access the same authorized source material; the generic architecture does not impose the earlier sensor-based partitioning experiment.

At the publication checkpoint, each branch releases its initial findings, assumptions, methods, and gaps. Investigation and communication then continue concurrently.

The checkpoint records which information each branch received. This makes it possible to distinguish independently developed findings from conclusions adopted after discussion.

### Collective direction without constant voting

Each member can commission work within its allowance. The council does not vote on every search or document inspection.

The shared agenda combines useful investigations across branches. Administrative decisions about shared resources can use a recorded majority decision, but votes never establish factual support.

A bounded minority-investigation allowance prevents the majority from suppressing every alternative explanation. Deliberate replication is allowed and labeled; a duplicate-task detector should not automatically cancel it.

Only the user can authorize a broader objective, increased spending ceiling, or expanded permissions.

## 3. Investigation lifecycle

| Stage | Required outcome |
|---|---|
| Define | Record the objective, scope, evidence standard, tools, council configuration, and limits. |
| Investigate independently | Each member develops its initial approach through its own workers. |
| Publish | Freeze and share initial analyses and their supporting records. |
| Cross-examine | Challenge claims, methods, assumptions, and missing investigation areas. |
| Revise | Update claims and commission checks that could resolve disagreements. |
| Review coverage | Identify overlooked areas, interactions, and unsupported generalizations. |
| Synthesize provisionally | Assemble the findings without erasing disagreement. |
| Run the six-month-plus premortem | Examine plausible reasons the provisional result could later prove wrong or incomplete. |
| Finalize | Publish a versioned result with support, limitations, unresolved questions, and review history. |

Cross-examination and revision are iterative, not a fixed number of speeches.

A challenge must reference a particular claim version or investigation decision. It should explain the alleged weakness and, where possible, identify evidence or a test that could resolve it.

Responses are recorded as accepted correction, narrowed claim, evidence-backed rebuttal, or unresolved. Silence is not acceptance. A failed reviewer is not counted as agreement.

### Coverage remains separate from debate

The platform maintains a coverage register: questions considered, methods attempted, assumptions checked, interactions examined, and known gaps.

A long argument about one claim does not count as investigating the rest of the problem.

Coverage percentages are permitted only when the run has an explicit checklist or benchmark. Otherwise, the UI shows concrete counts and gaps, not a fabricated "92% understood."

### Completion does not require unanimity

A run may finish with supported findings, competing interpretations, or an explicitly inconclusive result.

Execution status and finding status remain separate. "Run completed" must never mean "everything it said is proven."

## 4. Worker teams

Workers are created around questions rather than fixed personas.

An assignment might be:

> Determine whether these three sources provide independent evidence for claim C17. Trace their references, inspect the original material, and report unresolved lineage.

Each work item records its objective, parent, permitted evidence and tools, expected deliverable, dependencies, allowance, and stopping condition.

Workers can create narrower subtasks. Children inherit the same permissions or fewer, and their usage counts against the parent branch's allowance. They cannot expand access by spawning another agent.

A worker result contains the answer or current position, evidence references, method, limitations, unsuccessful checks, and remaining questions. "No adequate evidence found" is a legitimate result.

Workers release execution capacity while waiting for dependencies. The runtime must prevent a situation where every available slot is occupied by parents waiting for children.

## 5. The investigation graph

**This is the product's core, not an optional visualization.**

The graph represents the investigation's provenance and argument structure. Reuse relevant W3C PROV concepts for entities, activities, attribution, usage, and derivation without adopting a large ontology or requiring implementation of the entire standard. See [references](REFERENCES.md).

### One canonical record, multiple views

There is one investigation ledger with several projections.

The execution view shows agents, tasks, messages, tool operations, and outcomes.

The evidence view shows sources, assumptions, analyses, claims, challenges, revisions, and dependencies.

A later domain-specific view could represent the system being investigated, but the first version does not need a universal ontology of every possible subject.

### Core node types

| Node | Important contents |
|---|---|
| Agent/session | Logical identity, model, session version, branch, and access scope. |
| Task/action | Objective or operation, inputs, status, timestamps, and outputs. |
| Source version | Original identity, retained version, origin, relevant dates, and access restrictions. |
| Evidence item | Exact passage, observation, or result with its source locator. |
| Assumption | Explicit proposition being relied upon, scope, justification, and review status. |
| Analysis step | Method, inputs, conditions, output, and limitations. |
| Claim version | Statement, scope, supporting material, objections, and status. |
| Challenge | Target version, objection, proposed resolution, and outcome. |
| Revision/decision | What changed, who changed it, and the recorded reason. |

Assumptions must be first-class records. Otherwise, "Which conclusions rely on this assumption?" cannot be answered reliably.

### Mechanical relationships versus interpretations

The runtime automatically records relationships such as assigned to, requested, used, returned, produced, sent, received, and supersedes.

Agents submit interpretive relationships such as supports, challenges, depends on, shares an underlying source with, and narrows.

An interpretive relationship includes its author, justification, evidence references, and review status. It does not become an established fact merely because an agent created an edge.

"Occurred after" is not "caused by." "Cites" is not "proves."

The graph records observable actions and explicit rationales, not every internal reasoning step.

### Preserve combinations of evidence

Suppose a conclusion requires both evidence E1 and assumption A2. Two unrelated arrows would be ambiguous.

An analysis step must explicitly group the required premises and connect that combination to the conclusion. Alternative support paths are recorded separately.

This lets the app distinguish:

> This conclusion loses its only supporting route.

from:

> One supporting route is affected, but another remains.

The system records support structure; it does not automatically perform a formal proof.

### Feature A: dependency and impact tracing

Selecting a source, assumption, or claim exposes "What depends on this?"

The app follows recorded dependencies and returns affected claims, analyses, reports, and open tasks. It distinguishes direct dependencies, indirect dependencies, and mere citations.

When an assumption changes or a source is corrected, dependent findings become needs reassessment. They are not automatically declared false.

The user can also run a labeled hypothetical impact check without modifying the actual evidence.

Results always state that they cover recorded dependencies. Missing graph links remain a possible limitation.

### Feature B: claim evolution

Every substantive claim revision creates a new version.

Selecting "Why did this change?" shows the earlier wording, the relevant challenge, newly considered evidence, the revision decision, and the current wording.

The app should say:

> Revision R17 records challenge H9 as the reason for narrowing C17.

It should not infer that relationship solely because the challenge happened earlier.

### Feature C: shared-evidence tracing

The source model distinguishes a document from the underlying study, dataset, observation, or original report it uses.

Two articles can be different documents while relying on the same evidence.

Known shared origins are linked. Suspected matches remain reviewable suggestions; similar wording or different URLs do not establish either identity or independence.

The UI reports known shared origins, distinct traced origins, and unresolved provenance. It must not produce an unjustified numerical "independence score."

### Graph integrity

Revision chains cannot cycle. Dependency traversal uses cycle detection. Circular support is flagged rather than treated as independent corroboration.

Large outputs stay outside graph labels. Nodes contain concise descriptions and stable references.

No agent can silently delete another agent's challenge, replace a source snapshot, or rewrite recorded execution history.

## 6. Evidence and source handling

The first version accepts manually supplied evidence collections. Live connectors and a RAG service attach to the same interface later.

Every source has a retained identity and version. Where applicable, the record includes its origin, title, publication date, retrieval date, content hash, source locator, and access restrictions.

For a document, evidence might point to a passage and page. For a dataset, it might identify a query, snapshot, rows, units, and transformation. For a tool, it identifies the request and actual returned result.

A failed retrieval is different from an empty retrieval, and neither proves that evidence does not exist.

The ledger separates source statements, observations, computed results, inferences, hypotheses, recommendations, and imagined scenarios. User-provided assertions are attributed rather than silently promoted to verified facts.

### The RAG contract

A RAG service returns evidence packages, not just answers.

Members must be able to request original passages, surrounding context, contradictory material, source references, and retrieval-scope information.

Each council member can search independently. A shared cache may reuse authorized raw source material, but it must not leak another branch's unpublished interpretation.

The RAG agent is not a council leader and cannot decide that its retrieved set is complete.

### Evidence requirements

Each run selects an evidence profile appropriate to the task.

A source-comparison task might require faithful interpretation and reference tracing. A numerical task might require reproducible calculations. A design task might require explicit trade-offs rather than pretend empirical proof.

Profiles define required checks, but no automatic schema validator can certify every methodological judgment.

For an empirical claim, the preferred output is "supported under these conditions," with limitations, not a generic green "proven" badge.

## 7. Context continuity and agentic loops

Retain the established loop ideas: bounded work, observable feedback, external progress records, and fresh sessions. Karpathy's autoresearch is the experimentation-pattern reference; Ralph is the reference for fresh instances continuing through persistent external state. Neither becomes a separate framework inside the app. See [references](REFERENCES.md).

### Inner and outer loops

The inner loop performs a coherent investigation: retrieve, inspect, act, delegate, evaluate, and record.

The outer loop checkpoints work and starts a new session when the current session reaches a safe boundary or approaches its context allowance.

Each logical agent retains its identity, assignments, workers, findings, and unresolved challenges across sessions.

Fresh sessions are continuations, not additional independent reviewers.

### Continuation packet

A new session receives the current objective and constraints, current claim versions, relevant assumptions, unfinished work, unresolved challenges, pending operations, selected evidence, and the next intended action.

It also receives references to additional material it can retrieve.

This packet combines structured state with a short handover. The handover is not the authoritative history.

### Graph-assisted retrieval

The context manager first loads mandatory state: scope, permissions, task position, and outstanding obligations.

It then retrieves a bounded neighborhood around the current task or claim, including relevant objections and revisions. Supporting evidence is added within the remaining allowance.

Ordinary source and history search remain available. The agent must be able to find information that has not yet been connected correctly.

If important material does not fit, the system exposes the omission and splits the work or retrieves it in stages. It must not silently discard a blocking objection.

Each context packet records which source and claim versions were supplied. That makes later inspection possible.

### Checkpoints still matter

The graph does not replace execution state. Use LangGraph's thread-checkpoint and durable-store mechanisms underneath the application's records; verify current interfaces when implementation begins. See [references](REFERENCES.md).

Tool outputs and task transitions are persisted continuously. A crash before the final handover therefore leaves recoverable state.

Rollover happens before the context is exhausted, with space reserved for responses and tool results. Uncertain pending actions are reconciled before the new session can repeat them.

## 8. Models and provider controls

Model selection is an agent property, not a global architectural assumption.

Configuration inheritance is:

**Workspace default -> run default -> council-seat override -> worker default -> individual worker override.**

All initially resolve to the chosen DeepSeek model.

The UI shows where a setting is inherited and offers an explicit override. It also labels an all-DeepSeek council as same-model rather than implying training diversity.

### Provider registry

Each model entry records its provider, identifier, available capabilities, supported settings, context allowance, credential reference, configured pricing, and last compatibility check.

DeepSeek's model-list endpoint is a discovery source for identifiers, not the sole authority for all capability and pricing details needed by the app. Those belong in the registry and compatibility tests. See [references](REFERENCES.md).

Provider adapters normalize requests and results while preserving required provider-specific state. DeepSeek's documented thinking-mode tool-continuation handling stays inside its adapter; check the current API contract during implementation.

Provider continuation data is not automatically published to the council or displayed as an explanation of its conclusions.

### Changing a model mid-run

A model change is queued for a safe checkpoint. The new session receives an evidence-based handover, not incompatible provider-specific conversation state.

Earlier work retains its original attribution. Model settings, dates, and returned identifiers are recorded.

Switching providers also rechecks data-sharing permission. Automatic fallback to another provider is opt-in, never silent.

A model lacking a required capability cannot quietly take an assignment that depends on it.

## 9. Tools, permissions, and execution environments

Agents interact through typed capabilities such as searching evidence, reading sources, publishing findings, sending challenges, commissioning workers, tracing dependencies, and requesting calculations.

The gateway checks authorization on every request. A prompt alone does not enforce access.

Each tool has an input schema, result schema, permissions, timeout, execution classification, and expected provenance output.

Read-only investigation is the default.

External writes or consequential actions require explicitly granted authority. Approvals are bound to the particular action and parameters rather than giving an agent unlimited permission afterward.

Agents have separate sessions and branch workspaces. When an investigation concerns a mutable external target, investigative branches must not mutate the canonical environment directly. Each branch works from a recorded baseline and may change only its own isolated branch environment until an implementation is explicitly selected and promoted.

A branch environment is not a byte-for-byte clone of the user's machine. Before branching, environment discovery produces an **execution-relevant environment specification**: the smallest practical set of known conditions capable of materially changing the behavior under investigation. Relevant conditions can include OS/build/architecture, runtimes and libraries, services, filesystem and permission behavior, network/firewall/proxy/VPN rules, identity and certificate configuration, security software, kernel drivers, hardware/driver dependencies, data schema/scale/latency/concurrency characteristics, external integrations, and project configuration. Irrelevant installed software is excluded.

Every relevant condition is recorded as reproduced, simulated, omitted-as-irrelevant, unreproducible, or unknown. Unreproduced or uncertain conditions remain attached to candidate results as environment-fidelity limitations. If later discovery shows that an omitted condition could materially affect behavior, affected candidates must be revalidated.

Docker is one possible execution mechanism, not the environment abstraction. Containers are appropriate when they can reproduce the required behavior and constraints. VM, native-host, hardware-backed, or other isolated execution may be required for OS-, kernel-, driver-, device-, or security-product-sensitive behavior. Restricted Docker execution remains useful for generated code and calculations, but it must not be represented as a universal reproduction of the canonical environment. See [references](REFERENCES.md).

Large production systems do not require naive full duplication. A branch may use copy-on-write snapshots, overlays, isolated replicas, representative/anonymized datasets, simulated integrations, or read-only shared baselines when those preserve the behavior relevant to the investigation. All council branches must derive from the same recorded baseline specification so their candidate implementations remain comparable.

Promotion is distinct from investigation. An agent may have broad authority inside its own branch environment while having no authority to write the canonical target. After the council selects a candidate revision, promotion validates the candidate against the current canonical version, required permissions, environment-fidelity assumptions, and operational checks before any real change occurs.

Credentials stay in backend-managed secret storage. Raw keys do not reach browser state, generated scripts, source documents, or ordinary logs.

Retrieved material is treated as evidence, not executable authority. A document cannot grant tools, change the objective, or override access rules.

## 10. The six-month-plus premortem

The app freezes a provisional report version and sends it for independent future-failure review.

Each council member, using fresh workers where helpful, considers:

> At least six months have passed, and a careful independent investigation has shown that our conclusions were materially wrong or incomplete. What plausible mechanisms explain this?

Every scenario identifies the affected claims, assumptions, plausible failure mechanism, checks possible now, and observations that would require later evidence.

The review distinguishes an original analytical flaw from a conclusion that was valid but later became inapplicable.

A substantive objection reopens affected work. An untestable concern remains an explicit limitation or reassessment trigger.

These are hypothetical scenarios, never fabricated future facts. The feature runs now; it is not an automatic promise to perform another investigation six months later.

## 11. Complete interface

### Application shell

Use a desktop-first interface with a restrained dark theme, optional light theme, and resizable working panels.

Global navigation contains Projects, Runs, Sources, Models, and Settings.

Inside a run, the main views are Overview, Council, Work, Evidence Graph, Review, Report, and Activity.

The header permanently shows the objective, execution status, current phase, allowance remaining, and pause/stop controls.

The central workspace is not an endless chat feed.

### Run setup

The setup screen captures the objective, background, desired deliverable, exclusions, evidence profile, permitted sources and tools, council composition, resource limits, and premortem horizon.

Each council seat has provider and model dropdowns, supported reasoning controls, and a worker-default selector.

Advanced settings are collapsed. Before launch, the user sees a plain-language execution summary: what the agents can access, what they can do, and what would require further approval.

Configuration is versioned once execution begins.

### Overview

This is the human-readable status page.

It shows what has been established so far, the most important open questions, material disagreements, blocked work, and the next planned investigations.

Metrics include actual completed work, checks, unresolved challenges, context rollovers, and usage. They do not substitute activity volume for quality.

### Council view

Council seats appear as peer cards, each showing its current investigation, model, workers, latest published position, and outstanding challenges.

Selecting a member opens its task history, accessible evidence, received messages, published findings, and session changes.

Controls allow scoped guidance, branch pause, worker inspection, and a queued model change.

User guidance becomes an attributed instruction with a timestamp and scope. It is not inserted retroactively into earlier history.

### Work view

Tasks appear in both a dependency view and a searchable table.

Statuses distinguish queued, running, awaiting a dependency, awaiting approval, blocked, completed, failed, and cancelled.

The user can identify deliberate replication, unfinished branches, repeated failures, and work waiting on another agent.

### Evidence graph

The graph opens around the selected question or claim, not every recorded event.

Its primary controls are:

**Trace dependencies. Explain this revision. Find shared evidence. Show objections. Show assumptions. Compare versions.**

Selecting a node opens a detail inspector with the exact record, supporting material, author, status, related actions, and version history.

Selecting an edge shows its type, origin, justification, and review status.

A historical view shows the recorded investigation at a chosen point. It does not imply that rerunning the models would reproduce the same responses.

The graph supports bounded expansion, filters, saved views, and visible truncation notices. No silent "load everything."

React Flow is the proposed interactive graph library. Rendering and traversal limits remain application responsibilities. See [references](REFERENCES.md).

Every graph operation also has a table or list equivalent. Keyboard users should not need to manipulate a canvas to inspect evidence.

### Source viewer

Evidence opens beside the original passage, page, or result.

The viewer distinguishes exact source material from an agent's summary. It shows source version, retrieval scope, extraction limitations, and known shared origins.

An unavailable source is labeled unavailable; it is not replaced with a convincing paraphrase.

### Review view

This groups material challenges, unresolved assumptions, coverage gaps, claims requiring reassessment, and premortem scenarios.

A reviewer can move directly from an objection to the disputed claim version and its evidence.

### Report view

The report separates supported conclusions, conditional conclusions, recommendations, unresolved alternatives, and insufficiently supported claims.

Every significant finding links back to the graph and evidence.

Exports should include a readable report and a structured audit bundle. Exports respect source permissions and disclose unavailable artifacts.

### Activity and system settings

Activity contains the complete retained record of instrumented actions, with filtering by agent, task, source, operation, and outcome.

Settings manage provider credentials, model compatibility, connectors, permissions, resource limits, retention, and backups.

The UI exposes concise rationales and recorded actions, not a promise to reveal every internal reasoning step.

## 12. Final-report rules

A drafting agent can assemble the report, but it has editorial, not adjudicative, authority.

It cannot silently select a winning member, introduce unsupported findings, erase objections, or broaden a claim beyond its reviewed conditions.

Report statements reference specific claim versions. Material changes to those claims trigger review of the affected report sections.

Finalization records each council member's review disposition. A minority objection can survive into the final report.

The final snapshot includes the objective, source scope, findings, limitations, unresolved questions, coverage gaps, premortem outcome, methods, and model configuration.

Later evidence creates a new revision or follow-up run. It does not rewrite what the earlier run concluded.

## 13. Backend and storage design

### Recommended foundation

| Layer | Proposed choice |
|---|---|
| Interface | React and TypeScript |
| Interactive graph | React Flow |
| Backend | Python and FastAPI |
| Structured contracts | Pydantic |
| Stateful agent execution | LangGraph |
| Persistent application data | PostgreSQL |
| Artifact storage | Versioned local storage behind a replaceable storage interface |
| Optional executable tools | Restricted Docker environments |
| Live updates | Server-sent events, with ordinary API requests for commands |

Use LangGraph as a low-level orchestration runtime combining deterministic steps with agent-driven work, not a predefined single-supervisor architecture. FastAPI supplies the typed API boundary and schema-based validation. Verify current interfaces during implementation. See [references](REFERENCES.md).

No separate vector database, graph database, or distributed orchestration cluster is required initially.

### Main record groups

| Group | Records |
|---|---|
| Organization | Workspaces, projects, users, memberships, access grants |
| Configuration | Run versions, provider profiles, model profiles, evidence policies |
| Execution | Agents, sessions, tasks, task dependencies, operations, usage |
| Communication | Messages, publications, deliveries, review assignments |
| Sources | Sources, source versions, evidence items, artifacts, origin relationships |
| Analysis | Claims, claim versions, assumptions, analysis steps, support groups |
| Review | Challenges, responses, revisions, coverage items, premortem scenarios |
| Continuity | Checkpoints, continuation packets, context manifests |
| Audit | Events, graph relationships, projection progress, report snapshots |

Every relevant record carries project/run scope, attribution, version information, timestamps, and access classification.

### PostgreSQL graph representation

Use indexed node references and typed relationship records. Use bounded recursive queries with cycle handling for dependency traversal; consult PostgreSQL's current documentation during implementation. See [references](REFERENCES.md).

This is sufficient to test actual graph workloads before adding another database.

The general-purpose graph remains a projection of canonical records, not an unrelated store that can disagree silently with them.

### Consistency

A claim update, its audit event, and its essential relationship changes are committed together.

Expensive indexes and visual projections can update asynchronously, but expose a processed-event position. A context packet must not claim to include a just-published objection while using an older graph view.

Concurrent revisions use expected-version checks. Conflicting edits create a reviewable conflict rather than silently overwriting another member's work.

## 14. Runtime reliability and resource control

The runtime is ordinary software enforcing an agreed process. It does not decide which interpretation is correct.

Use a durable task queue with leases, heartbeats, retries, cancellation, and deduplication. PostgreSQL locking behavior is the starting mechanism for multiple consumers of a queue-like table; lease and recovery rules require explicit application implementation. See [references](REFERENCES.md).

Every operation distinguishes requested, started, completed, failed, cancelled, and outcome unknown.

After interruption, completed work is reused. An operation with an uncertain external outcome is reconciled before replay. Do not promise exactly-once behavior from an external service that does not provide it.

Pause prevents new scheduling and lets the runtime reach a safe state. Stop cancels controllable work but cannot undo an already completed external action.

### Budget controls

The run allowance is divided into member allowances and a protected review reserve.

Limits apply to concurrent model calls, worker creation, delegation depth, tool execution, and cumulative usage. Retries and failed attempts count.

The scheduler reserves allowance before concurrent calls, then reconciles actual usage. Missing prices are marked unknown rather than treated as free.

Repetitive work without new evidence, tests, revisions, or coverage triggers a progress review. Budget exhaustion produces a partial result, not forced agreement.

These are bounds on autonomy, not instructions to ask the user for permission at every step.

## 15. Security, ownership, and retention

The initial deployment can be single-owner, while records carry workspace and project boundaries from the beginning.

A later shared deployment can expose owner, operator, reviewer, and viewer roles. Backend enforcement applies to sources, artifacts, graph queries, search results, exports, and model requests, not only visible UI buttons.

Private-stage publications cannot leak through search previews, graph neighborhoods, or shared context retrieval.

Provider changes respect source-specific data-sharing restrictions. Connection credentials are never inherited by sub-agents.

Retention is explicit. Important findings and their cited evidence can be retained longer than verbose operational logs. Deletion or redaction leaves an appropriate audit marker, and the app warns when an export or old result can no longer be fully reproduced.

Backups include the database, referenced artifacts, configuration versions, and restoration checks. A graph without its evidence files is not an adequate backup.

## 16. Application interfaces

The backend exposes typed operations for:

- Run management: create, validate configuration, start, pause, resume, stop, fork, and finalize.
- Agent management: inspect state, assign work, send scoped guidance, request model changes, and view session history.
- Evidence operations: register sources, retrieve permitted passages, publish findings, create challenges, revise claims, and record checks.
- Graph operations: retrieve a bounded neighborhood, trace dependencies, explain revisions, inspect shared origins, and compare snapshots.
- System operations: configure models and connectors, inspect usage, approve scoped actions, and export results.

Natural-language graph questions may be translated into these constrained operations. They must not give an LLM unrestricted database access.

Live updates carry stable event identifiers. Reconnecting clients recover missed events rather than displaying a falsely current dashboard.

## 17. Acceptance tests

Before live-source integrations, the platform must pass a controlled suite using prepared evidence.

| Test | Required behavior |
|---|---|
| Non-coding investigation | Complete the workflow with no terminal tool. |
| Independent start | No branch reads another branch's unpublished analysis. |
| Source dependency | Trace affected conclusions when a source changes. |
| Assumption dependency | Preserve alternative support paths while flagging affected findings. |
| Claim narrowing | Recover the old claim, challenge, evidence, and revision reason. |
| Shared evidence | Identify differently presented documents relying on one original source. |
| Uncertain lineage | Preserve uncertainty rather than force a merge or independence claim. |
| Context rollover | Retain objections, current versions, permissions, and unfinished work. |
| Missing graph edge | Allow recovery through underlying source/history search. |
| Worker interruption | Resume without silently duplicating completed actions. |
| Model change | Preserve attribution and recheck provider permissions. |
| Hostile source content | Prevent source text from granting authority or changing instructions. |
| Premortem | Keep imagined failures separate from observed evidence. |
| Budget exhaustion | Produce an honest partial result with remaining gaps. |
| Inconclusive evidence | Finalize uncertainty instead of manufacturing consensus. |

Runtime invariants receive deterministic tests. Model-dependent behavior receives repeated evaluation rather than being judged from one successful run.

These tests establish whether the application behaves as specified. They do not establish that a council is universally better than one strong agent.

Graph-assisted continuation must also be compared with searchable records and summaries containing the same underlying information. Otherwise, the graph's own contribution remains unknown.

## 18. Build sequence and initial defaults

### Build sequence

Foundation: canonical records, source snapshots, permissions, task execution, provider adapters, and graph operations using prepared fixtures.

Working council: independent starts, worker delegation, publication, challenges, revisions, and resource controls.

Continuity and review: context rollover, graph-assisted retrieval, coverage inspection, premortem, and final reporting.

Product interface and hardening: complete graph inspection, model switching, recovery testing, exports, and backups.

Live-source and RAG integrations follow through the already-defined capability and evidence interfaces.

This ordering avoids creating an impressive dashboard before the underlying records are trustworthy.

### Initial configuration

Start with three council members, all using the selected DeepSeek model, and a shared limit of four concurrent model calls.

Workers are created dynamically, with two worker-delegation levels beneath each council member as an initial cap. Read-only evidence tools are enabled; executable tools are opt-in.

One independent publication checkpoint and one mandatory six-month-plus premortem are required for a fully reviewed run. Investigation and challenge cycles continue within the configured allowance.

These numbers are editable starting defaults, not claims about an optimal configuration.

---

## The defining behavior

A user should be able to open any important conclusion and ask:

> What supports this? What assumptions does it require? What challenged it? Why did it change? Who actually checked it? Are these sources genuinely separate? What still has not been investigated?

The app must answer those questions from retained records and evidence, not generate a plausible retrospective story.

**The complete product is a configurable agent council, a durable investigation process, and a graph that makes its conclusions accountable.**
