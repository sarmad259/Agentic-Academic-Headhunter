"""
CrewAI Tasks — sequential pipeline, each feeds into the next.
"""

from crewai import Task

SARMAD_FULL_PROFILE = """SARMAD'S COMPLETE PROFILE:
Primary Novel Work — CollabForms FYP (supervised by Dr. Omer Usman Khan, FAST-NUCES):
  - Novel proximity-based spatial clustering algorithm for checkbox-label association
    (solves a fundamental problem standard OCR pipelines cannot address)
  - Custom YOLOv11 model on real NUCES forms: 70% mAP@50, 112ms inference on CPU
  - Reflexion-inspired LLM refinement loop with persistent cross-session rule memory
    (extends Reflexion beyond single-task episodic to cross-task transfer learning)
  - Full-stack: Django, React, PostgreSQL, Docker, ONNX runtime

Independent Research — Diabetic Retinopathy Detection:
  - Developed SCDA (Spatial Channel Dual Attention) mechanism — novel
  - Developed DDA (Dynamic Depthwise Attention) mechanism — novel
  - First application of Lion optimizer to retinal pathology
  - Results: 97.22% accuracy, +5.91% over CIBM 2025 baseline
  - Resolved Type 1 diabetes recall collapse: 50% → 96.9%

Production AI (Owlvest):
  - RAG pipelines + hallucination mitigation for LLM inference systems

IELTS 7.0 | Available October 2026+ | Seeking fully funded Masters/PhD"""


def make_tasks(researcher, matcher, drafter, reviewer, professor: dict, papers: list):
    name = professor.get("name", "Unknown")
    last_name = name.split()[-1]
    institution = professor.get("institution") or professor.get("university", "")
    keywords = ", ".join(professor.get("research_keywords", []))

    papers_text = ""
    for i, p in enumerate(papers[:3], 1):
        papers_text += f"\n{i}. \"{p.get('title','Untitled')}\" ({p.get('year','N/A')}, {p.get('citationCount',0)} citations)"
        if p.get("abstract"):
            papers_text += f"\n   {p['abstract'][:300]}..."

    # ── Task 1: Research ──────────────────────────────────────────────────────
    research_task = Task(
        description=f"""Analyze the research profile of Professor {name} at {institution}.

Research keywords: {keywords}

Recent papers:{papers_text}

Extract SPECIFICALLY:
1. Primary research focus (1-2 sentences, be precise)
2. The EXACT name of the most specific technique/method from their most cited paper
3. What makes this technique novel (1 sentence)
4. How their research direction is evolving

You MUST name the exact technique — not just "attention mechanism" but the specific variant.""",
        expected_output=(
            "Structured summary: primary focus, EXACT technique name, novelty, research direction. "
            "Max 150 words. Must include the specific technique name."
        ),
        agent=researcher,
    )

    # ── Task 2: Match ─────────────────────────────────────────────────────────
    match_task = Task(
        description=f"""Find the strongest, most specific connection between Prof. {name}'s research and Sarmad Khan's work.

{SARMAD_FULL_PROFILE}

Use the research summary from Task 1.
Find: which of Sarmad's work (Research 1 OR Research 2 OR Production) best connects to the professor's specific technique.
Be precise — name both the professor's technique AND Sarmad's corresponding contribution.
Choose the most compelling angle — don't always default to the medical imaging work if the FYP is a better fit.""",
        expected_output=(
            "2-3 sentences: professor's technique name + Sarmad's corresponding work + "
            "why they connect. Must be specific, not generic."
        ),
        agent=matcher,
        context=[research_task],
    )

    # ── Task 3: Draft ─────────────────────────────────────────────────────────
    draft_task = Task(
        description=f"""Write a cold outreach email from Sarmad Khan to Professor {name} at {institution}.

Use the research summary (Task 1) and matching analysis (Task 2).

{SARMAD_FULL_PROFILE}

Write it like a real person — not a template. Three natural paragraphs:

Paragraph 1: Show you read their paper. Name ONE specific technique from Task 1 by its exact name. Connect it to a specific problem Sarmad has worked on — explain the connection, don't just say "aligns with".

Paragraph 2: Introduce Sarmad's most relevant work. Use exact numbers. If both the medical AI work AND the FYP are relevant, mention both briefly. If only one fits, use that one. Don't list everything.

Paragraph 3: IELTS 7.0, October 2026, clear ask for funded position.

MANDATORY — ALL must be present:
- Start with EXACTLY: "Dear Prof. {last_name},"
- Professor's specific technique named (from Task 1)
- At least ONE exact number: 97.22%, +5.91%, 50%→96.9%, 70% mAP@50, or 112ms
- "IELTS 7.0"
- "October 2026"
- "Do you have funded Masters/PhD positions available?"
- Under 180 words

FORBIDDEN: GPA, "deeply inspired", "renowned", "prestigious", "honored", "excited to",
"my background aligns", "I am writing to express", generic filler phrases
Email body ONLY — no subject line, no signature""",
        expected_output=(
            f"Natural 3-paragraph email starting with 'Dear Prof. {last_name},', under 180 words, "
            "with professor's specific technique, Sarmad's work with exact numbers, IELTS 7.0, October 2026, funding ask."
        ),
        agent=drafter,
        context=[research_task, match_task],
    )

    # ── Task 4: Review + Self-Fix ─────────────────────────────────────────────
    review_task = Task(
        description=f"""Review the email draft for Professor {name} against this EXACT checklist.
Count the words carefully.

CHECKLIST (all 8 must pass):
1. Names a SPECIFIC technique from their paper (not just "your research" or "your work")?
   FAIL FIX → ADD this exact technique name from their paper title (from Task 1 research summary)

2. Contains "SCDA" or "DDA" or "CollabForms" or "spatial clustering" or "YOLOv11"?
   FAIL FIX → ADD one of Sarmad's specific contributions by name

3. Contains at least one exact number: "97.22%" or "+5.91%" or "50%→96.9%" or "70% mAP" or "112ms"?
   FAIL FIX → ADD one of these exact strings

4. Contains "IELTS 7.0"?
   FAIL FIX → ADD: 'IELTS 7.0' in the second or third sentence

5. Contains "October 2026" or "Oct 2026"?
   FAIL FIX → ADD: 'available from October 2026' before the closing ask

6. Under 180 words?
   FAIL FIX → REMOVE the most generic sentence in the draft

7. No forbidden phrases: "deeply inspired", "renowned", "prestigious", "honored", "excited to", "I am writing to express"?
   FAIL FIX → REPLACE the forbidden phrase with a direct sentence referencing their specific technique

8. Ends with a clear ask for funded Masters/PhD position?
   FAIL FIX → REPLACE closing sentence with: 'Do you have funded Masters/PhD positions available in your lab?'

DECISION:
- If ALL 8 pass → output: "APPROVED: [exact email text as-is]"
- If ANY fail → apply ALL the prescribed fixes yourself and output: "REVISED: [complete rewritten email]"

You MUST output a complete email — either APPROVED or REVISED. No partial feedback.""",
        expected_output=(
            "'APPROVED: [complete email body]' or 'REVISED: [complete improved email body]'. "
            "The email must pass all 8 checklist items."
        ),
        agent=reviewer,
        context=[research_task, match_task, draft_task],
    )

    return research_task, match_task, draft_task, review_task
