"""
Runner: processes all professors through the LangGraph pipeline.
Drop-in replacement for IntelligenceLayer.generate_all_drafts()
"""

from typing import List, Dict
from agents.graph import get_graph
from agents.state import ProfessorState


def run_pipeline_for_professor(professor: dict, papers: list, student_profile: dict) -> Dict:
    """Run the full LangGraph pipeline for a single professor."""
    graph = get_graph()

    initial_state: ProfessorState = {
        "professor": professor,
        "student_profile": student_profile,
        "papers": papers,
        "research_summary": "",
        "match_score": professor.get("match_score", 0),
        "overlap_areas": professor.get("overlap_areas", []),
        "context_angle": "",
        "draft": "",
        "subject": "",
        "draft_attempts": 0,
        "review_passed": False,
        "review_feedback": "",
        "final_draft": "",
        "error": None,
    }

    try:
        result = graph.invoke(initial_state)
        draft = result.get("final_draft") or result.get("draft", "")
        return {
            "professor": professor,
            "papers_referenced": result.get("papers", []),
            "draft": draft,
            "subject": result.get("subject", "Prospective Masters Student — Medical AI Research (SCDA/DDA, IELTS 7.0)"),
            "context_used": result.get("context_angle", ""),
            "review_passed": result.get("review_passed", False),
            "draft_attempts": result.get("draft_attempts", 0),
            "error": result.get("error"),
        }
    except Exception as e:
        return {
            "professor": professor,
            "draft": None,
            "error": str(e),
        }


def run_pipeline_for_all(research_results: List[Dict], student_profile: Dict) -> List[Dict]:
    """Run LangGraph pipeline for all professors."""
    results = []
    total = len([r for r in research_results if r.get("papers")])
    done = 0

    for result in research_results:
        professor = result["professor"]
        papers = result.get("papers", [])

        if not papers:
            print(f"  Skipping {professor['name']} — no papers found")
            continue

        done += 1
        print(f"\n[{done}/{total}] Processing {professor['name']}...")

        output = run_pipeline_for_professor(professor, papers, student_profile)

        attempts = output.get("draft_attempts", 1)
        passed = "✓" if output.get("review_passed") else "~"
        angle = output.get("context_used", "default")
        print(f"  {passed} Done — angle: [{angle}] — attempts: {attempts}")

        results.append(output)

    return results
