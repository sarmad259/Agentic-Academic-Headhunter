from typing import TypedDict, List, Optional

class ProfessorState(TypedDict, total=False):
    """Shared state passed between all agents in the graph."""
    # Input
    professor: dict
    student_profile: dict

    # Research
    papers: List[dict]
    research_summary: str

    # Matching
    match_score: float
    overlap_areas: List[str]
    context_angle: str

    # Drafting
    draft: str
    subject: str
    draft_attempts: int

    # Review
    review_passed: bool
    review_feedback: str

    # Output
    final_draft: str
    error: Optional[str]
