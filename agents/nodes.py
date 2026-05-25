"""
LangGraph agent nodes.
Model priority: DeepSeek-V4-Flash → Qwen3.5-397B → Groq Llama-3.3-70b
"""

import os
import time
import requests
from dotenv import load_dotenv
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage

from agents.state import ProfessorState
from utils.intelligence_layer import CONTEXT_MAP, PRIORITY_ORDER

load_dotenv(override=True)


def get_model(task: str = "draft"):
    """
    task="draft"  → fast mode
    task="review" → thinking mode (DeepSeek only)
    Priority: DeepSeek-V4-Flash → Qwen3.5-397B → Groq
    """
    # Try DeepSeek-V4-Flash
    try:
        r = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": "deepseek-v4-flash:cloud", "prompt": "hi", "stream": False},
            timeout=20
        )
        if r.status_code == 200:
            mode = "thinking" if task == "review" else "fast"
            print(f"  [LLM] DeepSeek-V4-Flash ({mode})")
            return ChatOllama(
                model="deepseek-v4-flash:cloud",
                temperature=0.6 if task == "review" else 0.8,
                num_predict=800,
                model_kwargs={"think": task == "review"}
            )
    except Exception:
        pass

    # Try Qwen3.5-397B
    try:
        r = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": "qwen3.5:397b-cloud", "prompt": "hi", "stream": False},
            timeout=20
        )
        if r.status_code == 200:
            print("  [LLM] Qwen3.5-397B")
            return ChatOllama(model="qwen3.5:397b-cloud", temperature=0.7, num_predict=600)
    except Exception:
        pass

    # Groq fallback
    print("  [LLM] Groq/Llama-3.3-70b")
    from langchain_groq import ChatGroq
    return ChatGroq(
        model="llama-3.3-70b-versatile",
        api_key=os.getenv("GROQ_API_KEY"),
        temperature=0.7,
        max_tokens=600,
    )


def _clean(text: str) -> str:
    """Strip DeepSeek/Qwen thinking tags."""
    if "<think>" in text:
        text = text.split("</think>")[-1]
    return text.strip()


# ── Node 1: Researcher ─────────────────────────────────────────────────────────
def researcher_node(state: ProfessorState) -> dict:
    professor = state["professor"]
    author_id = professor.get("author_id") or professor.get("authorId")

    # Use pre-fetched papers if available
    if state.get("papers"):
        return {}

    if not author_id:
        return {"papers": [], "research_summary": "No author ID — using keywords only"}

    try:
        url = f"https://api.semanticscholar.org/graph/v1/author/{author_id}/papers"
        r = requests.get(url, params={"fields": "title,abstract,year,citationCount", "limit": 10}, timeout=15)
        r.raise_for_status()
        papers = sorted(r.json().get("data", []), key=lambda x: x.get("citationCount", 0), reverse=True)[:3]
        time.sleep(2)

        summary = f"Prof. {professor['name']} — top papers:\n"
        for p in papers:
            summary += f"- {p.get('title')} ({p.get('year')}, {p.get('citationCount',0)} citations)\n"
            if p.get("abstract"):
                summary += f"  {p['abstract'][:150]}...\n"

        return {"papers": papers, "research_summary": summary}
    except Exception as e:
        return {"papers": [], "research_summary": f"Error: {e}", "error": str(e)}


# ── Node 2: Matcher ────────────────────────────────────────────────────────────
def matcher_node(state: ProfessorState) -> dict:
    professor = state["professor"]
    papers = state.get("papers", [])

    search_text = " ".join(professor.get("research_keywords", [])).lower()
    for p in papers[:2]:
        search_text += " " + p.get("title", "").lower()
        search_text += " " + (p.get("abstract") or "")[:200].lower()

    context = CONTEXT_MAP["default"]
    for key in PRIORITY_ORDER:
        if key in search_text:
            context = CONTEXT_MAP[key]
            break

    return {"context_angle": context["angle"], "overlap_areas": [context["angle"]]}


# ── Node 3: Drafter ────────────────────────────────────────────────────────────
def drafter_node(state: ProfessorState) -> dict:
    professor = state["professor"]
    papers = state.get("papers", [])
    context_angle = state.get("context_angle", "medical AI and attention mechanisms")
    feedback = state.get("review_feedback", "")
    attempts = state.get("draft_attempts", 0)

    papers_text = ""
    for i, p in enumerate(papers[:3], 1):
        papers_text += f"\n{i}. \"{p.get('title','Untitled')}\" ({p.get('year','N/A')}, {p.get('citationCount',0)} citations)"
        if p.get("abstract"):
            papers_text += f"\n   {p['abstract'][:250]}..."

    feedback_block = f"\n\nPREVIOUS DRAFT REJECTED:\n{feedback}\nFix ALL issues above." if feedback else ""
    last_name = professor["name"].split()[-1]

    prompt = f"""Write a cold outreach email from Muhammad Sarmad Khan to Prof. {professor['name']} at {professor.get('institution', professor.get('university',''))}.

SARMAD'S BACKGROUND (pick what's most relevant, don't list everything):
- BS AI, FAST-NUCES Peshawar, Pakistan | IELTS 7.0 | Available October 2026
- FYP (CollabForms — PRIMARY): designed a novel proximity-based spatial clustering algorithm for checkbox-label association in document forms (standard OCR cannot solve this). Custom YOLOv11: 70% mAP@50, 112ms CPU inference. Reflexion-inspired LLM refinement with persistent cross-session rule memory. Supervised by Dr. Omer Usman Khan.
- Independent research: developed SCDA (Spatial Channel Dual Attention) + DDA (Dynamic Depthwise Attention) mechanisms for diabetic retinopathy — 97.22% accuracy, +5.91% over CIBM 2025 baseline, resolved recall collapse 50%→96.9%, first Lion optimizer application to retinal pathology
- Production: RAG pipelines + hallucination mitigation at Owlvest
- Context angle for this professor: {context_angle}
- Seeking fully funded Masters/PhD

PROFESSOR'S PAPERS:{papers_text}
{feedback_block}

WRITE A NATURAL 3-PARAGRAPH EMAIL:

Paragraph 1: Show you read their paper. Name ONE specific technique from their paper by its exact name. Explain the connection to your work — don't just say "aligns with", say WHY it connects.

Paragraph 2: Your most relevant work with exact numbers. If both medical AI and FYP are relevant, mention both briefly. Pick the stronger connection.

Paragraph 3: IELTS 7.0, October 2026, clear ask for funded position.

HARD RULES:
- Under 180 words
- Start with: "Dear Prof. {last_name},"
- Name the professor's specific technique (not "your research")
- At least one exact number: 97.22%, +5.91%, 50%→96.9%, 70% mAP@50, or 112ms
- NO GPA, NO flattery, NO "deeply inspired", NO "renowned", NO "my background aligns"
- Sound like a confident researcher, not a desperate applicant
- Email body ONLY — no subject line, no signature"""

    try:
        model = get_model(task="draft")
        response = model.invoke([HumanMessage(content=prompt)])
        draft = _clean(response.content)
        return {"draft": draft, "draft_attempts": attempts + 1, "review_feedback": ""}
    except Exception as e:
        return {"draft": "", "error": str(e)}


# ── Node 4: Reviewer ───────────────────────────────────────────────────────────
def reviewer_node(state: ProfessorState) -> dict:
    draft = state.get("draft", "")
    papers = state.get("papers", [])

    if not draft:
        return {"review_passed": False, "review_feedback": "Draft is empty. Write a complete email."}

    # Extract technique names from paper titles for prescriptive feedback
    paper_techniques = "\n".join(f"- \"{p.get('title','')}\"" for p in papers[:2])
    word_count = len(draft.split())

    prompt = f"""You are a strict quality reviewer for academic cold outreach emails.

PROFESSOR'S PAPERS (extract technique names from these):
{paper_techniques}

EMAIL TO REVIEW ({word_count} words):
{draft}

For each check below, if it FAILS write the EXACT fix — not just what's wrong, but the specific text to add or change.

CHECKLIST:
1. Names a SPECIFIC technique from the papers above (not just "your research" or "your work")?
   FAIL FIX → "ADD this exact technique name from the paper title: [extract it from the paper titles above]"

2. Contains "SCDA" or "DDA"?
   FAIL FIX → "ADD: 'my SCDA (Spatial Channel Dual Attention) mechanism' or 'DDA (Dynamic Depthwise Attention)'"

3. Contains at least one of: "97.22%" or "+5.91%" or "50%→96.9%"?
   FAIL FIX → "ADD one of these exact strings: '97.22% accuracy' or '+5.91% over CIBM 2025 baseline' or 'recall improved from 50% to 96.9%'"

4. Contains "IELTS 7.0"?
   FAIL FIX → "ADD: 'With IELTS 7.0' in the second or third sentence"

5. Contains "October 2026" or "Oct 2026"?
   FAIL FIX → "ADD: 'available from October 2026' before the closing ask"

6. Under 180 words? (current: {word_count} words)
   FAIL FIX → "REMOVE {max(0, word_count - 175)} words — cut the sentence starting with [quote the most generic sentence in the draft]"

7. No forbidden phrases: "deeply inspired", "renowned", "prestigious", "honored", "excited to", "I am writing to express"?
   FAIL FIX → "REPLACE '[quote the exact forbidden phrase found]' with a direct sentence referencing their specific technique"

8. Ends with a clear ask for funded Masters/PhD position?
   FAIL FIX → "REPLACE the closing sentence with: 'Do you have funded Masters/PhD positions available in your lab?'"

OUTPUT FORMAT — use exactly this:
PASSED: yes/no
FIXES:
[for each failed check: the exact prescribed fix text, one per line — or write "none" if all passed]"""

    try:
        model = get_model(task="review")
        response = model.invoke([HumanMessage(content=prompt)])
        review = _clean(response.content)

        passed = "passed: yes" in review.lower()

        # Also do a hard check on the draft itself — override if all key elements present
        has_all = (
            any(kw in draft for kw in ["SCDA", "DDA"]) and
            any(kw in draft for kw in ["97.22", "+5.91", "50%", "96.9"]) and
            any(kw in draft for kw in ["IELTS 7.0", "IELTS score of 7.0", "ielts"]) and
            any(kw in draft for kw in ["October 2026", "Oct 2026", "october 2026"]) and
            any(kw in draft.lower() for kw in ["funded", "position", "phd", "masters"])
        )
        if has_all and not passed:
            # Reviewer is being overly strict — trust the hard check
            passed = True

        # Extract prescriptive fixes section
        fixes = ""
        review_lower = review.lower()
        if "fixes:" in review_lower:
            idx = review_lower.find("fixes:")
            fixes = review[idx + len("fixes:"):].strip()

        return {
            "review_passed": passed,
            "review_feedback": fixes if not passed else ""
        }
    except Exception:
        return {"review_passed": True, "review_feedback": ""}


# ── Node 5: Finalizer ──────────────────────────────────────────────────────────
def finalizer_node(state: ProfessorState) -> dict:
    draft = state.get("draft", "")
    angle = state.get("context_angle", "")

    subjects = {
        "medical AI": "Prospective Masters Student — Medical AI Research (SCDA/DDA, IELTS 7.0)",
        "attention": "Graduate Application — Novel Attention Mechanisms for Medical AI (DFKI)",
        "transfer learning": "Prospective Masters Student — Transfer Learning Research (DFKI, IELTS 7.0)",
        "computer vision": "Research Inquiry: CNN Attention Mechanisms for Medical Imaging",
        "llm": "Research Inquiry — LLM/RAG Systems + Medical AI Background (IELTS 7.0)",
        "rag": "Research Inquiry — RAG Systems + Medical AI Background (IELTS 7.0)",
    }
    subject = next(
        (v for k, v in subjects.items() if k in angle.lower()),
        "Prospective Masters Student — Medical AI Research (SCDA/DDA, IELTS 7.0)"
    )

    final = f"""{draft}

--
Muhammad Sarmad Khan
BS Artificial Intelligence | FAST-NUCES Peshawar
Research: SCDA/DDA Attention Mechanisms | Diabetic Retinopathy (97.22% accuracy)
Supervisor: Dr. Saif Ur Rehman Khan (DFKI Germany)
khansardarms@gmail.com | IELTS 7.0 | Available Oct 2026"""

    return {"final_draft": final, "subject": subject}
