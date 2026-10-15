# Step 2 - Customer-local Git and checkpoint reads (approved subdesign)

**Decision date:** October 15, 2026. **Status:** owner-approved architectural choices; Step 2 remains IN DESIGN for precise interfaces and dependency/transfer/recovery policy. **Implementation:** NOT STARTED. **Runtime tests:** NOT RUN.

This specification supplements [ADR-17](LOCAL_REPOSITORY_AND_KNOWLEDGE_RETENTION.md), the [checkpoint communication contract](CHECKPOINT_COMMUNICATION_GATEWAY.md), and [Steps 2-5](MVP_SCOPE_BY_STEP.txt). It replaces no existing runtime verification requirements.

## Customer ownership and placement

- Use **native local Git** on infrastructure owned or controlled by the customer/company, not the Council vendor's Git, GitHub account, or server. "Local Git" is the Git version-control program and object store; it does not imply any remote service, external account, or public repository.
- Each run provisions **five separate, temporary, customer-owned Git repositories/workspaces**, one for each independent Council member, within member-private persistent Docker volumes or customer-approved equivalent mounts. The volumes remain customer-controlled even while containers stop/restart. One member never mounts another member's private workspace.
- A separately trusted host-side snapshot service operates **outside agent sandboxes**. The Council app and its own development repository are distinct from customers' projects. Company source is **not** mirrored to Council/vendor-owned Git or a hosted service by default.
- The company can explicitly authorize its **own** self-hosted Git server, GitLab/GitHub Enterprise, or other destination; this is an optional adapter/export, not a required part of Council.

## Checkpoint content and reads

1. When all five members legitimately arrive at an approved semantic checkpoint, freeze each member's chosen committed Git tree/revision and verify its identity. A member's private work stays unavailable before checkpoint authorization.
2. The trusted service exports a **selected, immutable, content-hashed, read-only snapshot** with a manifest of allowed paths, objects, revision/hash, and included artifact references. Export the approved file tree only, not full Git ancestry, hidden refs, credentials, or uncommitted work by default. Inspect/include sensitive data only as allowed by the customer's permissions.
3. Each authorized member receives **read access** to the other members' approved frozen snapshots, never write access or live access to their underlying Git repositories.
4. **All member-facing peer requests pass through the existing Council IRC-inspired checkpoint communication bridge**, with authorization and storage handled by the separate snapshot service outside the sandboxes. Members can request the snapshot tree, named files, or pinned authorized artifacts. Large/binary files use bounded, integrity-checked response transfers, not wholesale copies into IRC group messages or model context. Agents do not receive raw IRC administration, a peer's Git credentials, or direct peer/volume network paths.
5. Preserve **five sealed, independent reviews** before reveal. During sealed review, allowed source inspection does not reveal other reviewers' assessments. During `/work`, members may inspect/test pinned snapshots in disposable verification-only environments, not modify any authoritative candidate.
6. Checkpoint closure fences **both discussion and repository-read permissions** using the same checkpoint generation/lifecycle. The trusted service also verifies that read access and transfer routes were actually revoked; partial/UNKNOWN outcomes cannot be marked successfully closed. Members may retain information they legitimately saw, so revocation is about **new** reads, not impossible erasure of memory.

## Dependencies, artifacts and lifecycle

- Lockfiles/versions, submodules, LFS references, generated outputs, large binaries, and other required inputs are explicitly identified in each snapshot manifest. An unapproved dependency or missing required artifact blocks complete checkpoint publication; never silently fetch/expose confidential or external data. Prefer permitted hashed artifacts to cloning additional repos.
- After customer acceptance, export the selected implementation and authorized build/test/reconstruction information to a **customer-selected destination**, which can itself be local Git or a company-managed service. Retain failed approaches or other candidate artifacts only under the company's retention policy; do not automatically copy any customer code/lessons into Council's vendor-wide memory. Verify authorized archival and references before deleting project-lifetime Git, sandboxes, and database state.
- **Local Git alone is not a complete confidentiality guarantee:** remote LLM inference, web/tool access, telemetry, logs, and optional external publication require separately authorized egress boundaries. BYOK relates to provider billing and does not imply permission to transmit confidential company files.

## Open Step 2 engineering/design tasks

Specify the versioned tree/file/artifact request-response contracts, canonical grants, streaming/chunk limits and replay receipts, path and hash validation, submodule/LFS resolution, snapshot/volume layout, safe file/import filtering, egress enforcement, crash and UNKNOWN reconciliation, verified revocation, and how these new operations connect to Step 3 records, Step 4 commands/events, and Step 5 transactional guarantees. Step 8 checkpoint/finalization integration remains separate. **Do not mark Step 2, Steps 3-5, runtime implementation, or tests complete merely because these design choices were committed.**
