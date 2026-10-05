# Part 4A - authority, ownership, communication, and execution boundaries

**Status:** approved design for Part 4A as of October 1, 2026.  
**Scope:** authority boundaries only. This document does not mark Part 4 as complete.  
**Implementation status:** specification only.

## 1. Core principle

Council separates intellectual authority from infrastructure authority.

- The **user** controls project intent and user-granted permissions.
- The **Project Orchestrator** is a stable prompt and clarification layer. It does not supervise the Council.
- **Council members and their workers** control their own reasoning and the contents of their execution environments.
- The **runtime** enforces boundaries, isolation, lifecycle mechanics, and typed state changes without making intellectual decisions.
- The **Auditor** verifies protocol and semantic fidelity without judging which solution is best.
- The shared Council control plane has no intellectual owner.

A concise invariant is:

> Runtime controls boundaries. The Orchestrator preserves prompt consistency. The Auditor verifies protocol. The Council controls the work. The user controls project intent and final acceptance.

## 2. Project Orchestrator

The Project Orchestrator is deliberately narrow.

Its primary responsibilities are:

1. converse with the user before a run sufficiently to produce one canonical project prompt;
2. send the same logical project prompt to every Council member;
3. derive a versioned, project-specific checkpoint plan made of semantic project milestones;
4. retain a small prompt/clarification memory so later explanations remain consistent;
5. receive raw user answers to questions originated by Council agents or workers;
6. transform those raw answers into clear, agent-ready instructions without changing their substance;
7. route the processed answer to the requesting agent and, when the answer changes a project-wide requirement, to every affected branch through the appropriate canonical revision mechanism.

The Orchestrator is not:

- a Council lead;
- a planner for the Council's reasoning;
- a solution designer;
- a winner selector;
- a reviewer of whether an agent's question is intellectually worthwhile;
- a gatekeeper that may suppress a structurally valid user question;
- an owner of Council reasoning, evidence, candidate repositories, or private branch state.

Checkpoint planning is a legitimate Orchestrator responsibility because checkpoints are project-specific semantic milestones. The Orchestrator decomposes the project into review stages from the canonical project prompt, but this does not give it authority over Council reasoning, solution choice, or branch implementation.

### 2.1 Small Orchestrator memory

The Orchestrator retains only the context required to keep prompting and clarification consistent, for example:

- current canonical project prompt and version;
- current project-specific checkpoint plan and milestone sequence;
- user-approved requirements and constraints;
- established terminology;
- prior user clarifications relevant to future interpretation;
- prior Council questions and the processed answers returned;
- references needed to resolve phrases such as "same as before."

The Orchestrator must not become a central investigation memory. It does not ingest ordinary private Council reasoning, candidate code, peer debate, evidence analysis, or unpublished branch work merely to improve its own context.

## 3. Initial Council prompt

Before execution, the Orchestrator produces a versioned canonical project prompt.

Every Council member receives the same logical project requirements. Agent-specific operational metadata may differ, such as member identity, model/provider, execution-environment identifier, or branch identifier, but the project objective and constraints must not silently diverge.

The canonical prompt is versioned and hashable so the system can prove which project instruction a branch received.

## 4. Agent-originated user questions

Any authorized Council member or worker/sub-agent may originate a user question when it believes user input is required.

The normal path is:

```text
Council member or worker
        |
        v
RequestUserInput
        |
        v
durable interaction request
        |
        v
user interface
        |
        v
user
```

The Orchestrator does not decide whether the question is intellectually important enough to reach the user.

The runtime may reject or coalesce a request only for structural reasons such as:

- malformed contract;
- duplicate identical open request;
- explicit rate/loop protection;
- invalid actor;
- security or permission violation.

The runtime must not suppress a question because another model thinks the question is unnecessary.

Only work that actually depends on the answer must block. Unaffected tasks and branches continue where safe.

## 5. User response routing

A raw user reply never flows directly into a Council agent or worker.

The mandatory path is:

```text
User raw response
       |
       v
Project Orchestrator
       |
       v
processed agent-ready response
       |
       v
requesting Council agent or worker
```

The user may experience the UI as replying to the requesting agent, but technically the return path always crosses the Orchestrator.

Both forms are retained:

- **RAW_USER_RESPONSE** - the user's original answer;
- **PROCESSED_USER_RESPONSE** - the Orchestrator's agent-ready rendering.

Council agents normally receive the processed form, not the raw form.

### 5.1 Transformation invariant

> The Orchestrator may improve the form of a user's answer, but not its substance.

It may:

- remove conversational noise;
- resolve obvious pronouns or references from its small memory;
- make an already-clear requirement explicit;
- structure the answer;
- compress repetition;
- render the response in a form that is easier for an LLM to apply;
- identify the scope of the clarification.

It may not:

- invent a requirement or preference;
- strengthen "prefer" into "must";
- weaken "must" into "prefer";
- turn uncertainty into certainty;
- grant a permission the user did not grant;
- add an implementation choice the user did not make.

If material meaning is unresolved, the Orchestrator asks the user again rather than inventing an interpretation.

### 5.2 Response scope

A response does not automatically become visible to every branch.

At minimum, the protocol distinguishes information whose scope is:

- task/local;
- branch;
- project-wide.

A local implementation permission or preference may return only to the requesting branch. A clarification that changes the common project requirements must become a canonical project-level revision and reach every affected branch consistently.

Scope determination is interpretation of what the user addressed, not selection of a preferred Council solution.

## 6. Council members and workers

Council members are peers. There is no permanent intellectual leader above them.

Each Council member controls:

- its reasoning strategy;
- its private branch work;
- its workers/sub-agents;
- its candidate solution;
- its use of the capabilities granted to that branch;
- its execution environment as observed from inside that environment.

Workers operate within the authority delegated by their parent branch and may themselves originate RequestUserInput interactions.

No Council member or worker may directly mutate another branch's unpublished work or bypass checkpoint visibility rules to inspect it.

### 6.1 Repository ownership and checkpoint visibility

Each Council member owns and continuously develops its own repository under its own GitHub identity.

Between checkpoints, peer repositories remain private to their owning branches. At an authorized checkpoint, the runtime temporarily grants reciprocal **read** access among the participating Council members. The repository itself is the primary publication surface; there is no requirement for a separate synthetic publication artifact to stand in for the branch's real committed work.

For each participating branch, checkpoint entry records:
- repository identity;
- repository owner/Council member;
- exact opening commit SHA;
- access-grant time;
- peer recipients.

Peers may inspect, clone, run, and test another member's checkpoint-visible repository inside their own execution environment. They may not push to, rewrite, or otherwise mutate the other member's authoritative repository.

The owner may continue committing to its own repository during the discussion/review window. Those commits remain attributable and the checkpoint records both the opening commit and the final closing commit.

When the checkpoint closes, reciprocal peer access is revoked. Each repository returns to branch-private visibility until the next authorized checkpoint. Agents retain what they legitimately learned during the checkpoint; privacy after closure prevents continued live leakage, not memory of already shared information.

Checkpoint discussion is carried by the per-deployment Checkpoint Communication Gateway. The agent sees only a minimal Council-controlled local message stream/client; it does not receive a raw IRC socket or general-purpose chat protocol surface. The runtime-side bridge, communication session, membership, credentials, and external route remain outside the agent-controlled environment and are ephemeral. There is no direct sandbox-to-sandbox communication route. Important peer actions are structured for tracking while their complete original text remains retained. See [CHECKPOINT_COMMUNICATION_GATEWAY.md](CHECKPOINT_COMMUNICATION_GATEWAY.md).

For proprietary work, "visible" means visible to authorized Council peers. Internet-wide public visibility is not an architectural requirement. Temporary collaborator/read access to otherwise private repositories is the preferred default.

## 7. Transparent execution isolation

Council agents must not need to know that their machine/workspace is implemented as a sandbox.

The agent should experience a normal execution environment and act as though it owns that machine.

> The agent controls everything it can see inside its execution environment. The runtime controls the invisible boundary around that environment.

Inside the environment, the agent may, subject only to resource/capability limits that are part of the environment itself:

- create, rewrite, move, or delete files;
- modify the repository;
- install or remove packages;
- add or replace runtimes;
- configure or destroy local databases;
- start, stop, or replace local services;
- change configuration;
- create local tools;
- restructure the candidate;
- make destructive experiments;
- render the current environment unusable.

Council does not attempt to govern ordinary internal mutations individually.

The agent is not required to behave safely toward the disposable environment itself.

### 7.1 Runtime boundary

The isolation mechanism remains outside agent authority.

An agent may not, merely because it controls its environment:

- escape into the host/control plane;
- access another branch's private environment;
- bypass capability permissions;
- obtain protected provider/Council credentials;
- directly mutate canonical Council records;
- remove or weaken the isolation boundary itself.

The runtime enforces these constraints externally. They should not depend on prompt obedience.

### 7.2 Disposable environment, persistent logical agent

The logical Council member is not identical to a particular environment instance.

If an environment is destroyed or becomes unusable:

1. runtime marks that environment unhealthy;
2. relevant durable logs/state are retained where available;
3. the broken environment may be terminated;
4. a replacement environment is created from the appropriate retained branch/environment state;
5. the same logical Council member continues.

The exact recovery snapshot/rebuild mechanism is a later environment-design detail. The architectural requirement is that loss of one disposable environment must not silently erase the identity or canonical history of the Council member.

## 8. Neutral shared control plane

State outside private branch environments is not intellectually owned by the Orchestrator, an Auditor, or any Council member.

The runtime mechanically maintains canonical shared records such as:

- project/run identity and lifecycle;
- actor identities;
- durable user interactions;
- publications and checkpoint records;
- provenance/events;
- granted permissions and budgets;
- model-call accounting;
- accepted project-level prompt revisions;
- final candidate metadata.

Agents interact with this plane through typed actions rather than unrestricted database CRUD.

Examples include:

- RequestUserInput;
- PublishArtifact;
- SubmitChallenge;
- RecordClaim;
- ProposeCandidate.

The runtime may validate authorization and state invariants. It does not judge the intellectual quality of the content merely because it processes the command.

## 9. Auditor

The Auditor is conceptually separate from the Orchestrator even if an MVP later shares implementation infrastructure.

The Auditor asks whether the protocol was followed faithfully.

Examples include detecting:

- unpublished branch leakage;
- isolation violations;
- semantic drift between RAW_USER_RESPONSE and PROCESSED_USER_RESPONSE;
- unauthorized capabilities;
- invalid publication scope;
- false or inconsistent runtime state.

The Auditor does not:

- choose the best candidate;
- rank Council members;
- design the solution;
- direct investigations;
- suppress minority approaches;
- become a mandatory intellectual approval layer for ordinary Council work.

Normal user clarification therefore remains:

```text
User -> Orchestrator -> requesting agent
```

not:

```text
User -> Orchestrator -> Auditor -> agent
```

The audit policy for high-impact changes may become stricter later, but that is a separate contract and must not silently add the Auditor as a universal bottleneck.

## 10. Part 4A invariants to carry forward

The rest of Part 4 must preserve these rules:

1. Orchestrator prompting is consistent across Council members.
2. Orchestrator memory is intentionally small and is not Council reasoning memory.
3. Council members and workers may originate user questions.
4. Structurally valid questions are not subject to Orchestrator intellectual veto.
5. Raw user replies never flow directly to Council agents/workers.
6. The Orchestrator returns an improved but substantively faithful response.
7. Private branch independence is preserved when a clarification is only local.
8. Project-wide clarifications propagate consistently to all affected branches.
9. Agents control the visible contents of their execution environments.
10. Isolation is transparent and externally enforced by the runtime.
11. A disposable environment may fail without destroying the persistent logical Council member.
12. The shared control plane has no intellectual owner.
13. The runtime enforces mechanics; it does not govern Council reasoning.
14. The Auditor verifies protocol; it does not govern Council reasoning.
15. User intent and final acceptance remain user authority.

## 11. Still unresolved after Part 4A

Part 4A intentionally does not decide:

- the exact typed checkpoint open/review/close contract and repository-access transitions;
- exact sandbox implementation/rebuild technology;
- resource ceilings and how agents request increases;
- the complete Auditor sampling/escalation policy;
- all command/event schemas and error codes.

Those belong to the next Part 4 design passes and must not be filled in by implication.
