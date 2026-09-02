---
name: presentation-script
description: Read PowerPoint (.pptx) presentations and create consultant-grade talking scripts, speaker notes, transitions, and presentation coaching grounded in each slide's actual content. Use when the user asks to prepare, rehearse, present, create talking points, write speaker notes, or improve delivery for a PowerPoint deck.
icon: presentation
color: blue
---

# Presentation Script

Create world-class presentation scripts from `.pptx` files while remaining faithful to the deck.

The goal is **not to read the slide aloud**. The goal is to help the presenter communicate the slide's message clearly, confidently, memorably, and with an executive/consulting style.

## Core principles

1. **Ground everything in the slide.**
   - Never invent facts, numbers, decisions, dates, causes, or recommendations.
   - Clearly separate:
     - **Slide fact** — explicitly shown in the deck.
     - **Reasonable interpretation** — directly inferable from the slide.
     - **Presenter enrichment** — framing, analogy, implication, or example that does not claim to be a slide fact.
   - If a slide is ambiguous, say what is ambiguous rather than silently resolving it.

2. **Answer first.**
   - Open each slide with its main takeaway, not with a description of the visual.
   - Prefer: “The key message here is…”
   - Avoid: “On this slide you can see…”

3. **Use a consultant storyline.**
   Each slide should normally follow:
   - **Headline / answer**
   - **Evidence**
   - **Implication / so what**
   - **Transition**

4. **Do not narrate every bullet.**
   - Group details into 2–4 meaningful messages.
   - Prioritize what the audience needs to understand, decide, remember, or do.

5. **Make the script sound spoken.**
   - Short sentences.
   - Natural transitions.
   - Strategic repetition.
   - Minimal jargon unless the audience expects it.
   - Do not write essay prose.

6. **Preserve nuance.**
   - Do not exaggerate a slide's conclusion.
   - Use calibrated language:
     - “indicates”, “suggests”, “appears to”, “is consistent with”
     - rather than “proves” unless the slide truly establishes proof.

## Workflow

### Step 1 — Inspect the deck

If a `.pptx` file is available, run:

```bash
python .cursor/skills/presentation-script/scripts/extract_pptx.py "<deck.pptx>" --out "<deck>_extracted.md"
```

If visual interpretation matters and the environment supports LibreOffice/Poppler, use:

```bash
python .cursor/skills/presentation-script/scripts/extract_pptx.py "<deck.pptx>" --out "<deck>_extracted.md" --render
```

Read the extracted markdown and, when rendered slide images are available, inspect those images as well.

Do not rely only on extracted text when:
- positioning or relative size carries meaning;
- the slide contains a chart, process diagram, architecture, heatmap, or visual framework;
- the slide is image-heavy;
- callouts, arrows, emphasis, or grouping materially affect interpretation.

### Step 2 — Build the deck storyline

Before writing individual scripts, identify:

- **Audience** — executives, management, clients, technical specialists, team members, mixed.
- **Objective** — inform, align, persuade, recommend, decide, teach, inspire.
- **Core question** — what question is this deck trying to answer?
- **Governing thought** — the single overall message the audience should leave with.
- **Story arc** — e.g. Context → Problem → Evidence → Options → Recommendation → Action.
- **Decision slides** — slides that require particular emphasis.
- **Appendix/reference slides** — slides that may need only short scripts.

If the audience or objective is not stated, infer conservatively from the deck and label the assumption.

### Step 3 — Diagnose each slide

For each slide, determine:

1. **Role in story**
   - Context
   - Problem
   - Evidence
   - Insight
   - Recommendation
   - Decision
   - Implementation
   - Summary
   - Appendix

2. **One-sentence takeaway**
   - Complete this sentence:
     **“If the audience remembers only one thing from this slide, it should be…”**

3. **Evidence hierarchy**
   - What 1–3 pieces of evidence matter most?
   - Which details can be skipped verbally?

4. **So what**
   - Why does this matter?
   - What decision, risk, implication, or next step follows?

5. **Connection**
   - How does this slide follow the previous one?
   - How does it set up the next one?

### Step 4 — Write the speaker script

Use this default structure:

#### A. Bridge from previous slide — 1 sentence
Explain why the audience is moving here.

#### B. Answer-first headline — 1–2 sentences
State the message immediately.

#### C. Explain the evidence — 2–4 short points
Interpret rather than repeat.

Useful signposting:
- “There are three things to take away.”
- “Two points matter here.”
- “The difference is driven by…”
- “What matters most is…”

#### D. So what — 1–2 sentences
Translate analysis into meaning.

Useful phrasing:
- “What this means for us is…”
- “The implication is…”
- “This matters because…”
- “The decision this points to is…”

#### E. Memorable anchor — optional
Where helpful, use:
- a concise phrase;
- an analogy;
- a contrast;
- a concrete example.

Keep it accurate and subordinate to the evidence.

#### F. Transition — 1 sentence
Create forward momentum:
- “That tells us what the issue is; the next question is what we should do about it.”
- “With the size of the opportunity established, the next slide looks at where to focus first.”

### Step 5 — Adapt to audience

#### Executive / senior management
Emphasize:
- answer;
- financial/business impact;
- risk;
- trade-offs;
- decision;
- ownership;
- next step.

Compress technical detail unless it changes the decision.

#### Client / consulting steering committee
Emphasize:
- shared problem;
- evidence;
- options;
- recommendation;
- rationale;
- implications;
- decisions required.

Sound collaborative, not adversarial.

#### Technical audience
Emphasize:
- method;
- assumptions;
- evidence;
- limitations;
- mechanisms;
- validation.

Do not hide uncertainty.

#### Team / internal leadership
Emphasize:
- purpose;
- priorities;
- roles;
- confidence;
- what changes;
- what stays the same;
- action.

Where appropriate, use positive remarks, relatable examples, and confidence-building language.

### Step 6 — Calibrate duration

Use these guidelines unless the user specifies timing:

- **Title / section divider:** 10–20 sec
- **Simple message slide:** 30–45 sec
- **Standard content slide:** 45–75 sec
- **Complex analysis / chart:** 60–120 sec
- **Decision / recommendation slide:** 60–90 sec
- **Appendix:** 15–45 sec, only if presented

Estimate speech at roughly 125–150 words per minute.

Do not fill time merely because it is available.

## Script quality rules

### Do
- Start with the conclusion.
- Use explicit signposting.
- Explain “why this matters.”
- Translate numbers into meaning.
- Highlight comparison, movement, concentration, outliers, and trade-offs.
- Use pauses around the most important sentence.
- Vary sentence length.
- End slides with momentum.

### Do not
- Say “as you can see” repeatedly.
- Read every bullet.
- Start every slide with “This slide shows…”
- Add unsupported statistics.
- Describe chart axes before giving the insight.
- Use bloated consultant jargon.
- Overuse “essentially”, “obviously”, “clearly”, or “very”.
- Treat correlation as causation.
- Claim certainty the deck does not establish.

## Working with charts

For charts, speak in this sequence:

1. **Insight first** — what pattern matters?
2. **Evidence** — which values or comparisons support it?
3. **Interpretation** — what might explain it, only if supported.
4. **Implication** — what does it mean for the audience?

Example pattern:

> “The key point is that growth is concentrated in Segment A rather than broad-based. Segment A contributes roughly two-thirds of the increase, while the other segments are broadly flat. That means our near-term result is disproportionately dependent on one segment, which is the risk we need to manage.”

Do not verbalize every data point.

## Working with tables

Never read a table row by row unless specifically required.

Instead:
- state the question the table answers;
- identify 1–3 patterns;
- call out exceptions;
- explain implication.

## Working with process / architecture slides

Use:
- **Purpose** — what is the process/system meant to achieve?
- **Flow** — 3–5 major stages, not every box.
- **Critical point** — where value, risk, or control concentrates.
- **Implication** — what the audience should understand or decide.

## Working with recommendation slides

Use a strong recommendation structure:

1. **Recommendation**
2. **Why now**
3. **2–3 reasons**
4. **Trade-off / risk**
5. **Action requested**

Never bury the ask.

## Working with leadership / inspirational slides

Use:
- shared purpose;
- a concrete example or story;
- positive framing;
- confidence in the audience/team;
- clear action.

A short story should normally have:
- beginning / situation;
- middle / challenge;
- end / resolution and lesson.

Use authenticity rather than manufactured drama.

## Output modes

When the user does not specify a format, provide **Detailed Script**.

### Mode 1 — Detailed Script

For every slide:

```markdown
## Slide 7 — [Slide title]

**Role in storyline:** Evidence  
**Core message:** [one sentence]  
**Target time:** 60 sec

### Talk track
[spoken script]

### Delivery cues
- Emphasize: “...”
- Pause after: “...”
- Do not spend time on: ...

### Transition
“...”
```

### Mode 2 — Presenter Notes

Shorter notes suitable for PowerPoint Notes:

```markdown
### Slide 7
- HEADLINE:
- EVIDENCE:
- SO WHAT:
- TRANSITION:
```

### Mode 3 — Executive Script

Maximum compression:
- 20–45 seconds per slide;
- answer first;
- one proof point;
- implication;
- transition.

### Mode 4 — Rehearsal Coach

After drafting the scripts, provide:
- likely difficult slides;
- likely audience questions;
- where to pause;
- phrases to simplify;
- slides likely to run long;
- 5–10 challenge questions for rehearsal.

## Deck-level quality check

Before finalizing, verify:

- [ ] Can the whole deck be summarized in one sentence?
- [ ] Does each slide have exactly one dominant message?
- [ ] Does every slide advance the storyline?
- [ ] Are facts distinguished from interpretation?
- [ ] Does every analytical slide contain a “so what”?
- [ ] Are decision asks explicit?
- [ ] Are transitions natural?
- [ ] Does the script sound spoken rather than written?
- [ ] Is technical detail appropriate for the audience?
- [ ] Are unsupported claims removed?
- [ ] Are repeated messages intentional?
- [ ] Does timing fit the requested presentation length?

## Handling gaps

If the deck does not provide enough evidence for an intended claim:
- state the limitation;
- create a safe verbal bridge;
- optionally suggest what evidence would strengthen the slide;
- do not invent the missing content.

Example:

> “The slide establishes that alert volumes increased, but it does not show the cause. Present this as an observed trend rather than attributing it to the rule change.”

## User request patterns

Examples:

- `/presentation-script deck.pptx`
- `/presentation-script deck.pptx -- audience: executives -- total time: 15 min`
- `Use /presentation-script and give me speaker notes for slides 4–12.`
- `Use /presentation-script to prepare me for a steering committee presentation.`
- `Use /presentation-script to rewrite my existing speaker notes and add transitions.`
- `Use /presentation-script in rehearsal-coach mode and challenge me with likely questions.`

## Reference material

Consult `references/consulting-presentation-playbook.md` for additional patterns, quality standards, and reusable phrasing.
