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

## 6. Still to design in Part 7

The following remain open and must be decided before Part 7 is marked DESIGNED:

- exact distinction between a heavy private-work sandbox slot and checkpoint-participation capacity;
- what state is preserved/suspended when an early member waits at a checkpoint;
- fairness/order for activating members when fewer than five work slots exist;
- model-call concurrency separate from local sandbox concurrency;
- crash/restart recovery of member environments;
- pause and stop semantics;
- run/member budget allocation and protected checkpoint/review allowance;
- host pressure handling and resource ceilings.
