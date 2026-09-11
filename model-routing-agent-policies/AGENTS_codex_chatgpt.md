# AGENTS.md — Codex / ChatGPT Model Routing Policy

> Last reviewed: September 2026.
>
> Goal: use the **fastest / least expensive model that can reliably finish the task**, while recognizing that GPT‑6 Astra is not merely a "bigger Sol": it is particularly valuable for difficult **end-to-end agentic work**, long-horizon execution, large context, computer use, browsing, and workflows that span multiple tools.

---

# 1. Routing Philosophy

Choose models on **two axes**, not one:

1. **Reasoning difficulty**
   - How hard is the intellectual problem?

2. **Agentic horizon**
   - How many steps, tools, systems, context windows, and course corrections must be coordinated before the task is finished?

This distinction matters.

A hard but bounded algorithmic problem may be a good fit for **GPT‑5.6 Sol**.

A similarly difficult task that requires hours-worth of repository exploration, browser research, terminal work, document creation, repeated verification, and adaptation is a better fit for **GPT‑6 Astra**.

Default hierarchy:

> **Luna executes → Terra builds → Sol reasons deeply → Astra owns the hardest end-to-end workflows.**

Do not use the hierarchy mechanically. Route based on task shape.

---

# 2. Model Tiers

## Tier 1 — GPT‑5.6 Luna

Use for fast, inexpensive, bounded work.

Best for:
- repository search
- locating files and symbols
- grep-like exploration
- extracting structured information
- mechanical edits
- formatting
- renaming
- repetitive changes
- boilerplate
- simple unit tests
- straightforward documentation
- summarizing logs
- small isolated fixes with explicit requirements

Typical reasoning:
- low / Instant where available

Avoid for:
- architecture
- ambiguous debugging
- high-risk financial or compliance logic
- broad refactors
- cross-system reasoning
- difficult tool orchestration

---

## Tier 2 — GPT‑5.6 Terra

Use as the **default engineering and analysis model**.

Best for:
- normal feature implementation
- multi-file changes
- frontend/backend work
- APIs
- SQL and data engineering
- tests
- routine refactoring
- bounded debugging
- CI/CD
- normal code review
- technical documentation
- implementation planning
- understanding unfamiliar repositories
- moderate performance optimization
- ordinary business/data analysis

Typical reasoning:
- low or medium

Default rule:

> If the task is neither clearly mechanical nor clearly frontier-level, use Terra.

---

## Tier 3 — GPT‑5.6 Sol

Use for **deep but reasonably bounded reasoning** and high-risk decisions.

Best for:
- system architecture
- difficult root-cause analysis
- complex algorithms
- complex data-model design
- concurrency reasoning
- distributed-system design
- security-sensitive review
- authentication / authorization
- difficult migrations
- large cross-cutting refactors
- complex performance problems
- contradictory requirements
- financial calculations
- AML / financial-crime / compliance logic
- high-impact technical review

Typical reasoning:
- medium

Use high / extra-high when:
- several plausible solutions need careful comparison
- the system has many interacting constraints
- earlier attempts failed
- correctness matters substantially more than latency
- adversarial review is needed

Sol is often the best choice when the task is **intellectually hard but can still be kept inside a relatively coherent problem boundary**.

---

## Tier 4 — GPT‑6 Astra

Model ID when directly selectable:
`gpt-6-astra`

Use Astra for the **hardest end-to-end work**.

Astra is preferred when difficulty comes not only from reasoning, but from having to remain oriented and effective across a long sequence of actions.

Best for:
- complex end-to-end software engineering
- large repository work requiring sustained context
- long-horizon debugging
- difficult multi-service migrations
- browser + terminal + code workflows
- computer-use-heavy tasks
- deep research that must turn into implementation or finished artifacts
- work spanning code, documents, data, browser, and professional tools
- large refactors with many dependent steps
- complex autonomous investigations
- tasks where requirements evolve materially during execution
- difficult work that requires repeated verification and adaptation
- high-value workflows where avoiding several failed iterations matters more than minimizing per-call cost

Supported reasoning levels may include:
- low
- medium
- high
- xhigh
- max

Do **not** automatically use max reasoning.
Astra at medium/high may be better than using a weaker model at maximum effort for a long-horizon task.

---

# 3. Astra Is Not Just "Sol but Smarter"

The routing distinction should be:

## Prefer Sol when:
- the task is difficult but bounded
- the relevant context can be narrowed effectively
- most of the work is reasoning rather than tool coordination
- one or a few files/components dominate the problem
- architecture or review is the main deliverable
- cost / usage conservation matters
- implementation can be delegated after the difficult decision is made

Examples:
- choose between three database schemas
- reason about a race condition once evidence is collected
- review AML scoring logic
- design an authorization model
- evaluate a migration strategy

## Prefer Astra when:
- the task is both difficult **and** long-horizon
- many tools must be coordinated
- the task spans several systems or work surfaces
- context preservation itself is a challenge
- the model must repeatedly inspect, act, test, observe, and adapt
- requirements may evolve during execution
- failed intermediate attempts would be expensive
- the user wants a finished end-to-end result rather than only a recommendation

Examples:
- understand a large unfamiliar monorepo, redesign a subsystem, implement it, migrate usages, test it, and update documentation
- investigate an intermittent production issue across logs, code, configuration, and browser behavior
- research a new framework, design an implementation, build it, test it, and produce deployment documentation
- carry a multi-stage data migration from discovery through validation and rollback planning
- complete a substantial professional workflow across browser, files, spreadsheets, documents, and code

---

# 4. GPT‑6 Pro in ChatGPT

Where ChatGPT exposes **GPT‑6 Pro powered by GPT‑6 Astra**, treat it as the ChatGPT-facing top-tier Astra experience.

Use it for:
- the hardest professional analysis
- highly complex research
- long multi-step Work tasks
- complex artifact creation
- expert review where maximum quality is worth higher usage

Do not assume it is available on every account, surface, plan, or workspace.

In Codex, prefer the actual Astra model when available.

---

# 5. Model + Reasoning Effort Are Separate Decisions

Always choose:

1. **model**
2. **reasoning effort**

Do not automatically increase both.

Examples:

### Rename symbols
Luna + low

### Normal API endpoint
Terra + medium

### Difficult but bounded architecture decision
Sol + high

### Large end-to-end refactor across many systems
Astra + medium/high

### Critical end-to-end migration with unresolved trade-offs
Astra + high/xhigh

### Repetitive fixtures after architecture is settled
Luna + low

The largest model does not always need the highest reasoning setting.

---

# 6. Task Classification

Before starting meaningful work, classify it across six dimensions.

## A. Complexity
- Low — mechanical/local
- Medium — several steps/files
- High — deeply coupled, novel, architectural

## B. Ambiguity
- Low — explicit requirements
- Medium — interpretation required
- High — conflicting requirements or unknown root cause

## C. Risk
- Low — reversible/cosmetic
- Medium — ordinary application behavior
- High — security, money, compliance, destructive data changes, production availability

## D. Context breadth
- Low — one function/file
- Medium — component/several files
- High — several services/repos/schemas/tools

## E. Agentic horizon
- Short — one or two direct actions
- Medium — several dependent actions
- Long — many steps, repeated observation/verification, changing state, tool coordination

## F. Evidence state
- Is the root cause known?
- Are assumptions verified?
- Are tests available?
- Has a previous attempt failed?
- Are there contradictions in the evidence?

Agentic horizon is the main additional signal for deciding **Sol vs Astra**.

---

# 7. Routing Matrix

| Situation | Preferred model | Typical effort |
|---|---|---|
| Search / extraction / formatting | Luna | Low |
| Mechanical edit | Luna | Low |
| Simple isolated bug | Luna or Terra | Low |
| Normal implementation | Terra | Low–Medium |
| Multi-file feature | Terra | Medium |
| Routine refactor | Terra | Medium |
| Normal code review | Terra | Medium |
| Moderately ambiguous debugging | Terra | Medium |
| Hard bounded debugging | Sol | High |
| Architecture decision | Sol | High |
| Security/compliance reasoning | Sol | High |
| Financial/AML logic | Sol | High |
| Difficult distributed/concurrency reasoning | Sol | High |
| Long-horizon multi-system debugging | Astra | High |
| Large autonomous refactor | Astra | Medium–High |
| Browser + code + terminal workflow | Astra | Medium–High |
| Large-context end-to-end implementation | Astra | Medium–High |
| Major end-to-end migration | Astra | High |
| Exceptional expert end-to-end work | Astra | XHigh/Max |

---

# 8. Direct-to-Astra Rules

Do **not** force every task through Luna → Terra → Sol before Astra.

Start directly with Astra when at least one of these is clearly true:

- the task is explicitly end-to-end and large
- it spans several systems and tools
- substantial computer/browser use is required
- long-term context preservation is essential
- the task requires sustained autonomous execution
- several dependent phases must be completed, not merely planned
- the user expects a finished professional deliverable plus implementation
- repeated lower-model retries would predictably waste more resources than starting with Astra

Escalation is useful when complexity is uncertain.

It is wasteful when the task is obviously Astra-shaped from the beginning.

---

# 9. Escalation Policy

## Luna → Terra

Escalate when:
- meaningful reasoning is required across multiple files
- requirements are ambiguous
- public interfaces change
- tests fail for non-obvious reasons
- shared abstractions are affected
- the task is no longer mechanical

---

## Terra → Sol

Escalate when:
- one serious implementation/debugging attempt fails
- multiple plausible root causes remain
- architecture must change
- security or permissions are involved
- financial/compliance behavior is involved
- destructive data operations are involved
- difficult concurrency/distributed-state reasoning is central
- blast radius is high

Use Sol when the problem can still be narrowed to a coherent decision or reasoning problem.

---

## Terra/Sol → Astra

Escalate to Astra when:
- the task keeps expanding across systems
- long-horizon coordination becomes the main difficulty
- repeated tool interactions are required
- context loss or compaction is harming progress
- implementation requires many dependent phases
- the model must repeatedly navigate code/browser/apps and adapt
- lower tiers understand pieces of the task but struggle to finish the whole workflow reliably

---

# 10. De-escalation

Even when Astra owns the parent task, do not make Astra perform every trivial subtask.

Preferred pattern:

> **Astra orchestrates → Sol decides difficult bounded questions → Terra implements bounded components → Luna performs mechanical work.**

Examples:

## Large migration
- Astra: own end-to-end execution and state
- Sol: resolve difficult schema/architecture decisions
- Terra: implement individual migration components
- Luna: repetitive edits and extraction

## Difficult production bug
- Luna: search logs/files
- Terra: reproduce and gather evidence
- Sol: reason about a difficult bounded hypothesis
- Astra: coordinate cross-system investigation if the issue remains broad
- Terra: implement verified fix

## Large product build
- Astra: plan and coordinate end-to-end build
- Sol: major architecture decisions
- Terra: implementation workstreams
- Luna: repetitive supporting work

The parent remains responsible for validating delegated output.

---

# 11. Codex Workflow

For ordinary coding:

1. Read repository instructions.
2. Inspect relevant files.
3. Classify complexity, risk, breadth, and agentic horizon.
4. Choose model + effort.
5. Implement the smallest coherent change.
6. Run relevant tests, lint, type checks, or builds.
7. Inspect the diff.
8. Fix evidence-backed failures.
9. Escalate only if the current task shape now warrants it.
10. Report:
   - what changed
   - verification performed
   - remaining assumptions/risks

For long-horizon work:

1. Prefer Astra as parent/orchestrator.
2. Maintain explicit task state.
3. Break execution into milestones.
4. Preserve key decisions and failed hypotheses.
5. Verify after each meaningful stage.
6. Delegate bounded subproblems to cheaper models when possible.
7. Reconcile delegated results before continuing.
8. Finish the requested end state, not merely the plan.

---

# 12. ChatGPT / Work Workflow

## Luna
Use for:
- extraction
- classification
- transformations
- summaries
- formatting
- simple drafting

## Terra
Use for:
- normal analysis
- planning
- synthesis
- document creation
- business/data analysis
- moderate research synthesis

## Sol
Use for:
- difficult strategy
- bounded complex technical reasoning
- architecture
- expert critique
- financial/compliance analysis
- difficult analytical decisions

## Astra / GPT‑6 Pro
Use for:
- hardest multi-step professional work
- end-to-end Work tasks
- complex research that turns into finished artifacts/actions
- workflows spanning browser/files/apps/code
- difficult long-context synthesis
- projects requiring sustained orientation and adaptation

---

# 13. Research Workflow

Separate:
1. evidence
2. inference
3. recommendation

Use:
- Luna for retrieval/extraction
- Terra for normal synthesis
- Sol for difficult interpretation and competing hypotheses
- Astra for large end-to-end research programs involving many sources, tools, artifacts, and follow-on actions

For fresh facts:
- verify using available web/search tools
- do not rely on model memory alone

Astra should not replace evidence gathering with unsupported confidence.

---

# 14. Debugging Protocol

Do not guess-and-patch repeatedly.

Require:
1. reproduction
2. relevant code path
3. logs/error evidence
4. explicit hypothesis
5. experiment
6. conclusion
7. minimal fix
8. regression test

Start:
- Terra for normal bugs
- Sol for clearly difficult bounded bugs
- Astra for clearly broad, multi-system, long-horizon investigations

Escalate Terra → Sol when the reasoning is hard.

Escalate Sol → Astra when **coordination and horizon**, not just reasoning, become the bottleneck.

---

# 15. Architecture Protocol

Usually start with Sol.

Require:
- goals
- constraints
- assumptions
- options
- trade-offs
- recommendation
- boundaries/contracts
- failure modes
- migration
- testing
- observability
- rollback

Use Astra instead when architecture is only one phase of a larger task that must then be executed across many systems.

Example:

> "Design the migration" → Sol

> "Understand the current platform, design the migration, implement it across six services, validate it, and update deployment/docs" → Astra parent, with Sol supporting critical decisions.

---

# 16. Review Policy

## Routine review
Terra + medium.

## High-risk bounded review
Sol + high.

Required for:
- authentication
- authorization
- security boundaries
- cryptography
- financial calculations
- transaction processing
- AML / transaction-monitoring controls
- regulatory/compliance logic
- destructive migrations

## Large end-to-end independent review
Astra when:
- the review spans a large system
- many artifacts/repos/tools must be reconciled
- the reviewer must run substantial verification
- final integration quality is the main concern

---

# 17. Cost and Usage Discipline

Optimize for **cost per successful completed task**, not token price alone.

Rules:
- do not use Astra for grep/search/formatting
- do not use Sol for repetitive edits
- do not force Luna through difficult reasoning
- do not force Sol through a workflow whose real difficulty is long-horizon execution
- decompose large tasks where decomposition genuinely reduces cost
- start directly with Astra when lower-model retries are predictably wasteful
- reuse verified findings
- stop analysis when evidence is sufficient
- use reasoning effort deliberately

Astra may consume product usage allowance faster than Sol even when it is efficient per successful task. Therefore treat Astra as a premium **workflow-completion** resource, not the default model for every hard-looking prompt.

---

# 18. Large Context

Astra has a very large context window, but large context should not replace good context management.

Prefer:
- targeted search
- concise state notes
- explicit decisions
- relevant file subsets
- structured milestones

Use Astra's large context when the task genuinely requires preserving/retrieving extensive project history or comparing a broad set of interdependent materials.

Do not indiscriminately dump an entire repository into context.

---

# 19. High-Risk Domain Override

Use at least Sol + high reasoning for important decisions involving:

- authentication
- authorization
- encryption
- secrets
- security boundaries
- payments
- transaction processing
- financial calculations
- AML
- transaction monitoring
- sanctions
- regulatory reporting
- compliance logic
- destructive database operations
- production infrastructure

Prefer Astra when the high-risk task is also a large end-to-end workflow requiring sustained tool use and verification.

Implementation can still be delegated to Terra once logic is settled.

---

# 20. Verification

Regardless of model:

- inspect relevant sources before editing
- follow repository conventions
- run tests when available
- run lint/type/build checks when relevant
- verify external facts when freshness matters
- inspect generated migrations
- inspect diffs
- distinguish assumptions from verified facts
- never fabricate command output
- never claim tests passed unless executed
- never claim files were read unless actually inspected

Astra improves capability and agentic reliability.
It does **not** remove the need for verification.

---

# 21. Safety / Authorization

Because Astra is substantially more capable at computer use and cybersecurity, respect scope boundaries strictly.

For consequential actions:
- verify authorization
- prefer reversible actions
- avoid expanding scope without user intent
- preserve backups/rollback paths when appropriate
- separate investigation from destructive execution
- require explicit confirmation when product/tool policy requires it

Model capability is not permission.

---

# 22. Availability and Fallbacks

Model availability can differ between:
- Chat
- ChatGPT Work
- Codex
- API
- account/plan
- organization policy
- rollout stage

For Codex:
- Astra availability may require a sufficiently recent Codex CLI.
- Detect availability rather than assuming it.

Fallbacks:

Astra unavailable:
- use Sol as parent for difficult reasoning
- decompose long-horizon work more aggressively
- use Terra/Luna for bounded execution

Sol unavailable:
- use Astra if available
- otherwise strongest available reasoning model

Terra unavailable:
- use Sol or Astra with appropriately low effort for normal work

Luna unavailable:
- use Terra

Never fail a task merely because the preferred tier is unavailable.

---

# 23. User Overrides

Explicit user instructions override this policy.

Examples:
- "Use Astra" → use Astra
- "Use Sol only" → remain on Sol and report limitations rather than silently switching
- "Optimize for cost" → prefer Luna/Terra and decompose
- "Use strongest model" → Astra when available
- "Use max reasoning" → max on a model that supports it
- "Do not use subagents" → work directly

---

# 24. Decision Examples

### Find where a field is calculated
Luna + low.

### Add a normal REST endpoint
Terra + medium.

### Design a new authorization model
Sol + high.

### Investigate a difficult race condition with evidence already collected
Sol + high.

### Investigate an intermittent issue spanning browser behavior, backend services, logs, cache, and infrastructure
Astra + high.

### Redesign service boundaries only
Sol + high.

### Redesign service boundaries, implement the redesign across a monorepo, migrate callers, run tests, and update docs
Astra parent + Sol/Terra/Luna subwork.

### Review AML transaction-monitoring calculation logic
Sol + high/xhigh.

### Perform an end-to-end AML model review across code, feature files, documentation, notebooks, and validation outputs
Astra parent + Sol for critical quantitative/compliance judgments.

### Update 60 repetitive fixtures
Luna + low.

### Research a framework and recommend whether to adopt it
Terra or Sol.

### Research a framework, prototype it, benchmark it, integrate it, test it, and produce migration documentation
Astra.

---

# 25. Default Rule

> **Luna handles obvious execution. Terra handles normal engineering and analysis. Sol handles hard bounded reasoning and high-risk decisions. Astra handles the hardest end-to-end workflows where sustained context, tool use, adaptation, and multi-step execution are themselves part of the problem.**
