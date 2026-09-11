# agent.md — Claude Model Routing Policy

## Purpose

Use the **smallest Claude model that can reliably complete the task**, and escalate only when task complexity, ambiguity, risk, or repeated failure justifies it.

This policy is designed for Claude-based coding/agent workflows where multiple model tiers are available.

---

## Model Tiers

### Tier 1 — Fast / Cheap
**Preferred model:** Claude Haiku 4.5  
**Alias when supported:** `haiku`  
**API model:** `claude-haiku-4-5-20251001`

Use for:
- Simple file discovery and repository navigation
- Grep/search/indexing tasks
- Straightforward summarization
- Formatting and cleanup
- Renaming variables or symbols
- Small documentation updates
- Boilerplate generation
- Simple unit tests
- Mechanical transformations
- Extracting structured information
- Reviewing logs for obvious errors
- Small isolated code changes with clear requirements

Do **not** use for:
- Architecture decisions
- Ambiguous debugging
- Security-sensitive reasoning
- Broad refactors
- Complex data/model logic
- Tasks requiring coordination across many files

---

### Tier 2 — Default / Balanced
**Preferred model:** Claude Sonnet 5  
**Alias when supported:** `sonnet`  
**API model:** `claude-sonnet-5`

This is the **default model for most real work**.

Use for:
- Feature implementation
- Multi-file code changes
- Debugging with a reasonably bounded problem
- Refactoring
- Test design
- Code review
- API design
- SQL and data engineering
- Data analysis
- Frontend/backend implementation
- CI/CD changes
- Writing technical documentation
- Reviewing pull requests
- Converting business requirements into implementation
- Investigating unfamiliar codebases
- Planning implementation work
- Moderate performance optimization
- Most agentic tool-use tasks

Default rule:

> If the task is neither obviously trivial nor clearly expert-level, use Sonnet.

---

### Tier 3 — Deep Reasoning / High Stakes
**Preferred model:** Claude Opus 5  
**Alias when supported:** `opus`  
**API model:** `claude-opus-5`

Use selectively for:
- System architecture
- Difficult root-cause analysis
- Complex or intermittent bugs
- Large cross-cutting refactors
- Complex migrations
- Security-sensitive code review
- Authentication/authorization design
- Financial or compliance-critical logic
- Complex algorithmic reasoning
- Performance problems involving several interacting systems
- Data-model redesign
- Reviewing a proposed architecture before implementation
- Resolving contradictions across requirements
- Tasks where Sonnet has already failed or remains materially uncertain
- Final review of high-impact changes

Do **not** use Opus merely because a task is large.  
Large but straightforward work should be decomposed and delegated to Sonnet/Haiku.

---

### Tier 4 — Optional Long-Horizon Expert
**Preferred model:** Claude Fable 5, **only if available in the environment**  
**API model:** `claude-fable-5`

Use only when:
- The task requires unusually long-horizon autonomous reasoning
- There are many interacting workstreams and decisions
- The problem is highly ambiguous and strategically important
- Opus cannot make reliable progress
- The expected value of additional reasoning clearly outweighs latency/cost

If Fable is unavailable, use Opus.

Never assume Fable is available in Claude Code or another harness. Detect model availability first.

---

# Routing Algorithm

Before delegating a task, classify it on five dimensions:

1. **Complexity**
   - Low: mechanical, local, obvious
   - Medium: several steps or files
   - High: architectural, deeply coupled, novel

2. **Ambiguity**
   - Low: requirements are explicit
   - Medium: some interpretation needed
   - High: requirements conflict or root cause is unknown

3. **Impact / Risk**
   - Low: reversible, cosmetic, isolated
   - Medium: normal application behavior
   - High: security, money, compliance, production availability, destructive changes

4. **Context Breadth**
   - Low: one file / one function
   - Medium: one component / several files
   - High: multiple systems, repositories, schemas, or services

5. **Reasoning History**
   - Has a lower-tier model already failed?
   - Is confidence still low after investigation?
   - Are tests contradicting the current hypothesis?

Then route:

| Situation | Model |
|---|---|
| Low complexity + low risk | Haiku |
| Mechanical subtask inside larger task | Haiku |
| Normal implementation/debugging | Sonnet |
| Multi-file or moderately ambiguous work | Sonnet |
| High ambiguity or high coupling | Opus |
| Security/compliance/financial-critical decision | Opus |
| Architecture or migration strategy | Opus |
| Sonnet fails once and root cause remains unclear | Opus |
| Exceptional long-horizon reasoning and Fable is available | Fable |

---

# Escalation Rules

Escalate **Haiku → Sonnet** when any of these occur:
- The task requires reasoning across multiple components
- The requested change is not mechanically obvious
- Tests fail for non-obvious reasons
- Requirements contain meaningful ambiguity
- The change affects public interfaces or shared contracts

Escalate **Sonnet → Opus** when any of these occur:
- One serious implementation/debugging attempt failed
- There are multiple plausible root causes with weak evidence
- The change affects architecture
- The task involves security, permissions, financial calculations, compliance, or irreversible migration
- The model cannot explain why its proposed solution should work
- A decision has a large blast radius

Escalate **Opus → Fable** only if:
- Fable is available
- The problem is genuinely long-horizon or strategically complex
- Opus is stuck or the task benefits from substantially deeper autonomous reasoning

Do not escalate merely to "be safe."

---

# De-escalation Rules

Use a cheaper model for bounded subtasks even when the parent task uses a stronger model.

Examples:
- Opus designs the architecture → Sonnet implements components
- Sonnet debugs the feature → Haiku updates comments and documentation
- Opus identifies migration stages → Sonnet writes migration scripts → Haiku checks naming/formatting
- Sonnet implements a feature → Haiku generates repetitive test fixtures

The orchestrating model remains responsible for validating delegated output.

---

# Task Decomposition

For complex work:

1. Understand the user goal.
2. Separate **decision-heavy work** from **execution-heavy work**.
3. Assign the strongest necessary model to decisions.
4. Assign cheaper models to independent mechanical execution.
5. Parallelize only independent workstreams.
6. Integrate results with the parent model.
7. Run tests or verification.
8. Escalate only if evidence shows the current tier is insufficient.

Prefer:

> Opus plans → Sonnet implements → Haiku handles mechanical follow-up

over:

> Opus does everything.

---

# Subagent Usage

Use subagents when:
- Workstreams are independent
- Tasks can run in parallel
- A task benefits from isolated context
- A specialist can return a bounded result to the parent

Avoid subagents when:
- The task is simple
- Work is sequential
- The same context must be preserved across every step
- Delegation overhead is greater than the task itself

Never spawn multiple agents to perform the same task unless intentionally using independent review.

---

# Recommended Specialist Routing

## Repository Explorer
Model: **Haiku**

Responsibilities:
- Locate files
- Search symbols
- Identify likely entry points
- Summarize folder structure
- Find usages/references

Return concise evidence. Do not redesign code.

---

## Implementer
Model: **Sonnet**

Responsibilities:
- Implement features
- Modify code
- Add tests
- Refactor bounded areas
- Run verification
- Explain material decisions

---

## Debugger
Initial model: **Sonnet**

Escalate to **Opus** when:
- Root cause remains unclear after one serious investigation
- Bug spans multiple services/components
- Behavior is nondeterministic
- Concurrency/state/caching interactions are involved

---

## Architect
Model: **Opus**

Responsibilities:
- Define architecture
- Evaluate alternatives
- Identify trade-offs
- Define boundaries/contracts
- Review migration strategy
- Identify major risks

After the decision, delegate implementation to Sonnet where possible.

---

## Reviewer
Routine review: **Sonnet**  
High-risk review: **Opus**

Use Opus for:
- Security
- Authentication/authorization
- Financial calculations
- AML/compliance logic
- Destructive migrations
- Major architectural changes

---

## Documentation Agent
Model: **Haiku** for mechanical documentation  
Model: **Sonnet** for conceptual/technical documentation

---

## Test Agent
Model: **Haiku** for repetitive test generation  
Model: **Sonnet** for test strategy and edge-case reasoning  
Model: **Opus** for adversarial/high-risk validation

---

# Coding Workflow

For normal implementation requests:

1. Use **Haiku** to locate relevant code if repository exploration is substantial.
2. Use **Sonnet** to understand and implement the change.
3. Run relevant tests, linting, and type checks.
4. If failure is non-obvious, keep Sonnet for one investigation cycle.
5. Escalate to **Opus** only if uncertainty remains.
6. Use Haiku for mechanical documentation/cleanup after correctness is established.

For trivial changes, skip orchestration and complete directly with Haiku or the current model.

---

# Architecture Workflow

For architecture/design requests:

1. Use **Opus** to clarify constraints and design the solution.
2. Ask it to explicitly identify:
   - assumptions
   - alternatives
   - trade-offs
   - failure modes
   - migration concerns
3. Once architecture is stable, break implementation into bounded tasks.
4. Route implementation tasks to **Sonnet**.
5. Route repetitive supporting tasks to **Haiku**.
6. Use **Opus** for final architecture consistency review if the change is high impact.

---

# Debugging Workflow

Start with **Sonnet**.

Require evidence:
- reproduction
- relevant logs/errors
- code path
- hypothesis
- test of hypothesis

Do not escalate simply because the first guess was wrong.

Escalate to **Opus** when:
- evidence points to several interacting causes
- debugging crosses system boundaries
- repeated local fixes fail
- the proposed fix changes architecture or core invariants

---

# Research Workflow

For lightweight repository or documentation research:
- Haiku for retrieval/extraction
- Sonnet for synthesis

For complex technical research:
- Sonnet gathers and synthesizes evidence
- Opus evaluates competing approaches when the decision is consequential

For very large research programs:
- Use Fable only if available and clearly justified

Always separate:
1. facts/evidence
2. inference
3. recommendation

---

# Cost and Latency Discipline

Model capability is a budget.

Follow these rules:
- Do not use Opus for formatting, searching, boilerplate, or obvious code edits.
- Do not use Sonnet when Haiku can complete the task reliably.
- Do not use Haiku for decisions where mistakes create expensive rework.
- Prefer decomposition over running an expensive model on a giant mixed task.
- Reuse prior findings instead of asking a new model to rediscover them.
- Never ask two expensive models to independently solve the same problem unless a second opinion is explicitly valuable.

---

# Verification

Regardless of model:
- Never treat generated code as correct merely because the model is stronger.
- Run available tests.
- Run lint/type checks when relevant.
- Inspect diffs before finalizing.
- Verify assumptions against repository code.
- Do not claim tests passed unless they were actually executed.
- Do not claim files were inspected unless they were actually read.

A stronger model reduces reasoning risk; it does not replace verification.

---

# High-Risk Changes

Use **Opus** for decision/review work involving:
- Authentication
- Authorization
- Encryption
- Secrets
- Security boundaries
- Financial calculations
- Transaction processing
- AML / financial-crime controls
- Regulatory or compliance logic
- Schema/data migrations with destructive operations
- Production infrastructure with significant blast radius

Implementation may still be delegated to Sonnet after the design is settled.

Always verify with tests and relevant domain constraints.

---

# Anti-Patterns

Do not:
- Default everything to Opus
- Route purely based on token count
- Escalate because a task "sounds important"
- Spawn agents for one-line edits
- Run multiple agents on dependent sequential tasks
- Let a subagent silently change architecture
- Accept an agent's conclusion without evidence
- Redo successful work using a stronger model
- Use outdated/retired model IDs when active alternatives exist

---

# User Overrides

Explicit user instructions override this routing policy.

Examples:
- "Use Opus for this" → use Opus
- "Optimize for cost" → prefer Haiku/Sonnet
- "Use the strongest model" → use strongest available model
- "Do not use subagents" → work directly
- "Use Sonnet only" → remain on Sonnet unless impossible, then report limitation rather than silently escalating

---

# Model Availability

Before relying on a specific model:
1. Use the model aliases exposed by the current Claude environment when possible (`haiku`, `sonnet`, `opus`).
2. If explicit API IDs are required, use currently supported IDs.
3. Do not assume optional models such as Fable are available.
4. If a preferred tier is unavailable:
   - Haiku unavailable → use Sonnet
   - Sonnet unavailable → use Opus
   - Opus unavailable → use strongest available model
   - Fable unavailable → use Opus
5. Never fail a task solely because the preferred model tier is unavailable.

---

# Decision Examples

### Example 1 — Rename a field in three files
Use: **Haiku**

Reason: bounded, mechanical change.

### Example 2 — Add a new REST endpoint
Use: **Sonnet**

Reason: normal implementation involving several files and tests.

### Example 3 — API intermittently returns stale state
Start: **Sonnet**

Escalate to Opus only if investigation reveals difficult concurrency/cache/distributed-state interactions.

### Example 4 — Redesign service boundaries
Use: **Opus** for design.

Then use Sonnet for implementation.

### Example 5 — Update 40 repetitive fixtures after a schema decision
Use: **Haiku**

The schema decision may have been made by Sonnet or Opus, but execution is mechanical.

### Example 6 — Review AML transaction-monitoring calculation logic
Use: **Opus** for reasoning/review.

Use Sonnet for bounded implementation after the logic is agreed and independently verified.

---

# Default Rule in One Sentence

> **Haiku executes obvious work, Sonnet handles normal engineering, Opus handles difficult decisions and high-risk reasoning, and Fable is reserved for exceptional long-horizon work when available.**
