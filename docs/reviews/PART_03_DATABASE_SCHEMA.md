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

The central Council database has two responsibilities only:

1. persistent Council configuration reused across runs;
2. the minimal active-run manifest needed for recovery and orchestration.

It does not model how agents build inside their sandboxes.

### 5.1 Persistent Council configuration

Persist centrally:

- Council member GitHub account identities;
- prompts;
- provider credential references;
- model configurations;
- MCP server definitions;
- Council-visible tools;
- reusable tool/capability sets;
- secret bindings/references.

### 5.2 Minimal active-run manifest

The active-run manifest will be reviewed separately in this Part. Its purpose is only to let the orchestrator recover which run exists, which member owns which repo/sandbox, what phase it is in, and what cleanup/promotion work remains.

## 6. Persistent configuration schema

### 6.1 `agent_accounts`

Represents the persistent Council-member identities used to provision sandboxes and repositories.

| Column | Purpose |
|---|---|
| `id` | primary key |
| `name` | Council member identity/label |
| `github_username` | GitHub account used by this member |
| `github_auth_secret_ref` | reference to GitHub credential/session material in secret storage |
| `status` | active/disabled |
| `created_at` | audit |

The actual GitHub credential is never stored directly in PostgreSQL.

### 6.2 `prompts`

Stores exact reusable prompt definitions.

| Column | Purpose |
|---|---|
| `id` | primary key |
| `name` | human-readable identity |
| `purpose` | intended use |
| `prompt_text` or `artifact_ref` | exact prompt |
| `content_hash` | reproducibility |
| `status` | active/retired |
| `created_at` | audit |

There is no generic prompt-version hierarchy.

A materially changed prompt is a new immutable prompt row. Historical runs keep pointing to the exact prompt row/hash they used.

Multiple agents may reference the same prompt.

### 6.3 `provider_credentials`

Operational credential bindings are separate from model definitions.

| Column | Purpose |
|---|---|
| `id` | primary key |
| `provider` | provider identity |
| `secret_ref` | external secret-store reference |
| `status` | active/disabled |
| `created_at` | audit |

Rotating an API key does not create a new model configuration.

### 6.4 `model_configs`

| Column | Purpose |
|---|---|
| `id` | primary key |
| `name` | human-readable identity |
| `provider` | provider identifier |
| `model` | model identifier |
| `settings_json` | non-secret model/runtime settings |
| `provider_credential_id` | FK to provider credential binding |
| `status` | active/retired |
| `created_at` | audit |

A changed model/settings combination is represented by another immutable configuration row. Agent identities themselves are not versioned.

### 6.5 `mcp_servers`

| Column | Purpose |
|---|---|
| `id` | primary key |
| `name` | server identity |
| `transport` | supported transport such as stdio/http |
| `connection_config_json` | non-secret connection information |
| `credential_binding_id` | nullable secret/credential binding reference |
| `status` | active/disabled |
| `created_at` | audit |

MCP is a capability transport, not the persistence layer.

### 6.6 `tools`

Council-facing tool identity.

| Column | Purpose |
|---|---|
| `id` | primary key |
| `name` | stable Council-visible tool name |
| `backend_kind` | mcp/native/http/database/environment/etc. |
| `mcp_server_id` | nullable FK for MCP-backed tools |
| `remote_tool_name` | nullable external/MCP tool identifier |
| `native_tool_key` | nullable native implementation identifier |
| `status` | active/disabled |
| `created_at` | audit |

The agent interacts with the Council tool identity rather than needing to know how the backend is implemented.

### 6.7 `tool_sets`

Reusable capability bundles.

| Column | Purpose |
|---|---|
| `id` | primary key |
| `name` | e.g. independent_member, discussion_member, promotion |
| `description` | bounded description |
| `created_at` | audit |

### 6.8 `tool_set_members`

| Column | Purpose |
|---|---|
| `tool_set_id` | FK |
| `tool_id` | FK |
| `policy_json` | non-secret scope/capability restrictions |

Unique: `(tool_set_id, tool_id)`.

The same Council member may move from one tool set to another as the run changes phase. Enforcement is performed by the actual gateway/repository/sandbox permissions, not only by this row.

Example:

```text
INDEPENDENT
A: own repo read/write
B/C repos: no access

DISCUSSION
A: own repo read/write
B/C repos: read
```

### 6.9 `secret_bindings`

Optional named bindings used where a reusable secret reference needs to be associated with a Council capability.

| Column | Purpose |
|---|---|
| `id` | primary key |
| `name` | binding name |
| `secret_ref` | external secret-store reference |
| `purpose` | bounded purpose description |
| `status` | active/disabled |

The actual secret value never appears in PostgreSQL, prompts, or ordinary logs.

### 6.10 `council_presets` (optional)

A convenience layer for reusable combinations such as:

- council member count;
- prompt ids;
- model config ids;
- tool set ids;
- budget/resource preset.

This is optional configuration convenience, not a requirement for agent independence.

### 6.11 Run-member configuration references

For an active run, a member only needs to reference the exact configuration it is using:

```text
run_member_config
    run_member_id
    agent_account_id
    prompt_id
    model_config_id
    tool_set_id
```

The only expected differences between otherwise identical council members may simply be:

- GitHub identity;
- repository;
- sandbox.

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
