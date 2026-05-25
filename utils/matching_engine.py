from typing import Dict, List

# Sarmad's full profile for matching
SARMAD_PROFILE = {
    "interests": [
        "medical image analysis", "diabetic retinopathy", "attention mechanisms",
        "spatial channel attention", "transfer learning", "knowledge distillation",
        "large language models", "retrieval augmented generation", "ai safety",
        "computer vision", "multimodal learning", "natural language processing",
        "efficient deep learning", "retinal pathology", "cnn architectures"
    ],
    "skills": [
        "pytorch", "tensorflow", "python", "resnet", "vgg19", "cnn",
        "attention mechanism", "transfer learning", "knowledge distillation",
        "rag", "llm fine-tuning", "flask", "docker", "git", "react", "streamlit"
    ],
    "projects": [
        {
            "name": "Diabetic Retinopathy Detection (SCDA/DDA)",
            "keywords": ["diabetic retinopathy", "attention mechanism", "scda", "dda",
                         "resnet50", "vgg19", "transfer learning", "medical imaging",
                         "lion optimizer", "retinal", "cibm", "dfki"]
        },
        {
            "name": "Pneumonia Detector",
            "keywords": ["pneumonia", "chest x-ray", "medical imaging", "computer vision",
                         "classification", "flask", "tensorflow", "ann"]
        },
        {
            "name": "Kisan Saathi",
            "keywords": ["multimodal", "chatbot", "plant disease", "gemini",
                         "react", "node.js", "agriculture", "deployed"]
        },
        {
            "name": "RAG Pipeline at Owlvest",
            "keywords": ["rag", "llm", "retrieval augmented generation",
                         "hallucination", "fine-tuning", "inference"]
        }
    ]
}


class MatchingEngine:
    """Scores professors against Sarmad's profile and ranks them."""

    def __init__(self, student_profile: Dict = None):
        self.profile = student_profile or SARMAD_PROFILE

    def compute_match_score(self, professor: Dict) -> Dict:
        """
        Compute a 0-100 match score between professor and student profile.
        Returns score + breakdown.
        """
        score = 0
        overlap_areas = []
        gaps = []

        # Build professor text corpus
        prof_text = self._build_professor_text(professor)

        # 1. Interest keyword overlap (40 points max)
        interest_hits = 0
        for interest in self.profile["interests"]:
            if interest.lower() in prof_text:
                interest_hits += 1
                overlap_areas.append(interest)
        interest_score = min((interest_hits / len(self.profile["interests"])) * 40, 40)
        score += interest_score

        # 2. Skill overlap (20 points max)
        skill_hits = 0
        for skill in self.profile["skills"]:
            if skill.lower() in prof_text:
                skill_hits += 1
        skill_score = min((skill_hits / len(self.profile["skills"])) * 20, 20)
        score += skill_score

        # 3. Project alignment (30 points max)
        project_score = 0
        for project in self.profile["projects"]:
            proj_hits = sum(1 for kw in project["keywords"] if kw.lower() in prof_text)
            if proj_hits >= 2:
                project_score += 10
                overlap_areas.append(f"Project: {project['name']}")
        project_score = min(project_score, 30)
        score += project_score

        # 4. Academic strength bonus (10 points max)
        h_bonus = min(professor.get("hIndex", 0) / 50 * 10, 10)
        score += h_bonus

        # Identify gaps
        core_areas = ["medical image analysis", "knowledge distillation", "large language models"]
        for area in core_areas:
            if area not in overlap_areas:
                gaps.append(f"No overlap with: {area}")

        # Deduplicate overlap areas
        overlap_areas = list(dict.fromkeys(overlap_areas))

        return {
            "match_score": round(min(score, 100), 1),
            "overlap_areas": overlap_areas[:5],
            "gaps": gaps,
            "breakdown": {
                "interest_score": round(interest_score, 1),
                "skill_score": round(skill_score, 1),
                "project_score": round(project_score, 1),
                "academic_bonus": round(h_bonus, 1)
            }
        }

    def _build_professor_text(self, professor: Dict) -> str:
        """Build a searchable text blob from professor data."""
        parts = []
        parts.append(professor.get("name", ""))
        for paper in professor.get("recent_papers", []):
            parts.append(paper.get("title", ""))
            parts.append((paper.get("abstract") or "")[:300])
        for kw in professor.get("research_keywords", []):
            parts.append(kw)
        return " ".join(parts).lower()

    def rank_professors(self, professors: List[Dict]) -> List[Dict]:
        """Add match scores and rank professors."""
        for prof in professors:
            match = self.compute_match_score(prof)
            prof["match_score"] = match["match_score"]
            prof["overlap_areas"] = match["overlap_areas"]
            prof["gaps"] = match["gaps"]
            prof["score_breakdown"] = match["breakdown"]

        return sorted(professors, key=lambda x: x["match_score"], reverse=True)
