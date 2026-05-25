import json
from typing import List, Dict

class SemanticGraph:
    """
    Builds RDF-style relationship graph:
    (Professor) → works_in → (Lab/University)
    (Professor) → research_area → (Topic)
    (Professor) → similar_to → (Professor)
    Used to avoid duplicate outreach and suggest next contact in same lab.
    """

    def __init__(self):
        self.triples = []       # RDF-style: [subject, predicate, object]
        self.nodes = {}         # node_id → metadata
        self.lab_map = {}       # university → [professors]
        self.area_map = {}      # research_area → [professors]

    def build(self, professors: List[Dict]) -> None:
        """Build graph from professor list."""
        self.triples = []
        self.nodes = {}
        self.lab_map = {}
        self.area_map = {}

        for prof in professors:
            prof_id = prof.get("authorId", prof["name"].replace(" ", "_"))
            uni = prof.get("university", "Unknown")
            country = prof.get("country", "Unknown")

            # Register node
            self.nodes[prof_id] = {
                "type": "professor",
                "name": prof["name"],
                "university": uni,
                "country": country,
                "match_score": prof.get("match_score", 0),
                "h_index": prof.get("hIndex", 0)
            }

            # Triple: professor → works_in → university
            self.triples.append([prof["name"], "works_in", uni])

            # Triple: professor → located_in → country
            self.triples.append([prof["name"], "located_in", country])

            # Track lab map
            if uni not in self.lab_map:
                self.lab_map[uni] = []
            self.lab_map[uni].append(prof["name"])

            # Research area triples from papers
            for paper in prof.get("recent_papers", []):
                title = paper.get("title", "")
                for area in self._extract_areas(title + " " + (paper.get("abstract") or "")[:200]):
                    self.triples.append([prof["name"], "research_area", area])
                    if area not in self.area_map:
                        self.area_map[area] = []
                    if prof["name"] not in self.area_map[area]:
                        self.area_map[area].append(prof["name"])

            # Research area triples from keywords
            for kw in prof.get("research_keywords", []):
                self.triples.append([prof["name"], "research_area", kw])

        # Build similarity triples (same lab)
        for uni, profs in self.lab_map.items():
            for i, p1 in enumerate(profs):
                for p2 in profs[i+1:]:
                    self.triples.append([p1, "same_lab_as", p2])

    def _extract_areas(self, text: str) -> List[str]:
        """Extract known research areas from text."""
        areas = [
            "medical imaging", "knowledge distillation", "computer vision",
            "natural language processing", "large language models", "rag",
            "transfer learning", "multimodal", "ai safety", "deep learning",
            "reinforcement learning", "federated learning", "model compression"
        ]
        text_lower = text.lower()
        return [a for a in areas if a in text_lower]

    def get_lab_colleagues(self, professor_name: str) -> List[str]:
        """Get other professors in the same lab/university."""
        colleagues = []
        for triple in self.triples:
            if triple[0] == professor_name and triple[1] == "same_lab_as":
                colleagues.append(triple[2])
            elif triple[2] == professor_name and triple[1] == "same_lab_as":
                colleagues.append(triple[0])
        return colleagues

    def get_similar_professors(self, professor_name: str) -> List[str]:
        """Get professors working in same research areas."""
        # Find this professor's areas
        my_areas = set(
            t[2] for t in self.triples
            if t[0] == professor_name and t[1] == "research_area"
        )
        # Find others with overlapping areas
        similar = {}
        for area in my_areas:
            for other in self.area_map.get(area, []):
                if other != professor_name:
                    similar[other] = similar.get(other, 0) + 1
        return sorted(similar, key=lambda x: similar[x], reverse=True)

    def to_json(self) -> Dict:
        """Export graph as JSON."""
        return {
            "triples": self.triples,
            "nodes": self.nodes,
            "lab_map": self.lab_map,
            "area_map": self.area_map,
            "stats": {
                "total_professors": len([n for n in self.nodes.values() if n["type"] == "professor"]),
                "total_triples": len(self.triples),
                "total_labs": len(self.lab_map),
                "total_areas": len(self.area_map)
            }
        }

    def save(self, path: str = "graph.json") -> None:
        with open(path, "w") as f:
            json.dump(self.to_json(), f, indent=2)
        print(f"  ✓ Graph saved to {path}")
