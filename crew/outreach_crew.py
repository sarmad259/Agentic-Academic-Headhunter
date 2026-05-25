"""
CrewAI Crew — orchestrates all agents for one professor.
"""

from crewai import Crew, Process
from crew.agents import make_agents
from crew.tasks import make_tasks


def run_crew_for_professor(professor: dict, papers: list) -> dict:
    """Run the full CrewAI pipeline for a single professor."""

    researcher, matcher, drafter, reviewer = make_agents()
    research_task, match_task, draft_task, review_task = make_tasks(
        researcher, matcher, drafter, reviewer, professor, papers
    )

    crew = Crew(
        agents=[researcher, matcher, drafter, reviewer],
        tasks=[research_task, match_task, draft_task, review_task],
        process=Process.sequential,  # Each task feeds into the next
        verbose=True,
    )

    try:
        result = crew.kickoff()
        raw_output = str(result.raw) if hasattr(result, "raw") else str(result)

        # Parse approved/revised
        if raw_output.startswith("APPROVED:"):
            draft = raw_output[len("APPROVED:"):].strip()
            status = "approved"
        elif raw_output.startswith("REVISED:"):
            draft = raw_output[len("REVISED:"):].strip()
            status = "revised"
        else:
            draft = raw_output.strip()
            status = "unknown"

        # Add signature
        final = f"""{draft}

--
Muhammad Sarmad Khan
BS Artificial Intelligence | FAST-NUCES Peshawar
Research: SCDA/DDA Attention Mechanisms | Diabetic Retinopathy (97.22% accuracy)
Supervisor: Dr. Saif Ur Rehman Khan (DFKI Germany)
khansardarms@gmail.com | IELTS 7.0 | Available Oct 2026"""

        return {
            "professor": professor,
            "papers_referenced": papers,
            "draft": final,
            "subject": _pick_subject(professor),
            "status": status,
            "error": None,
        }

    except Exception as e:
        return {
            "professor": professor,
            "draft": None,
            "error": str(e),
        }


def run_crew_for_all(research_results: list) -> list:
    """Run CrewAI pipeline for all professors."""
    results = []
    valid = [r for r in research_results if r.get("papers")]
    total = len(valid)

    for i, result in enumerate(valid, 1):
        professor = result["professor"]
        papers = result.get("papers", [])
        print(f"\n{'='*60}")
        print(f"[{i}/{total}] Running crew for {professor['name']}")
        print(f"{'='*60}")

        output = run_crew_for_professor(professor, papers)
        status = output.get("status", "error")
        print(f"  → Status: {status}")
        results.append(output)

    return results


def _pick_subject(professor: dict) -> str:
    keywords = " ".join(professor.get("research_keywords", [])).lower()
    if any(k in keywords for k in ["medical", "retina", "imaging", "diabetic"]):
        return "Prospective Masters Student — Medical AI Research (SCDA/DDA, IELTS 7.0)"
    if any(k in keywords for k in ["attention", "vision", "cnn"]):
        return "Graduate Application — Novel Attention Mechanisms for Medical AI"
    if any(k in keywords for k in ["llm", "rag", "nlp", "language"]):
        return "Research Inquiry — LLM/RAG Systems + Medical AI Background (IELTS 7.0)"
    return "Prospective Masters Student — AI Research Experience (DFKI, IELTS 7.0)"
