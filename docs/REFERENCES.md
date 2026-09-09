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
