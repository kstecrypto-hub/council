# Orchestrator development-pattern library — semantic checkpoint planning

**Owner approval:** October 15, 2026. **Status:** APPROVED DESIGN DIRECTION; pattern taxonomy, retrieval ranking and exact v1 schema are IN DESIGN. **Implementation:** NOT STARTED. **Runtime tests:** NOT RUN. This is an extension of the **existing Project Orchestrator**, not a sixth Council member, another central intellectual reviewer, separate service, new database or imposed software-development process.

## 1. Purpose and authority

The Orchestrator already owns creation of the **user-approved, outcome-based semantic checkpoint plan**, with the same logical approved objective delivered to all five independent members. The owner proposes that its checkpoint planning consult an **optional development knowledge library** of well-attributed patterns for how categories of products are built. The goal is **better-informed milestones**: where to demand demonstrable integration, risk investigation, validation, and reproducible evidence appropriate to the actual project.

The pattern library advises the **Orchestrator's checkpoint design only**. It never chooses a coding stack, solution algorithm, project direction, member work decomposition, implementation architecture, test result, winning candidate or private-branch task list. A library reference is not authority to narrow the approved Project Contract or prescribe solution components. Runtime still does not decide CHECKPOINT_READY: each of the fixed five members decides this independently; all-five verified arrivals determine opening. Time estimates never turn into forced member deadlines.

For non-programming Council runs, use the same mechanism with approved research/engineering/analysis methodology patterns, or plan directly without a match. A purported library-matched "standard practice" does not override user requirements or actual evidence.

## 2. Deployment without new infrastructure

**Authoritative curated pattern library:** versioned structured Markdown/YAML/JSON data shipped with the installed customer-controlled Council product or in a separately approved customer-local extension directory. Ship no proprietary customer data in public/global Council defaults. The application version and individual pattern content/version hash identify exactly what was consulted.

**Retrieval:** during setup, the trusted Orchestrator module queries an embedded indexing layer over approved local pattern files: category tags, feature/constraint tags, and deterministic full-text or PostgreSQL-native text search as the initial default. It may use semantic retrieval **only if** later needed, proven useful and authorized. No separately deployed vector DB, graph DB, retrieval agent or external search service is required for the MVP. Searching local files must not expose other tenant data.

**Project-state persistence:** the existing project-local PostgreSQL Project Contract/checkpoint-plan revision stores (a) the generated milestone plan and accepted plan revision; (b) referenced pattern IDs, file revisions/content hashes, relevance/context notes; (c) explicit source/fallback provenance. The Orchestrator retains only a small *planning/clarification memory*, not copies of five members' private investigation histories. Immutable contract revision semantics and user acceptance remain unchanged.

**Optional customer-specific patterns:** the customer may maintain private local extensions scoped to its own tenant and permission policy. No customer-generated milestone patterns, experiment summaries, private Git source or company experience are uploaded to a vendor/general library by default. Cross-customer reuse follows the already approved Step 11 opt-in, privacy/IP/license review and permissioned archival, not an Orchestrator shortcut.

## 3. Minimal pattern record

Each curated entry includes:
- **pattern_id, version, content_hash, provenance/usage rights, author/source references**;
- **domain and applicability tags** (e.g. SaaS with tenant isolation, embedded devices with hardware-in-loop, RAG over sensitive documents, robotics with sensors and actuators; non-code research types where appropriate);
- **preconditions and explicit non-applicability warnings**, project size, risk factors, core dependencies and important unknowns;
- **illustrative semantic outcomes/milestones** and **observable evidence suggestions** suited to review (e.g. a documented working end-to-end workflow, measured integration conditions, a reproducible baseline or clearly labeled blocked validation);
- **common failure/risk patterns** and possible integration/evidence omissions, with uncertainty and source qualifiers;
- **alternatives and flexibility**: no mandatory technical stack/implementation sequence unless required by the user's actual approved objectives;
- **limitations** and a change/provenance history so a later version does not silently rewrite an earlier run's planning basis.

Sample SaaS pattern: checkpoint evidence might progress from an independently justified overall design/baseline to functioning core host/guest workflows, then cross-boundary tenant isolation/integration/security evaluation, then deployment/acceptance evidence. Those are **illustrative** outcomes, not a fixed four-checkpoint template. Five members may reach outcomes through entirely different architectures.

## 4. Retrieval and fallback algorithm (architectural contract)

1. Orchestrator obtains the user-approved objective draft, scope, deliverables, constraints, evidence profile and permissions. It identifies **possible**, not falsely certain, project categories and cross-domain components.
2. Retrieve relevant authorized, versioned patterns locally, considering preconditions/constraints, dependency and evidence coverage; retain IDs/content hashes and applicable limitations. Multi-domain projects may combine compatible patterns, with the Orchestrator avoiding contradictory or redundant milestone obligations.
3. Produce a **project-specific semantic checkpoint proposal**: each checkpoint names a reviewable outcome, required *kind* of supporting evidence, important integration/uncertainty coverage, and relations to the user-approved contract. It does **not** prescribe how members must implement the outcome, force an AI-selected code stack, dictate internal worker strategy or choose a preferred candidate.
4. If patterns are **strongly applicable**, adapt them. If **partially applicable**, incorporate only supported aspects. If **nothing relevant is found**, **still generate a reasonable checkpoint plan from the approved project requirements**. A missing pattern is not a reason to block launching the project or fabricate a citation. Record `requirements_derived_no_library_match` in provenance.
5. Present the resulting phase/checkpoint plan and key rationale to the user for the **existing Project Contract approval**, with pattern references and uncertain assumptions appropriately labeled. Only approved revisions become authoritative for the five members. If the user changes the contract, re-derive and version a plan as already required; never retroactively alter historical approvals.

No library entry automatically grants new permissions, an external data source, model costs, network egress or authority to access member-private code. Domain-general planning works even if no library was installed or its index is unavailable.

## 5. Why this does not compromise independence

The library helps establish *what the milestone should demonstrate* and *which validation risks ought to be considered*, not *how five candidates must be built*. A source suggesting relational databases are common in an app is not authorization to make all agents use PostgreSQL. Members independently choose techniques, tests, experiments and readiness timing within budgets. The library is **only** used by the Orchestrator in neutral setup and when the **user approves** material plan revisions. It must not grow into an AI supervisor that judges member candidates or private reasoning.

Do not confuse (a) a general, permitted source of development-method patterns, (b) Step 11 customer-owned accepted-project reuse, and (c) the Orchestrator's deliberately small project-specific memory. They have different audiences and permissions. No direct bypass of Step 11 retention and cross-customer consent rules.

## 6. Integration and completion status

**Step 4A:** the existing Orchestrator gains `consult authorized planning-pattern library` as a checkpoint-plan generation *input*, not a new authority or tool that agents use for peer exchange.

**Step 3:** existing versioned Project Contract and checkpoint-plan records retain pattern IDs/versions/hashes and plan provenance, not a copy of every library item.

**Step 4/5:** current contract-revision approval/idempotency and user-confirmation semantics protect the plan. Retrieval failures and pattern unavailability are ordinary degradations to requirements-only planning, **not** failed checkpoint opening or model-induced readiness.

**Step 11:** curated generic records are separate from permission-scoped customer-derived project knowledge. If users explicitly choose customer-local pattern expansion based on prior accepted projects, honor their existing retention and opt-in restrictions.

**Step 8.3:** no change to member readiness/verified freeze or all-five barrier. **Step 8.4:** checkpoints/review use the same user-approved semantic plan; no automatic objective or solution evaluation by the Orchestrator.

**OPEN DESIGN:** initial curated content set and versioned schema, compatibility/ranking criteria, license attribution, user-facing rationale/sourcing and any future permitted promotion of customer-derived planning knowledge. **APPROVED POLICY:** optional reference improves accuracy, partial/no-match fallback always plans, no additional Orchestrator intellectual authority, user-approved checkpoints and member self-declared readiness. No code, retrieval index, migrations or tests have been implemented.
