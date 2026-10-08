# Council - complete app design

**Design baseline:** approved in the project conversation on September 10, 2026.  
**Repository status:** specification only; application implementation has not started.  
**Authority:** this document preserves the approved complete design. Supporting handoff documents organize its execution and must not silently change its requirements.  
**References:** [upstream design references](REFERENCES.md). References describe source concepts, not verified behavior of this unimplemented application.  
**Part 3 persistence model:** [POSTGRES_DATA_MODEL.md](POSTGRES_DATA_MODEL.md).  
**Part 4 state/action/UI contracts:** [TYPED_INTERACTION_CONTRACTS.md](TYPED_INTERACTION_CONTRACTS.md).  
**Checkpoint communication architecture:** [CHECKPOINT_COMMUNICATION_GATEWAY.md](CHECKPOINT_COMMUNICATION_GATEWAY.md).

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
| Project orchestrator | Produce one stable canonical project prompt, retain small prompt/clarification memory, and transform raw user replies into consistent agent-ready instructions without changing their substance. |
| Council protocol | Independent investigation, checkpoint-scoped publication, cross-examination, revision, coverage review, and synthesis. |
| Worker runtime | Execute assignments, manage delegation, and maintain agent sessions. |
| Model gateway | Route each agent to its selected provider and model. |
| Capability gateway | Enforce access to sources, retrieval, calculations, and other tools. |
| Local privileged broker | Perform narrowly approved elevated host operations for Match My PC and device/VM/container setup without elevating the main Council runtime or exposing raw administrator, Docker-daemon, or kernel control to agents. |
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

### Project Orchestrator and user communication boundary

Before a Council run exists, the Project Orchestrator discusses the project with the user until it can produce one stable, versioned canonical project prompt. Every Council member receives the same logical project requirements; only operational metadata such as member identity, model, branch, or environment may differ.

The Orchestrator is deliberately narrow. It is a prompt and clarification layer with small persistent memory for the current canonical prompt, user-approved constraints, established terminology, and prior clarifications. It must not become a central investigation memory, Council lead, solution designer, winner selector, checkpoint-policy owner by default, or hidden judge.

Any Council member or worker may originate RequestUserInput when it believes user input is needed. The Orchestrator does not decide whether the question is intellectually worthwhile enough to reach the user. The runtime may intervene only for structural reasons such as malformed requests, duplicate open requests, rate/loop protection, invalid actors, or security violations.

The user's raw reply never flows directly to the requesting Council agent or worker. The raw answer is retained, then the Orchestrator transforms it into a clear agent-ready response using its small project memory. It may improve form, resolve obvious references, compress repetition, and make already-clear requirements explicit, but it must not invent, strengthen, weaken, or silently authorize user intent. If material ambiguity remains, it asks the user again.

Processed answers return to the requesting agent or worker. A local clarification need not be exposed to unrelated branches. If the answer changes a project-wide requirement, the change becomes a canonical project-level revision and is delivered consistently to every affected branch.

The authority and routing invariants are specified in [PART_4A_AUTHORITY_BOUNDARIES.md](PART_4A_AUTHORITY_BOUNDARIES.md).

### Independent beginnings

Before seeing their peers' analyses, each member produces an initial investigation plan and preliminary findings.

During this stage, its workers cannot read other branches' unpublished work. Members may access the same authorized source material; the generic architecture does not impose the earlier sensor-based partitioning experiment.

Before execution, the Project Orchestrator derives a versioned, project-specific checkpoint plan from the canonical project prompt. Checkpoints are semantic project milestones, not generic time slices. Their subjects depend on the work itself—for example, a RAG project may review initial retrieval architecture first, reranking next, then fusion, while a web system may review architecture, data/API contracts, backend workflows, frontend integration, and security in a different sequence. Each checkpoint defines its milestone purpose, participating branches, expected maturity/artifacts, peer-review focus, access rules, completion condition, and the next private phase.

Each Council member owns and continuously develops its own repository under its own GitHub identity. Between checkpoints, peer repositories are private to their owning Council member and its branch. At an authorized checkpoint, the runtime temporarily grants the participating Council members read access to one another's repositories. The repository is the primary publication surface: peers inspect the actual committed code, architecture, documentation, experiments, findings, tests, commit history, and other retained branch work rather than receiving a separate synthetic publication object.

Checkpoint entry records the exact repository and opening commit for every participant. Peers may clone and test another member's repository inside their own execution environment, but they never receive write access to another member's authoritative repository. During checkpoint review, the authoritative candidate remains frozen. Verification runs against the frozen snapshot or a disposable copy; implementation commits resume only after checkpoint closure.

When the checkpoint closes, reciprocal peer access is revoked and each repository becomes private to its branch again. Before leaving the checkpoint, each Council member writes a short closeout stating what it intends to carry forward. Runtime then creates a deterministic Checkpoint Return Packet containing the member's closeout, relevant structured actions, test/findings evidence, exact frozen peer snapshot references, unresolved/disputed items, and a reference to the durable full transcript. These are revision inputs rather than instructions; each member independently decides how to change its next private branch. Agents retain frozen peer snapshots they were authorized to inspect, but those snapshots never update after access closes. Peer discussion during the open checkpoint runs through the per-deployment, runtime-controlled Checkpoint Communication Gateway defined in [CHECKPOINT_COMMUNICATION_GATEWAY.md](CHECKPOINT_COMMUNICATION_GATEWAY.md); there is no direct sandbox-to-sandbox communication route. Agents see a minimal Council-controlled message stream, not a raw IRC channel. Important discussion can be promoted to structured peer actions while the complete original text remains preserved and authoritative. The final mature-candidate checkpoint follows the same mechanism but exposes the full candidate repositories for peer inspection, challenge, comparative testing, and revision.

The Project Orchestrator may revise the project-specific checkpoint plan when the project structure materially changes or a new milestone is needed, but it does not judge which Council solution is correct or instruct branches how to solve the milestone. Agents determine their own implementations and signal when their branch has reached the defined checkpoint maturity; the runtime then enforces repository visibility and access transitions. During checkpoint discussion, communication and execution are mutually exclusive per member: an agent may temporarily enter a bounded /work excursion to run a test or verification, during which it cannot communicate live and incoming peer messages/actions are queued for replay when it returns. Other Council members continue discussing normally. /work is verification-only against the frozen checkpoint snapshot or a disposable copy; it cannot change the authoritative candidate or implement fixes. Any implementation happens only after checkpoint closure in private development, preventing a live fix/review loop.

Every checkpoint records the participating repositories, exact opening and closing commits, the period during which reciprocal read access existed, and the discussion/review records produced during that window. This makes it possible to distinguish independently developed work from changes made after peer visibility.

### Collective direction without constant voting

Each member can commission work within its allowance. The council does not vote on every search or document inspection.

The shared agenda combines useful investigations across branches. Administrative decisions about shared resources can use a recorded majority decision, but votes never establish factual support.

A bounded minority-investigation allowance prevents the majority from suppressing every alternative explanation. Deliberate replication is allowed and labeled; a duplicate-task detector should not automatically cancel it.

Only the user can authorize a broader objective, increased spending ceiling, or expanded permissions.

## 3. Investigation lifecycle

### Action-linked state and interaction contract

Lifecycle state, descriptive activity, operation status, and user interaction are separate concepts. A status must never be implemented as a passive label when it implies behavior. Every externally meaningful state/activity has an explicit entry trigger, runtime behavior, observable effect, allowed commands, emitted events, transitions, and failure/recovery path. A user-facing gate additionally defines the exact decision surface and the consequence of every action.

Blocking pop-ups are created from durable interaction requests, not from seeing an activity code such as AWAITING_PROJECT_APPROVAL. This makes decisions resumable across reconnects and prevents replayed events from opening duplicate prompts. Closing a visual prompt without choosing an action does not approve, reject, or otherwise resolve it.

The complete typed command/event taxonomy, scoped activity codes, State Contract schema, Project Contract approval behavior, clarification flow, permission/budget gates, final candidate review, idempotency rules, frontend/SSE behavior, and deterministic acceptance tests are authoritative in [TYPED_INTERACTION_CONTRACTS.md](TYPED_INTERACTION_CONTRACTS.md).

| Stage | Required outcome |
|---|---|
| Define | Project Orchestrator and user agree on and approve a versioned Project Contract; derive the neutral council instruction package, council configuration, permissions, limits, and project-specific checkpoint policy. |
| Investigate independently | Each member develops its initial approach through its own workers while unpublished branch material remains private. |
| Publish | At a planned or approved adaptive checkpoint, freeze and expose only the checkpoint's declared publication scope. |
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

**This is the product's core, not an optional visualization.** The detailed Step 6 contract is defined in [PART_6_EVIDENCE_PROVENANCE_GRAPH.md](PART_6_EVIDENCE_PROVENANCE_GRAPH.md).

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

Agents have separate sessions and workspaces. Executable workloads run in restricted sandboxes with approved inputs, resource limits, and no provider credentials.

For the controlled initial deployment, Docker is the proposed execution boundary. Its security depends on configuration and daemon access, so it must not be represented as absolute isolation against hostile workloads. See [references](REFERENCES.md).

### Council-managed project environments

For executable projects, the default is a **Council-managed project environment**, not host replication.

Each candidate branch receives an isolated execution environment that starts from an approved base and can evolve as the solution requires. Isolation is transparent to the agent: it should experience the environment as a normal machine/workspace that it owns. Everything visible inside that environment is under the branch's operational authority, including destructive changes. The runtime controls only the invisible containment/lifecycle boundary and must prevent escape, cross-branch access, protected credential access, or direct mutation of canonical Council state.

Different branches may choose different stacks and supporting services. Those environment choices are part of the candidate architecture and become reviewable alongside the code.

The user's existing software environment is therefore not a prerequisite for ordinary execution. The host primarily needs to provide the container/runtime capabilities and physical resources required to run the candidate environments.

Environment state must not become an undocumented snowflake. Changes made interactively during development must be captured in reproducible project definitions such as Dockerfiles or image definitions, dependency lock files, Compose/service definitions, migrations, configuration templates, persistent-volume declarations, and an environment manifest.

Before a candidate can be accepted as reproducible, the runtime must be able to destroy its disposable development container, rebuild the project environment from the retained definitions, launch it cleanly, and run the applicable acceptance checks.

The accepted environment is part of the deliverable. The user may retain the built image/container for convenience, but the durable source of truth is the reproducible environment definition plus the project and required persistent data.

Council-only construction machinery does not remain in the delivered runtime. Finalization removes agent processes, provider credentials, agent GitHub credentials, hidden Council control mechanisms, and other orchestration-only tooling unless the Project Contract explicitly requires a related runtime feature.

### Match My PC mode

**Match My PC** is optional and is selected only when the Project Contract requires behavior tied to the user's actual machine. It means reproducing the project-relevant behavior of the host in a controlled environment; it does **not** mean giving council agents unrestricted access to the user's computer.

The Project Orchestrator scopes environment capture from the approved Project Contract. A local profiler collects only relevant capabilities such as operating system/version/architecture, runtime and toolchain versions, selected services, package-manager information, required ports/network assumptions, relevant filesystem locations, GPU/driver/CUDA capability, approved devices, and other explicitly relevant host properties. Personal files, browser state, credentials, unrelated repositories, and unrelated application data are excluded by default.

The profiler produces a sanitized, versioned **Host Profile**. From it, the system proposes an **Environment Contract** describing what will be reproduced, what will be bridged to the real host, what remains unavailable, and what data or devices would be exposed. The user approves this Environment Contract before executable council work begins.

All candidate branches start from the same approved host baseline. Each branch may then add its own candidate-specific overlay. Baseline state and candidate-added state remain distinguishable so the system can answer what came from the user's machine versus what an agent introduced.

Each required capability is recorded as one of:

- **Exact** - the relevant host behavior/version is reproduced.
- **Compatible** - a different implementation or version is expected to satisfy the requirement.
- **Bridged** - the candidate uses an explicitly approved real host resource through a controlled bridge.
- **Unavailable** - the capability cannot currently be reproduced or exposed.

A candidate must not claim verification against the user's environment when a required capability is only compatible or unavailable.

The runtime chooses the least-privileged execution backend that can satisfy the Environment Contract. Ordinary cases use containers; host-specific cases may use GPU/device passthrough, Windows containers, a VM, or narrowly controlled host execution. A custom user-supplied image or environment specification remains a third execution mode alongside Council-managed and Match My PC.

The main Council application remains unprivileged. When Match My PC requires elevated setup or inspection, the app requests elevation only for the **local privileged broker**. On Windows this is an on-demand UAC/admin approval for the broker, not a requirement to run the entire Council application as Administrator.

The broker exposes typed, allowlisted capabilities such as inspecting an approved driver/runtime, configuring a VM, mounting an approved path, attaching an approved device, or launching an approved host-side build. It does not expose a generic administrator shell, unrestricted filesystem access, the raw Docker daemon socket, or kernel control to agents.

Kernel-level access is not part of normal Match My PC operation. If a project genuinely requires kernel development, tracing, or another kernel-level capability, that requirement must be explicit in the Project Contract and separately approved. Prefer an isolated VM or equivalent boundary before real-host kernel access.

**Match My PC does not imply Modify My PC.** Reproducing or bridging host capabilities and mutating the user's real operating environment are separate permissions. Installing software on the host, changing system configuration, enabling services, modifying drivers, or writing outside approved project locations requires an explicit additional authorization.

Any approved host mutation performed through the broker is recorded with before/after state where practical and a cleanup or rollback action when the operation is reversible. Temporary mounts, device bridges, VM resources, and elevated helper state are torn down at the end of the run unless the user explicitly keeps them.

The runtime fingerprints the approved host capabilities relevant to the project. If those capabilities materially change during a run -- for example a driver, runtime, SDK, or service version changes -- the Environment Contract is marked stale for affected work and exact-match claims require revalidation.

The number of logical council agents remains independent from the number of concurrently executing local sandboxes. Resource scheduling controls local parallelism; it does not change council membership or the reasoning protocol.

The number of logical council agents remains independent from the number of concurrently executing local sandboxes. Resource scheduling controls local parallelism; it does not change council membership or the reasoning protocol.

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

Run setup is a conversation between the user and the Project Orchestrator. The orchestrator elicits the objective, background, desired deliverable, exclusions, evidence profile, permitted sources and tools, council composition, resource limits, environment mode, premortem horizon, acceptance criteria, and definition of done.

When enough information is available, the orchestrator produces the proposed Project Contract, neutral council instruction package, and checkpoint policy. The user can correct or refine them before launch.

The council is not created until the user approves the Project Contract. Once approved, the contract, generated instruction package, checkpoint policy, and configuration are versioned.

Each council seat has provider and model dropdowns, supported reasoning controls, and a worker-default selector. Advanced settings are collapsed. Before launch, the user sees a plain-language execution summary: what the agents can access, what they can do, how and when branches can communicate, which execution-environment mode will be used, and what would require further approval.

### Overview

This is the human-readable status page.

It shows what has been established so far, the most important open questions, material disagreements, blocked work, and the next planned investigations.

Metrics include actual completed work, checks, unresolved challenges, context rollovers, and usage. They do not substitute activity volume for quality.

### Council view

Council seats appear as peer cards, each showing its current investigation, model, workers, latest published position, and outstanding challenges.

Selecting a member opens its task history, accessible evidence, received messages, published findings, and session changes.

Controls allow branch pause, worker inspection, and a queued model change. The UI does not provide a direct natural-language guidance channel to an individual council member.

User clarifications or requested scope changes go through the Project Orchestrator. If accepted, they become attributed, versioned Project Contract revisions and are distributed consistently to every affected branch rather than inserted retroactively into earlier history.

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
| Project-lifetime Council state | Isolated PostgreSQL inside each Council deployment sandbox |
| Artifact storage | Versioned local storage behind a replaceable storage interface |
| Long-term accepted-project learning | Git-backed archive/index |
| Optional executable tools | Restricted Docker environments |
| Live updates | Server-sent events, with ordinary API requests for commands |

Use LangGraph as a low-level orchestration runtime combining deterministic steps with agent-driven work, not a predefined single-supervisor architecture. FastAPI supplies the typed API boundary and schema-based validation. Verify current interfaces during implementation. See [references](REFERENCES.md).

No separate vector database, graph database, or distributed orchestration cluster is required initially.

### Main record groups

The exact Part 3 persistence model is defined in [POSTGRES_DATA_MODEL.md](POSTGRES_DATA_MODEL.md). Each active Council deployment owns an isolated PostgreSQL instance inside its trusted deployment sandbox, with logical schemas for canonical project state and runtime operations. This database exists for the lifetime of the active Council project; accepted reusable knowledge is exported to Git rather than preserved as a permanent SQL registry.

At a high level, the canonical model includes:

| Group | Records |
|---|---|
| Project intent | Projects, Project Contracts, immutable contract revisions, approvals, instruction packages |
| Council execution | Runs, seats, branches, logical agents, sessions |
| Checkpoints and visibility | Checkpoint policies/versions, checkpoint instances, publications, publication deliveries, structured escalations |
| Candidates | Candidate solutions, repositories, repository revisions, candidate snapshots, acceptance decisions |
| Environments | Environment definitions, Host Profiles, Environment Contracts, broker grants, host-mutation authorizations, drift events, rebuild verifications |
| Sources and analysis | Sources, source versions, evidence items, assumptions, analysis steps, claims, support groups, challenges, revisions, coverage |
| Continuity | Context manifests, continuation packets, non-authoritative agent-state snapshots |
| Audit and graph | Append-only events, typed graph relationships, projection offsets |
| Runtime | Tasks, leases, operations/attempts, scheduler reservations, sandbox instances, broker requests, model calls, outbox |
| Reuse archive | Git-backed accepted project/repository references, capabilities, stack metadata, lessons, tests, and reuse relationships |

Every relevant record carries project/run scope, attribution, version information, timestamps, and access classification. Branch-private canonical rows are enforced through backend authorization plus PostgreSQL row-level security tied to explicit publication/delivery records rather than prompt convention.

### PostgreSQL graph representation

Use indexed node references and typed relationship records. Use bounded recursive queries with cycle handling for dependency traversal; consult PostgreSQL's current documentation during implementation. See [references](REFERENCES.md).

This is sufficient to test actual graph workloads before adding another database.

The general-purpose graph remains a projection of canonical records, not an unrelated store that can disagree silently with them.

### Consistency

A claim update, its audit event, and its essential relationship changes are committed together.

Expensive indexes and visual projections can update asynchronously, but expose a processed-event position. A context packet must not claim to include a just-published objection while using an older graph view.

Concurrent revisions use expected-version checks. Conflicting edits create a reviewable conflict rather than silently overwriting another member's work. The full atomicity, idempotency, external-operation reconciliation, task-lease, outbox, and projection-consistency contract is defined in [PART_5_TRANSACTIONS_IDEMPOTENCY_CONFLICTS.md](PART_5_TRANSACTIONS_IDEMPOTENCY_CONFLICTS.md).

## 14. Runtime reliability and resource control

The runtime is ordinary software enforcing an agreed process. It does not decide which interpretation is correct.

Use durable runtime operations/queues with leases, heartbeats, retries, cancellation, and deduplication for Council-controlled work such as provisioning and external effects. These runtime queues do not centrally schedule the private internal tasks of a Council member. Each member controls its own work inside its private sandbox. PostgreSQL locking behavior remains the starting mechanism for trusted runtime consumers. See [PART_7_MEMBER_SCHEDULING_RECOVERY_RESOURCES.md](PART_7_MEMBER_SCHEDULING_RECOVERY_RESOURCES.md).

### Host-aware execution scheduling

Local execution capacity is a schedulable resource, not a limit on council membership. The runtime discovers or accepts configured host limits for CPU, memory, disk, GPU/device access, and sandbox concurrency, then applies per-operation reservations and caps.

A low-spec machine may run only one or two Council-member work sandboxes at once while the remaining logical members wait to start/resume. A stronger workstation may execute more member sandboxes concurrently. The investigation protocol and fixed logical Council membership do not change merely because local parallelism changes.

When a member reaches the current semantic checkpoint, it stops private development beyond that barrier and releases scarce private-work execution capacity while other members continue toward the same checkpoint. Releasing that capacity means the runtime quiesces and persists the member sandbox, records its repo/environment/continuation state, and stops the execution container rather than relying on a RAM-holding pause. Later it reconstructs the same logical sandbox from preserved private state and reissues only currently authorized ephemeral credentials/capabilities. Checkpoint review opens only after all required members have reached that barrier. Once open, the same member sandboxes may participate concurrently or be time-sliced through the available sandbox slots. The durable checkpoint gateway queues ordered messages/actions for inactive members; resuming a member delivers accumulated traffic and outstanding obligations. A DONE member targeted by a new required action becomes AVAILABLE again. Checkpoint mode never permits private implementation beyond the frozen snapshot. The scheduler must avoid starvation, throttle or pause new local work under host pressure, and prefer waiting over uncontrolled oversubscription. Remote model calls and local executable slots are accounted for separately because inference may occur on provider infrastructure while builds, tests, tools, and containers consume the user's machine.

The scheduler must not claim capacity or required host capabilities that the machine does not possess. Ordinary Council-managed environments do not attempt to mirror the host. Tasks that explicitly require unavailable host hardware or behavior remain blocked, use an approved alternate backend, or proceed only with a recorded limitation.

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

Retention is phase-specific. During an active project, the isolated Council PostgreSQL database and referenced artifacts persist strongly enough to survive crashes/restarts.

After the user accepts the result, Council first exports/verifies the accepted project and the curated reusable learning package in Git. It then deletes the Council control database, agent/runtime state, checkpoint machinery, temporary peer copies, caches, credentials, and disposable sandbox residue.

The long-term exception is intentional: the accepted project plus useful distilled knowledge about what worked, what failed, important conclusions, tests, reusable components, and reuse relationships may remain in Git for the owner's future Council runs. Raw operational state is not kept merely for historical completeness.

If the accepted product itself legitimately contains a database, that project database is part of the delivered project and is separate from Council's temporary control PostgreSQL.

Backups of an active run include the temporary Council database plus referenced artifacts/configuration needed for crash recovery. Long-term archival after acceptance is Git/project oriented rather than a permanent Council database backup.

## 16. Application interfaces

The backend exposes typed operations for:

- Project orchestration: converse with the user, draft and revise the Project Contract, request approval, generate the neutral council instruction package, create and amend checkpoint policies, receive structured escalations, and publish canonical clarifications.
- Run management: create from an approved Project Contract, validate configuration, start, pause, resume, stop, fork, and finalize.
- Agent management: inspect state, assign work through the runtime, receive structured status/escalation signals, request model changes, and view session history. There is no direct user-to-agent free-form guidance operation.
- Evidence operations: register sources, retrieve permitted passages, publish findings, create challenges, revise claims, and record checks.
- Graph operations: retrieve a bounded neighborhood, trace dependencies, explain revisions, inspect shared origins, and compare snapshots.
- System operations: configure models and connectors, inspect usage, approve scoped actions, and export results.

Natural-language graph questions may be translated into these constrained operations. They must not give an LLM unrestricted database access.

Live updates carry stable event identifiers. Reconnecting clients recover missed events rather than displaying a falsely current dashboard.

## 17. Acceptance tests

Before live-source integrations, the platform must pass a controlled suite using prepared evidence.

| Test | Required behavior |
|---|---|
| Project Contract approval | Do not create/start the council until the user approves a versioned Project Contract. |
| No direct user-agent chat | User clarifications and scope changes pass through the Project Orchestrator and become canonical revisions; individual branches cannot receive informal private guidance from the user. |
| Neutral prompt generation | Generated council instructions state requirements, permissions, acceptance criteria, and communication rules without prescribing an implementation unless the Project Contract requires it. |
| Non-coding investigation | Complete the workflow with no terminal tool. |
| Independent start | No branch reads another branch's unpublished analysis. |
| Scoped checkpoint visibility | At each checkpoint expose only the declared publication scope, record what each branch received, and restore isolation when the policy says to do so. |
| Adaptive checkpoint | Insert an additional scoped checkpoint from structured execution-state signals without requiring unrestricted inspection of private branch repositories. |
| Source dependency | Trace affected conclusions when a source changes. |
| Assumption dependency | Preserve alternative support paths while flagging affected findings. |
| Claim narrowing | Recover the old claim, challenge, evidence, and revision reason. |
| Shared evidence | Identify differently presented documents relying on one original source. |
| Uncertain lineage | Preserve uncertainty rather than force a merge or independence claim. |
| Context rollover | Retain objections, current versions, permissions, and unfinished work. |
| Missing graph edge | Allow recovery through underlying source/history search. |
| Worker interruption | Resume without silently duplicating completed actions. |
| Council-managed environment | By default, create an isolated project environment without attempting to reproduce the user's installed software environment; allow the branch to add authorized runtimes, packages, services, and configuration. |
| Reproducible environment | Capture interactive environment changes declaratively, destroy the development container, rebuild from retained definitions, and pass applicable acceptance checks. |
| Clean delivery boundary | Retain the accepted reproducible project environment while removing Council/agent credentials, processes, and orchestration-only control mechanisms from the delivered runtime. |
| Match My PC scoping | Build the Host Profile only from Project-Contract-relevant capabilities; exclude unrelated user data and secrets by default. |
| Environment Contract approval | Show reproduced, bridged, compatible, and unavailable capabilities and require user approval before Match My PC execution begins. |
| Privilege separation | Elevate only the local privileged broker when required; agents and the main Council runtime never receive unrestricted administrator, Docker-daemon, or kernel access. |
| No implicit host mutation | Match My PC may inspect/reproduce/bridge approved capabilities without changing the real host; host mutations require separate explicit authorization and are auditable. |
| Host drift | Detect material changes to relevant host capabilities and invalidate affected exact-match verification until revalidated. |
| Optional host matching | Never claim exact verification when required host capabilities were only compatible, bridged without equivalent behavior, or unavailable. |
| Resource scheduling | Allow more logical agents than executable sandbox slots; queue and resume local work without starvation or uncontrolled host oversubscription. |
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

The Project Orchestrator generates project-specific communication checkpoints from the approved Project Contract; there is no globally fixed checkpoint count. At minimum, the policy must preserve an independent beginning and provide a mature-candidate peer-review stage before final acceptance. Adaptive checkpoints may be inserted from structured escalation signals.

One mandatory six-month-plus premortem remains required for a fully reviewed run. Investigation and challenge cycles continue within the configured allowance.

These numbers and policies are editable starting defaults, not claims about an optimal configuration.

---

## The defining behavior

A user should be able to open any important conclusion and ask:

> What supports this? What assumptions does it require? What challenged it? Why did it change? Who actually checked it? Are these sources genuinely separate? What still has not been investigated?

The app must answer those questions from retained records and evidence, not generate a plausible retrospective story.

**The complete product is a configurable agent council, a durable investigation process, and a graph that makes its conclusions accountable.**
