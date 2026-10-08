# Part 7 - member execution scheduling, recovery, and resource controls

**Status:** IN DESIGN.  
**Scope:** runtime scheduling of Council-member execution environments, checkpoint barriers, resource limits, recovery, pause/stop, and budget controls.  
**Implementation status:** specification only.

## 1. First locked rule: schedule member environments, not their internal work

Each fixed Council member owns and controls its own private sandbox environment during private development.

The trusted Council runtime does **not** schedule or intellectually manage the member's internal tests, files, subtasks, worker decomposition, or development steps. Those remain inside the member's sandbox and branch authority.

Step 7 schedules coarse execution capacity around whole Council-member environments.

Conceptually:

```text
Five logical Council members:
A  B  C  D  E

Host allows N active work sandboxes at once:
N may be 1, 2, 3, 4, or 5 depending on configured/available resources.
```

The number of logical Council members does not change with machine capacity. Only wall-clock parallelism changes.

## 2. Member execution slots

The runtime may activate only as many member work sandboxes concurrently as the deployment resource policy allows.

Example with two active work slots:

```text
slot 1 -> A
slot 2 -> B

C, D, E -> not currently executing
```

When a running member reaches the current semantic checkpoint milestone, it stops private development beyond that barrier and releases its scarce work-execution slot. Another logical member that has not yet reached the checkpoint may then start or resume.

The scheduler decides **when a member environment may execute** based on resource/budget policy. It does not decide which member's intellectual approach is better or direct the contents of that member's private work.

## 3. Checkpoints are all-member barriers

Every planned semantic checkpoint is a barrier across all fixed Council members participating in the project.

A member can reach the checkpoint earlier than another member even when some members started later because host capacity forced staggered execution.

Example:

```text
A -> CHECKPOINT_READY
B -> still working
C -> not started
D -> not started
E -> not started
```

A does not proceed into the next private-development phase.

Its checkpoint repository state is frozen/recorded and it waits while the released work slot can be used by another member.

Checkpoint review/communication does not open until all required Council members have independently reached the same checkpoint milestone:

```text
A READY
B READY
C READY
D READY
E READY
    |
    v
OPEN CHECKPOINT REVIEW
```

Therefore host capacity changes elapsed time, not the logical Council protocol.

## 4. Barrier semantics

For checkpoint K:

1. a member privately develops toward the Orchestrator-defined semantic milestone;
2. when that member declares the milestone reached, runtime records/finalizes its checkpoint-ready repository SHA and required checkpoint metadata;
3. that member may not continue into post-checkpoint private revision before checkpoint K has opened, completed, and closed;
4. its scarce private-work execution capacity can be released while other members continue toward K;
5. runtime opens checkpoint K only when every required member is ready;
6. the existing checkpoint review/communication protocol runs;
7. checkpoint K closes and each member receives its deterministic return packet;
8. members may then enter the next private-development phase as execution capacity becomes available.

A faster member is never allowed to gain an extra private development phase merely because it reached the barrier first.

## 5. Separation from Part 5 task leasing

Part 5 still uses durable operations, leases, retries, and reconciliation for **trusted runtime work** such as provisioning, external side effects, access changes, publication, and other Council-controlled operations.

Those runtime records must not be misinterpreted as a central scheduler for the agent's private internal work.

Agent-internal development remains controlled by the agent inside its sandbox.

## 6. Second locked rule: checkpoint participation may be time-sliced

All required members must reach the checkpoint barrier before review opens, but all member sandboxes do **not** need to execute simultaneously during the review.

If host capacity allows fewer than five active member sandboxes, runtime may time-slice checkpoint participation across the same logical members and their existing sandboxes.

Example with two active sandbox slots:

```text
checkpoint K is OPEN

active:   A, B
waiting:  C, D, E
```

A and B participate from their existing member environments in checkpoint mode. They may inspect the frozen peer snapshots they are authorized to see, receive/send checkpoint messages and structured actions, and use the already-approved verification-only `/work` path.

They may not continue private implementation/revision beyond the frozen checkpoint state.

When a member currently has no communication obligations and satisfies the existing `/done` rules, its sandbox may release the active slot. Another checkpoint member can then resume and receive the complete ordered checkpoint transcript/messages and current structured-action obligations that accumulated while it was inactive.

```text
A + B active
A -> /done
A slot released
C resumes
C receives accumulated checkpoint traffic
```

Checkpoint communication is therefore durable and asynchronous-capable even though members may also communicate live when multiple slots are available.

If an inactive/DONE member receives a new required QUESTION, CHALLENGE, or TEST_REQUEST, its checkpoint status returns to AVAILABLE and the scheduler must give it another participation turn before normal checkpoint closure can succeed.

The runtime does not replace a suspended member with a lightweight substitute or a new logical agent. It resumes the **same logical Council member and same sandbox state**. Hardware capacity changes checkpoint latency, not Council membership, identity, access rules, or review semantics.

A deployment with one active sandbox slot can therefore execute a five-member checkpoint by rotating A -> B -> C -> D -> E and revisiting members when new required obligations appear. A deployment with five slots may allow all five to participate concurrently.

The durable Checkpoint Communication Gateway is the synchronization layer: messages/actions remain ordered and available while a member is not executing. No direct sandbox-to-sandbox communication is introduced.

## 7. Third locked rule: durable suspend by persistence + container stop

When a member releases an execution slot, Council does not rely on a long-lived paused container or preserved process memory.

The trusted runtime first **quiesces** the member sandbox, persists the durable project/environment state required to reconstruct it, records the suspension point, and then stops the execution container so CPU, RAM, GPU/device reservations, and process capacity can be released.

A normal suspension sequence is:

```text
member running
  -> stop accepting new private work
  -> finish/abort to a safe boundary
  -> flush persistent filesystem/database state
  -> record current repo SHA + sandbox/environment version
  -> persist logical-agent continuation state
  -> mark member SUSPENDED / CHECKPOINT_READY as appropriate
  -> stop execution container
  -> release compute slot/resources
```

Durable sandbox state includes, where applicable:

- private workspace/files;
- authoritative member repository and Git metadata;
- project-local databases/data;
- installed project dependencies and reproducible environment definition;
- configuration created by the member;
- agent-created tools/scripts;
- build/test artifacts intentionally retained;
- logical-agent continuation/recovery state.

The **logical sandbox identity persists**, but the underlying container process/ID does not need to. On resume, runtime may recreate a fresh execution container around the same preserved sandbox state:

```text
slot available
  -> reconstruct/start member container
  -> attach same private persistent state
  -> validate expected environment/repo state
  -> reissue currently authorized ephemeral capabilities
  -> load continuation/checkpoint obligations
  -> resume same logical Council member
```

Council does not require process-memory checkpoint/restore for MVP. Open sockets, in-memory Python processes, GPU state, and similar ephemeral execution details are not treated as durable agent memory. Logical continuity comes from preserved files/state plus continuation records.

Ephemeral authority must **not** be made durable merely because the sandbox filesystem persists. Provider tokens, checkpoint credentials, temporary peer-repo grants, gateway session credentials/routes, privileged broker grants, and similar capabilities are runtime-controlled and reissued only if the resumed member is currently authorized to have them.

Thus suspension frees active compute while preserving the member's project state and identity, without allowing stale credentials or capabilities to survive across lifecycle transitions.

## 8. Fourth locked rule: deterministic seat-order scheduling

When fewer than five Council-member sandboxes can execute at once, the runtime schedules eligible members in fixed ascending seat order:

```text
Member 1 -> Member 2 -> Member 3 -> Member 4 -> Member 5 -> wrap
```

The runtime skips a member that currently requires no execution and returns to it on a later rotation if it becomes eligible again.

Examples:

- private development: if slots 1 and 2 are occupied by Members 1 and 2, the next released slot goes to Member 3, then Member 4, then Member 5;
- checkpoint review: a member already at `/done` with no new obligations is skipped; if a later required QUESTION, CHALLENGE, or TEST_REQUEST makes it AVAILABLE again, it re-enters the normal seat-order rotation.

Seat number is a stable identity only. It is **not** rank, seniority, intellectual authority, model quality, or scheduling priority derived from the member's approach.

Council therefore does not need a fairness scorer or branch-importance scheduler.

## 9. Step 7 / Step 8 execution boundary

Step 7 controls whether a Council member is allowed to execute and what resources it may consume.

It may enforce:

- active sandbox-slot ceilings;
- remote model-call concurrency/rate ceilings;
- local-model CPU/GPU/RAM ceilings;
- run/member budget ceilings;
- pause/stop/resource-pressure controls.

Step 7 does **not** decide the member's intellectual loop, how many reasoning iterations are enough, whether an approach is promising, or when the work is substantively complete.

The member's repeated observe/reason/act/delegate/evaluate loop and its decision to emit `CHECKPOINT_READY`, `BLOCKED`, or final-candidate readiness belong to Step 8.

Remote and local inference use the same logical agent loop. The difference is resource accounting: remote inference consumes provider calls/tokens/cost/rate limits; local inference consumes host compute such as GPU/VRAM/RAM/CPU.

## 10. Still to design in Part 7

The following remain open and must be decided before Part 7 is marked DESIGNED:

- crash/restart recovery when suspension or reconstruction is interrupted mid-transition;
- exact remote model-call concurrency/rate ceilings and local-model resource ceilings;
- crash/restart recovery of member environments;
- pause and stop semantics;
- run/member budget allocation and protected checkpoint/review allowance;
- host pressure handling and resource ceilings.
