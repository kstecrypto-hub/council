# Design references

These are the upstream references identified during the design discussion. They are background and implementation starting points, not evidence that this unimplemented product already works. Runtime versions, provider capabilities, licensing, prices, and exact API contracts must be checked when implementation begins.

## Provenance and source lineage

- W3C PROV overview: https://www.w3.org/TR/prov-overview/
- W3C PROV data model: https://www.w3.org/TR/prov-dm/

Use the concepts of entities, activities, agents, usage, derivation, attribution, and delegation. Provenance records information lineage; it does not by itself establish truth.

## Agent loops and persistent execution

- Karpathy autoresearch: https://github.com/karpathy/autoresearch
- Experiment instructions: https://github.com/karpathy/autoresearch/blob/master/program.md
- Ralph implementation and documented fresh-session pattern: https://github.com/snarktank/ralph
- Geoffrey Huntley's Ralph description: https://ghuntley.com/ralph/
- LangGraph overview: https://docs.langchain.com/oss/python/langgraph/overview
- LangGraph persistence: https://docs.langchain.com/oss/python/langgraph/persistence
- LangGraph memory: https://docs.langchain.com/oss/python/langgraph/add-memory

Autoresearch contributes a bounded experiment/feedback/logging pattern. Ralph describes repeated fresh instances with external progress records. Our design adapts those mechanisms inside the selected runtime; it does not adopt coding-only prompts, permission bypasses, or indefinite execution policies.

## Model gateway

- DeepSeek model listing: https://api-docs.deepseek.com/api/list-models/
- DeepSeek thinking-mode tool continuation: https://api-docs.deepseek.com/guides/thinking_mode/

Model identifiers, prices, context allowances, and compatibility are registry data, not permanent assumptions in application code.

## Backend, graph, interface, and containment

- FastAPI features: https://fastapi.tiangolo.com/features/
- PostgreSQL recursive queries: https://www.postgresql.org/docs/current/queries-with.html
- PostgreSQL SELECT and locking: https://www.postgresql.org/docs/current/sql-select.html
- PostgreSQL JSON types: https://www.postgresql.org/docs/current/datatype-json.html
- React Flow custom nodes: https://reactflow.dev/learn/customization/custom-nodes
- Docker security: https://docs.docker.com/engine/security/
- Docker rootless mode: https://docs.docker.com/engine/security/rootless/

Graph behavior, authorization, retries, deduplication, evidence validation, and review rules still need application-specific implementation and testing.

## Repository publication only

- GitHub CLI repository creation: https://cli.github.com/manual/gh_repo_create
- GitHub CLI authentication: https://cli.github.com/manual/gh_auth_login
- Git credential setup through GitHub CLI: https://cli.github.com/manual/gh_auth_setup-git

The publishing helper uses the user's locally authenticated GitHub CLI. It never asks the user to paste credentials into the design documents or this conversation.

## Architecture-review references checked October 13, 2026

- GitHub repository visibility: https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/managing-repository-settings/setting-repository-visibility . Public publication exposes repository content and related history; public forks remain public when the original becomes private. Council's publication safeguards are design requirements, not tested integration behavior.
- PostgreSQL transaction isolation and sequence behavior: https://www.postgresql.org/docs/current/transaction-iso.html . Sequence allocation is not transactional commit order; the event-clock protocol is Council's chosen design and still needs integration tests.
- LangGraph persistence: https://docs.langchain.com/oss/python/langgraph/persistence . Framework continuation does not replace Council's own operation/authorization/accounting authority; concrete adapter/replay behavior must be verified during implementation.

## Step 8.2a Docker persistence references (October 14, 2026)

- Docker named volumes and their lifecycle: https://docs.docker.com/engine/storage/volumes/ . Volume content remains independent of the container's writable layer and persists across container removal unless the volume is explicitly deleted. Bind mounts are an alternative when explicitly permitted.
- Docker container writable layers versus durable mounts: https://docs.docker.com/engine/storage/ . A deleted container loses its writable layer; `tmpfs` also does not provide persistent storage.
- Docker automatic restart policies: https://docs.docker.com/engine/containers/start-containers-automatically/ . Container restart starts the configured process again; it does not restore arbitrary in-memory worker/process state and must not bypass Council's intentional whole-member stop/admission gates.

Council's chosen worker recovery model is **member-owned persistent workspace files on authorized Docker mounts**, not a Council per-worker recovery manager. The references provide Docker mechanics, not a claim that a live Council volume-restart workflow has been implemented or verified.

## Step 8.2 Docker monitoring references (October 14, 2026)

Official backend references for the approved **design-only** trusted Council Resource Monitor:

- Docker `docker stats` behavior: https://docs.docker.com/reference/cli/docker/container/stats/ . Docker CLI memory presentation can differ from raw API memory stats/cache fields.
- Docker Engine `GET /containers/{id}/stats`: https://docs.docker.com/reference/api/engine/version/v1.51/ . Negotiate the actual server-supported API; do not hard-code v1.51.
- Docker resource constraints and OOM risks: https://docs.docker.com/engine/containers/resource_constraints . Supported CPU/memory/PIDs/cgroups hard limits reduce damage but do **not** guarantee a workload cannot crash.
- Docker Engine container events (including `oom`, `die`, `restart`): https://docs.docker.com/reference/cli/docker/system/events/ .
- Docker Desktop WSL2 backend and VM resource boundaries: https://docs.docker.com/desktop/features/wsl/ and https://docs.docker.com/desktop/features/wsl/best-practices/ .
- Docker storage/volumes and why block-I/O does not equal free disk space: https://docs.docker.com/engine/storage/drivers/ .
- NVIDIA NVML as optional supported GPU/VRAM observer: https://developer.nvidia.com/management-library-nvml and https://docs.nvidia.com/deploy/nvml-api/latest/index.html .

These sources describe available primitives, **not** a tested Council monitoring service, GPU isolation guarantee, OOM prevention guarantee, or permission to expose Docker Engine credentials inside agent sandboxes. Windows Resource Monitor and Prometheus/Grafana are not MVP dependencies.
