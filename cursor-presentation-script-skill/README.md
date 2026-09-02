# Cursor Presentation Script Skill

A reusable Cursor Agent Skill for turning PowerPoint decks into consultant-grade presentation scripts.

## Install

Copy this folder into your project so the final path is:

```text
.cursor/
  skills/
    presentation-script/
      SKILL.md
      scripts/
        extract_pptx.py
      references/
        consulting-presentation-playbook.md
```

Cursor automatically discovers project skills from `.cursor/skills/`.

## Dependency

The extraction script requires:

```bash
pip install python-pptx
```

Optional visual rendering requires:
- LibreOffice (`soffice`)
- Poppler (`pdftoppm`)

The skill still works without rendering, but complex diagrams and visual charts should be inspected visually when possible.

## Use

In Cursor Agent chat:

```text
/presentation-script MyDeck.pptx
```

Or:

```text
Use /presentation-script on MyDeck.pptx.
Audience: executive leadership.
Objective: secure approval.
Presentation time: 15 minutes.
Give me detailed scripts plus likely Q&A.
```

Other useful prompts:

```text
Use /presentation-script for slides 4-10 only.
```

```text
Use /presentation-script in executive-script mode.
```

```text
Use /presentation-script in rehearsal-coach mode and challenge me slide by slide.
```

```text
Use /presentation-script to create PowerPoint-ready speaker notes.
```

## Recommended workflow

1. Put the `.pptx` in the Cursor workspace.
2. Invoke `/presentation-script`.
3. Cursor runs the extraction helper.
4. It identifies the deck storyline before scripting individual slides.
5. It generates answer-first scripts grounded in slide content.
6. Ask for rehearsal mode to practice likely questions.

## Design choices

The skill is deliberately strict about source grounding. It separates slide facts from interpretation and prevents the Agent from inventing missing evidence.

The default presentation pattern is:

```text
Bridge → Answer → Evidence → So what → Memorable anchor → Transition
```

This is more useful than simply paraphrasing slide bullets.
