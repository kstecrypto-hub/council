# Part 3 of 15 — Minimal Durable Schema and Repository-Based Agent Work

**Status:** active Part 3 design; not yet approved.  
**Branch:** `design/code-level-implementation`.  
**Authority:** this document replaces the earlier over-specified Part 3 schema draft. Parts 1-2 remain authoritative.

## 1. Core decision

Council's database is **not** a model of how agents build things.

Each council member receives:

1. an isolated execution environment/sandbox;
2. its own repository for the run;
3. the tools/capabilities granted to that member.

The agent is free to organize its work inside that environment however it decides.

Council constrains the boundary around the sandbox through code and infrastructure, not through prompt text or a relational schema describing the agent's internal workflow.

The central database stores only durable Council configuration and the minimum control metadata required to recover and operate a run.

## 2. Per-member GitHub accounts and repositories

Each independent Council member has:

1. its own pre-authenticated GitHub account;
2. its own repository for the current user project;
3. its own isolated sandbox/environment.

There is no requirement for a separate central live project repository during the Council run.

Conceptually:

```text
optional starting project state
          |
     copied into each
       member repo
      /     |     \
     v      v      v
 GitHub A GitHub B GitHub C
   repo A   repo B   repo C
     |       |       |
 sandbox A sandbox B sandbox C
```

If the user already has a project, that project is used only as the starting state copied into each member repository.

If the Solution Registry finds a previous project that is similar or identical, that earlier repository may be used:

- as the starting base copied into each member repository;
- as a reference the agents may inspect;
- or almost unchanged, with only the small changes required for the new project.

A previous project's live repository is never reused in place for a new user project. The new Council run still creates new member repositories so ownership, experimentation, archive, and cleanup remain isolated.

The agent decides how to organize its own repository and sandbox. Council does not impose an internal Git strategy, commit cadence, local versioning scheme, file layout, database layout, build system, test structure, or implementation process.

Council stores only the repository/account references needed to operate the run; it does not mirror repository contents/history into PostgreSQL.

## 3. Independence and repository visibility

The approved independent-start requirement still applies.

During the independent phase:

- each member can read its own repository;
- workers inherit their parent member's repository/environment;
- another member cannot read that repository's unpublished work.

At the publication/cross-examination boundary, repository visibility may be opened to the other council members.

After that point, peers may inspect the published/live repository state as allowed by the Council protocol.

This gives us both:

1. genuine independent initial investigation; and
2. repository-based collaboration once discussion begins.

If the product design later intentionally removes the independent-start phase, that is a Council-protocol change, not a database change.

## 4. Sandbox enforcement is structural

Security and isolation cannot depend on instructions such as "do not access production."

The sandbox/environment builder enforces the actual boundary.

Depending on the selected environment mechanism, enforcement can include:

- isolated filesystem/mounts;
- separate repository credentials scoped to the member repository;
- network namespace/rules;
- production-network denial;
- explicit allowlisted external services;
- secret injection without exposing secret-store credentials;
- CPU/RAM/disk/process limits;
- VM/container/native-host isolation as required by fidelity;
- no Docker/socket/host-control access unless intentionally granted;
- canonical environment mounted/readable only when required and writable only through the promotion path;
- device/driver/hardware constraints where relevant;
- cleanup/destruction behavior.

Prompts may describe the rules to the model for usability, but the prompt is not the security mechanism.

## 5. What the database is for

The main Council database has two responsibilities.

### 5.1 Persistent Council configuration

Configuration that is reused across runs:

- agent prompt/template definitions;
- model configuration;
- MCP server definitions;
- tool/capability configuration;
- secret references;
- Council/run presets where useful.

### 5.2 Minimal durable run manifest

A small amount of runtime state is required so an orchestrator crash/restart does not make an active run unknowable.

The manifest records only boundary/control information such as:

- run identity and objective;
- common baseline reference/fingerprint;
- which logical members belong to the run;
- each member's prompt/model/tool configuration;
- each member's GitHub account reference and repository reference;
- each member's sandbox/environment instance reference;
- current high-level lifecycle state;
- repository visibility/publication phase;
- selected output/repository when one is chosen;
- user acceptance/cleanup state.

The manifest does **not** describe how the agent engineered the solution inside its sandbox.

## 6. Proposed minimal Council database

### 6.1 `agent_prompts`

Stores reusable prompts/instructions.

| Column | Purpose |
|---|---|
| `id` | primary key |
| `name` | human-readable identity |
| `prompt_text` or `artifact_ref` | exact prompt |
| `content_hash` | reproducibility |
| `created_at` | audit |
| `status` | active/retired |

A run records the exact prompt id/hash it actually used.

Different agents may reference the same prompt.

Agent A and Agent B are not versions of each other.

### 6.2 `model_configs`

| Column | Purpose |
|---|---|
| `id` | primary key |
| `provider` | provider identifier |
| `model` | model identifier |
| `settings_json` | non-secret model settings |
| `secret_ref` | backend secret-store reference |
| `created_at` | audit |
| `status` | active/retired |

### 6.3 `mcp_servers`

| Column | Purpose |
|---|---|
| `id` | primary key |
| `name` | server identity |
| `transport` | stdio/http/etc. as supported |
| `endpoint_config_json` | non-secret connection config |
| `secret_ref` | optional secret-store reference |
| `status` | active/disabled |
| `created_at` | audit |

MCP is a capability transport. It is not the database.

### 6.4 `tool_configs`

Council may expose native tools, MCP-backed tools, APIs, database connectors, or environment capabilities through a common tool gateway.

| Column | Purpose |
|---|---|
| `id` | primary key |
| `name` | stable Council-visible tool name |
| `backend_kind` | mcp/native/http/database/environment/etc. |
| `mcp_server_id` | nullable FK when MCP-backed |
| `tool_key` | remote/native tool identifier |
| `policy_json` | non-secret capability/scoping config |
| `status` | active/disabled |

Exact input/output schemas may be discovered from the backend or cached where useful; Part 3 does not require duplicating every remote schema in relational tables.

### 6.5 `council_presets` (optional)

Reusable combinations of:

- number of council members;
- prompt ids;
- default model configs;
- tool sets;
- budget/resource preset.

This is convenience configuration, not a requirement for agent independence.

### 6.6 `runs`

| Column | Purpose |
|---|---|
| `id` | primary key |
| `objective` | user's requested outcome |
| `baseline_ref` | common input/environment baseline |
| `baseline_hash` | immutable fingerprint |
| `phase` | setup/independent/discussion/selection/awaiting_acceptance/closed |
| `status` | active/paused/completed/failed |
| `selected_member_id` | nullable |
| `created_at` | creation |
| `accepted_at` | nullable user acceptance |
| `closed_at` | nullable cleanup completion |

### 6.7 `run_members`

One row per logical council member.

| Column | Purpose |
|---|---|
| `id` | primary key |
| `run_id` | FK |
| `member_key` | A/B/C/etc. |
| `agent_prompt_id` | exact prompt used |
| `model_config_id` | exact model config used |
| `github_account_ref` | non-secret reference to member's pre-authenticated GitHub identity |
| `repo_ref` | repository owned by this Council member's GitHub account |
| `sandbox_ref` | current opaque environment instance reference |
| `status` | provisioning/active/waiting/finished/failed/destroyed |
| `created_at` | audit |
| `destroyed_at` | nullable |

Workers do not need separate independent repositories unless an agent itself chooses to create them inside its environment. Council only needs to know workers separately if runtime/budget orchestration later requires it.

### 6.8 `run_member_tools`

Maps a member to the Council tool configurations/capabilities it is allowed to access.

This is authorization metadata, not a description of how the agent uses those tools.

### 6.9 `repo_visibility`

Records the cross-agent visibility state of a member repository when the Council protocol requires an independent phase.

Possible state:

```text
OWNER_ONLY
COUNCIL_READ
SELECTED_FOR_PROMOTION
CLOSED
```

The actual permission is enforced by repository credentials/access control, not by trusting this row alone.

### 6.10 `run_outputs`

Council treats an agent's published result as an opaque output.

| Column | Purpose |
|---|---|
| `id` | primary key |
| `run_id` | FK |
| `run_member_id` | producer |
| `repo_ref` | repository containing the output |
| `commit_ref` | exact published state if Git-backed |
| `artifact_ref` | optional non-repo output |
| `summary` | bounded human/agent summary |
| `supersedes_output_id` | nullable prior published output from same member |
| `published_at` | timestamp |

A, B, C outputs are siblings, not versions.

If B publishes a later state, B2 may simply supersede B1.

Council does not model B's internal commits as database entities.

### 6.11 `run_selection`

Records which published output/repository was selected for promotion and by whom/what Council decision process.

### 6.12 `run_cleanup`

Small durable cleanup state so environment/repository destruction can be retried safely after user acceptance.

## 7. What is explicitly not in the central database

Unless a later Council-level feature proves it is required, the central DB does not need tables for:

- agent-local claims;
- assumptions;
- analysis steps;
- internal candidate revisions;
- local Git commits;
- internal test cases;
- intermediate files;
- agent-local task breakdown;
- scratch notes;
- private graph structure;
- implementation dependencies discovered only inside one sandbox;
- internal database schemas created by an agent;
- per-file change history.

Those belong to the agent's own repository/sandbox or to an artifact it explicitly publishes.

## 8. Repositories versus database responsibilities

```text
DATABASE
-------
Who is running?
Which prompt/model/tools?
Which repo belongs to whom?
Which sandbox belongs to whom?
What baseline did they start from?
Who may read which repo?
Which published output was selected?
Has the user accepted the work?
Can cleanup/promotion safely proceed?

REPOSITORY / SANDBOX
--------------------
How did the agent solve the problem?
What files did it create?
What architecture did it choose?
How did it organize versions/commits?
What tests did it invent?
What local services/DBs did it create?
What experiments did it run?
```

## 9. Solution Registry remains separate

The previously agreed Solution Registry is still useful, but it should remain much smaller than the old Part 3 draft implied.

Its purpose is to answer:

> Have we already built something close enough to reuse?

A minimal registry can store:

### `solutions`

- id;
- name;
- summary;
- solution kind/category;
- current/recommended repo ref;
- reuse/access scope;
- status.

### `solution_releases`

Only when the same reusable product has materially changed over time and we actually need to distinguish releases:

- solution id;
- release identifier;
- repo ref + commit/tag;
- environment requirements;
- validation summary/artifact refs;
- created_at.

No universal "version" system is required.

### `solution_capabilities`

Searchable capability tags/descriptions.

### `solution_environment_requirements`

Only the environment constraints needed to decide whether reuse is compatible.

### `solution_components` (optional)

Reusable component references when component-level reuse proves useful in practice.

The registry points to repositories/artifacts; it does not duplicate them into PostgreSQL.

## 10. Reuse flow

Before creating the member repositories:

```text
user request
   |
   v
search Solution Registry
   |
   +--> direct match -> use existing product/repo, modify only if needed
   |
   +--> partial match -> use existing repo/components as common baseline
   |
   +--> no useful match -> create fresh common baseline
```

Each council member receives the same chosen starting state copied into that member's own repository.

## 11. Outstanding Part 3 questions

Part 3 is still active.

The next design questions are:

1. exact repository lifecycle: creation, initial visibility, peer-read opening, retention, deletion/archive;
2. whether the minimal run manifest lives entirely in PostgreSQL or partly in durable orchestrator files;
3. exact prompt/MCP/tool configuration schema and secret-reference handling;
4. sandbox lifecycle records needed for crash recovery without modeling internals;
5. Solution Registry minimum searchable fields and reuse decision flow;
6. retention of unselected member repositories after user acceptance;
7. whether cross-agent discussion itself needs a dedicated durable message channel or can be repo/publication based;
8. what minimal audit trail is required for promotion/canonical writes;
9. indexing/migration strategy after the minimal schema is agreed.

Part 3 is not approved until these are reviewed explicitly.
