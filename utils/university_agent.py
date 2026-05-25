import requests
import time
from typing import List, Dict

TOP_UNIVERSITIES_BY_REGION = {
    "USA": [
        {"name": "MIT", "country": "USA", "qs_rank": 1},
        {"name": "Stanford University", "country": "USA", "qs_rank": 2},
        {"name": "Carnegie Mellon University", "country": "USA", "qs_rank": 3},
        {"name": "University of California Berkeley", "country": "USA", "qs_rank": 4},
        {"name": "Harvard University", "country": "USA", "qs_rank": 5},
        {"name": "Princeton University", "country": "USA", "qs_rank": 6},
        {"name": "University of Washington", "country": "USA", "qs_rank": 7},
        {"name": "Columbia University", "country": "USA", "qs_rank": 8},
        {"name": "New York University", "country": "USA", "qs_rank": 9},
        {"name": "Cornell University", "country": "USA", "qs_rank": 10},
        {"name": "University of Michigan", "country": "USA", "qs_rank": 11},
        {"name": "University of California Los Angeles", "country": "USA", "qs_rank": 12},
        {"name": "University of California San Diego", "country": "USA", "qs_rank": 13},
        {"name": "University of Illinois Urbana-Champaign", "country": "USA", "qs_rank": 14},
        {"name": "Georgia Institute of Technology", "country": "USA", "qs_rank": 15},
        {"name": "University of Texas Austin", "country": "USA", "qs_rank": 16},
        {"name": "University of Pennsylvania", "country": "USA", "qs_rank": 17},
        {"name": "Johns Hopkins University", "country": "USA", "qs_rank": 18},
        {"name": "Duke University", "country": "USA", "qs_rank": 19},
        {"name": "University of Wisconsin Madison", "country": "USA", "qs_rank": 20},
        # Rank 100-300
        {"name": "University of Massachusetts Amherst", "country": "USA", "qs_rank": 101},
        {"name": "University of Maryland", "country": "USA", "qs_rank": 102},
        {"name": "Brown University", "country": "USA", "qs_rank": 103},
        {"name": "Purdue University", "country": "USA", "qs_rank": 104},
        {"name": "University of Minnesota", "country": "USA", "qs_rank": 105},
        {"name": "Ohio State University", "country": "USA", "qs_rank": 106},
        {"name": "University of California Santa Barbara", "country": "USA", "qs_rank": 107},
        {"name": "University of California Irvine", "country": "USA", "qs_rank": 108},
        {"name": "Rice University", "country": "USA", "qs_rank": 109},
        {"name": "Vanderbilt University", "country": "USA", "qs_rank": 110},
        {"name": "University of Colorado Boulder", "country": "USA", "qs_rank": 111},
        {"name": "Stony Brook University", "country": "USA", "qs_rank": 112},
        {"name": "University of Pittsburgh", "country": "USA", "qs_rank": 113},
        {"name": "Rutgers University", "country": "USA", "qs_rank": 114},
        {"name": "Penn State University", "country": "USA", "qs_rank": 115},
        {"name": "University of Notre Dame", "country": "USA", "qs_rank": 116},
        {"name": "University of Southern California", "country": "USA", "qs_rank": 117},
        {"name": "Northeastern University", "country": "USA", "qs_rank": 118},
        {"name": "Boston University", "country": "USA", "qs_rank": 119},
        {"name": "University of Arizona", "country": "USA", "qs_rank": 120},
        {"name": "University of Virginia", "country": "USA", "qs_rank": 121},
        {"name": "University of Florida", "country": "USA", "qs_rank": 122},
        {"name": "Michigan State University", "country": "USA", "qs_rank": 123},
        {"name": "Indiana University Bloomington", "country": "USA", "qs_rank": 124},
        {"name": "University of Rochester", "country": "USA", "qs_rank": 125},
    ],
    "Germany": [
        {"name": "Technical University of Munich", "country": "Germany", "qs_rank": 1},
        {"name": "RWTH Aachen University", "country": "Germany", "qs_rank": 2},
        {"name": "Karlsruhe Institute of Technology", "country": "Germany", "qs_rank": 3},
        {"name": "University of Freiburg", "country": "Germany", "qs_rank": 4},
        {"name": "University of Tubingen", "country": "Germany", "qs_rank": 5},
        {"name": "Saarland University", "country": "Germany", "qs_rank": 6},
        {"name": "TU Berlin", "country": "Germany", "qs_rank": 7},
        {"name": "Heidelberg University", "country": "Germany", "qs_rank": 8},
        # Rank 100-300
        {"name": "University of Bonn", "country": "Germany", "qs_rank": 101},
        {"name": "University of Hamburg", "country": "Germany", "qs_rank": 102},
        {"name": "TU Darmstadt", "country": "Germany", "qs_rank": 103},
        {"name": "University of Erlangen Nuremberg", "country": "Germany", "qs_rank": 104},
        {"name": "University of Stuttgart", "country": "Germany", "qs_rank": 105},
        {"name": "University of Cologne", "country": "Germany", "qs_rank": 106},
        {"name": "University of Gottingen", "country": "Germany", "qs_rank": 107},
        {"name": "University of Munster", "country": "Germany", "qs_rank": 108},
        {"name": "Ludwig Maximilian University Munich", "country": "Germany", "qs_rank": 109},
        {"name": "Humboldt University Berlin", "country": "Germany", "qs_rank": 110},
    ],
    "UK": [
        {"name": "University of Oxford", "country": "UK", "qs_rank": 1},
        {"name": "University of Cambridge", "country": "UK", "qs_rank": 2},
        {"name": "Imperial College London", "country": "UK", "qs_rank": 3},
        {"name": "University College London", "country": "UK", "qs_rank": 4},
        {"name": "University of Edinburgh", "country": "UK", "qs_rank": 5},
        {"name": "University of Manchester", "country": "UK", "qs_rank": 6},
        # Rank 100-300
        {"name": "University of Bristol", "country": "UK", "qs_rank": 101},
        {"name": "University of Warwick", "country": "UK", "qs_rank": 102},
        {"name": "University of Glasgow", "country": "UK", "qs_rank": 103},
        {"name": "University of Birmingham", "country": "UK", "qs_rank": 104},
        {"name": "University of Sheffield", "country": "UK", "qs_rank": 105},
        {"name": "University of Southampton", "country": "UK", "qs_rank": 106},
        {"name": "University of Nottingham", "country": "UK", "qs_rank": 107},
        {"name": "University of Leeds", "country": "UK", "qs_rank": 108},
        {"name": "King's College London", "country": "UK", "qs_rank": 109},
        {"name": "University of Bath", "country": "UK", "qs_rank": 110},
        {"name": "Durham University", "country": "UK", "qs_rank": 111},
        {"name": "University of St Andrews", "country": "UK", "qs_rank": 112},
    ],
    "Canada": [
        {"name": "University of Toronto", "country": "Canada", "qs_rank": 1},
        {"name": "McGill University", "country": "Canada", "qs_rank": 2},
        {"name": "University of Waterloo", "country": "Canada", "qs_rank": 3},
        {"name": "Mila Quebec AI Institute", "country": "Canada", "qs_rank": 4},
        {"name": "University of British Columbia", "country": "Canada", "qs_rank": 5},
        {"name": "University of Alberta", "country": "Canada", "qs_rank": 6},
        # Rank 100-300
        {"name": "Simon Fraser University", "country": "Canada", "qs_rank": 101},
        {"name": "University of Montreal", "country": "Canada", "qs_rank": 102},
        {"name": "University of Ottawa", "country": "Canada", "qs_rank": 103},
        {"name": "York University", "country": "Canada", "qs_rank": 104},
        {"name": "Dalhousie University", "country": "Canada", "qs_rank": 105},
        {"name": "University of Calgary", "country": "Canada", "qs_rank": 106},
        {"name": "Queen's University", "country": "Canada", "qs_rank": 107},
    ],
    "Japan": [
        {"name": "University of Tokyo", "country": "Japan", "qs_rank": 1},
        {"name": "Kyoto University", "country": "Japan", "qs_rank": 2},
        {"name": "Osaka University", "country": "Japan", "qs_rank": 3},
        {"name": "Tokyo Institute of Technology", "country": "Japan", "qs_rank": 4},
        # Rank 100-300
        {"name": "Tohoku University", "country": "Japan", "qs_rank": 101},
        {"name": "Nagoya University", "country": "Japan", "qs_rank": 102},
        {"name": "Kyushu University", "country": "Japan", "qs_rank": 103},
        {"name": "Hokkaido University", "country": "Japan", "qs_rank": 104},
        {"name": "Keio University", "country": "Japan", "qs_rank": 105},
        {"name": "Waseda University", "country": "Japan", "qs_rank": 106},
        {"name": "NAIST", "country": "Japan", "qs_rank": 107},
        {"name": "JAIST", "country": "Japan", "qs_rank": 108},
    ],
    "China": [
        {"name": "Tsinghua University", "country": "China", "qs_rank": 1},
        {"name": "Peking University", "country": "China", "qs_rank": 2},
        {"name": "Zhejiang University", "country": "China", "qs_rank": 3},
        {"name": "Shanghai Jiao Tong University", "country": "China", "qs_rank": 4},
        # Rank 100-300
        {"name": "Fudan University", "country": "China", "qs_rank": 101},
        {"name": "University of Science and Technology of China", "country": "China", "qs_rank": 102},
        {"name": "Nanjing University", "country": "China", "qs_rank": 103},
        {"name": "Wuhan University", "country": "China", "qs_rank": 104},
        {"name": "Sun Yat-sen University", "country": "China", "qs_rank": 105},
        {"name": "Harbin Institute of Technology", "country": "China", "qs_rank": 106},
        {"name": "Central South University", "country": "China", "qs_rank": 107},
        {"name": "Tongji University", "country": "China", "qs_rank": 108},
        {"name": "Beihang University", "country": "China", "qs_rank": 109},
        {"name": "Xi'an Jiaotong University", "country": "China", "qs_rank": 110},
        {"name": "Beijing Institute of Technology", "country": "China", "qs_rank": 111},
        {"name": "Renmin University of China", "country": "China", "qs_rank": 112},
    ],
    "Australia": [
        {"name": "Australian National University", "country": "Australia", "qs_rank": 1},
        {"name": "University of Melbourne", "country": "Australia", "qs_rank": 2},
        {"name": "University of Sydney", "country": "Australia", "qs_rank": 3},
        # Rank 100-300
        {"name": "University of Queensland", "country": "Australia", "qs_rank": 101},
        {"name": "Monash University", "country": "Australia", "qs_rank": 102},
        {"name": "University of New South Wales", "country": "Australia", "qs_rank": 103},
        {"name": "University of Adelaide", "country": "Australia", "qs_rank": 104},
        {"name": "University of Western Australia", "country": "Australia", "qs_rank": 105},
        {"name": "Macquarie University", "country": "Australia", "qs_rank": 106},
        {"name": "Deakin University", "country": "Australia", "qs_rank": 107},
    ],
    "Switzerland": [
        {"name": "ETH Zurich", "country": "Switzerland", "qs_rank": 1},
        {"name": "EPFL", "country": "Switzerland", "qs_rank": 2},
        {"name": "University of Zurich", "country": "Switzerland", "qs_rank": 101},
        {"name": "University of Basel", "country": "Switzerland", "qs_rank": 102},
        {"name": "University of Bern", "country": "Switzerland", "qs_rank": 103},
    ],
    "Netherlands": [
        {"name": "University of Amsterdam", "country": "Netherlands", "qs_rank": 1},
        {"name": "Delft University of Technology", "country": "Netherlands", "qs_rank": 2},
        {"name": "Eindhoven University of Technology", "country": "Netherlands", "qs_rank": 101},
        {"name": "Utrecht University", "country": "Netherlands", "qs_rank": 102},
        {"name": "Leiden University", "country": "Netherlands", "qs_rank": 103},
        {"name": "Radboud University", "country": "Netherlands", "qs_rank": 104},
    ],
    "South_Korea": [
        {"name": "Seoul National University", "country": "South Korea", "qs_rank": 1},
        {"name": "KAIST", "country": "South Korea", "qs_rank": 2},
        {"name": "POSTECH", "country": "South Korea", "qs_rank": 3},
        {"name": "Yonsei University", "country": "South Korea", "qs_rank": 101},
        {"name": "Korea University", "country": "South Korea", "qs_rank": 102},
        {"name": "Sungkyunkwan University", "country": "South Korea", "qs_rank": 103},
        {"name": "Hanyang University", "country": "South Korea", "qs_rank": 104},
    ],
    "Singapore": [
        {"name": "National University of Singapore", "country": "Singapore", "qs_rank": 1},
        {"name": "Nanyang Technological University", "country": "Singapore", "qs_rank": 2},
        {"name": "Singapore Management University", "country": "Singapore", "qs_rank": 101},
    ],
    "Turkey": [
        {"name": "Middle East Technical University", "country": "Turkey", "qs_rank": 1},
        {"name": "Bilkent University", "country": "Turkey", "qs_rank": 2},
        {"name": "Bogazici University", "country": "Turkey", "qs_rank": 3},
        {"name": "Istanbul Technical University", "country": "Turkey", "qs_rank": 101},
        {"name": "Koc University", "country": "Turkey", "qs_rank": 102},
        {"name": "Sabanci University", "country": "Turkey", "qs_rank": 103},
        {"name": "Hacettepe University", "country": "Turkey", "qs_rank": 104},
    ],
    "Sweden": [
        {"name": "KTH Royal Institute of Technology", "country": "Sweden", "qs_rank": 1},
        {"name": "Chalmers University of Technology", "country": "Sweden", "qs_rank": 2},
        {"name": "Lund University", "country": "Sweden", "qs_rank": 101},
        {"name": "Uppsala University", "country": "Sweden", "qs_rank": 102},
        {"name": "Linkoping University", "country": "Sweden", "qs_rank": 103},
    ],
    "France": [
        {"name": "Inria", "country": "France", "qs_rank": 1},
        {"name": "Ecole Polytechnique", "country": "France", "qs_rank": 2},
        {"name": "Sorbonne University", "country": "France", "qs_rank": 3},
        {"name": "University of Paris", "country": "France", "qs_rank": 101},
        {"name": "CentraleSupelec", "country": "France", "qs_rank": 102},
        {"name": "Grenoble INP", "country": "France", "qs_rank": 103},
        {"name": "University of Bordeaux", "country": "France", "qs_rank": 104},
    ],
    "Italy": [
        {"name": "Politecnico di Milano", "country": "Italy", "qs_rank": 1},
        {"name": "Politecnico di Torino", "country": "Italy", "qs_rank": 2},
        {"name": "Sapienza University of Rome", "country": "Italy", "qs_rank": 101},
        {"name": "University of Bologna", "country": "Italy", "qs_rank": 102},
        {"name": "University of Padova", "country": "Italy", "qs_rank": 103},
        {"name": "University of Trento", "country": "Italy", "qs_rank": 104},
    ],
    "Hungary": [
        {"name": "Budapest University of Technology and Economics", "country": "Hungary", "qs_rank": 1},
        {"name": "Eotvos Lorand University", "country": "Hungary", "qs_rank": 2},
        {"name": "University of Debrecen", "country": "Hungary", "qs_rank": 101},
        {"name": "University of Pecs", "country": "Hungary", "qs_rank": 102},
    ],
    "Austria": [
        {"name": "Vienna University of Technology", "country": "Austria", "qs_rank": 101},
        {"name": "University of Vienna", "country": "Austria", "qs_rank": 102},
        {"name": "Graz University of Technology", "country": "Austria", "qs_rank": 103},
        {"name": "Johannes Kepler University Linz", "country": "Austria", "qs_rank": 104},
    ],
    "Belgium": [
        {"name": "KU Leuven", "country": "Belgium", "qs_rank": 101},
        {"name": "Ghent University", "country": "Belgium", "qs_rank": 102},
        {"name": "Vrije Universiteit Brussel", "country": "Belgium", "qs_rank": 103},
    ],
    "Denmark": [
        {"name": "Technical University of Denmark", "country": "Denmark", "qs_rank": 101},
        {"name": "University of Copenhagen", "country": "Denmark", "qs_rank": 102},
        {"name": "Aarhus University", "country": "Denmark", "qs_rank": 103},
    ],
    "Finland": [
        {"name": "Aalto University", "country": "Finland", "qs_rank": 101},
        {"name": "University of Helsinki", "country": "Finland", "qs_rank": 102},
        {"name": "University of Oulu", "country": "Finland", "qs_rank": 103},
    ],
    "Norway": [
        {"name": "Norwegian University of Science and Technology", "country": "Norway", "qs_rank": 101},
        {"name": "University of Oslo", "country": "Norway", "qs_rank": 102},
    ],
    "Czech_Republic": [
        {"name": "Czech Technical University in Prague", "country": "Czech Republic", "qs_rank": 101},
        {"name": "Charles University", "country": "Czech Republic", "qs_rank": 102},
        {"name": "Brno University of Technology", "country": "Czech Republic", "qs_rank": 103},
    ],
    "Poland": [
        {"name": "Warsaw University of Technology", "country": "Poland", "qs_rank": 101},
        {"name": "AGH University of Science and Technology", "country": "Poland", "qs_rank": 102},
        {"name": "Jagiellonian University", "country": "Poland", "qs_rank": 103},
    ],
    "Portugal": [
        {"name": "Instituto Superior Tecnico Lisbon", "country": "Portugal", "qs_rank": 101},
        {"name": "University of Porto", "country": "Portugal", "qs_rank": 102},
    ],
    "Spain": [
        {"name": "Universitat Politecnica de Catalunya", "country": "Spain", "qs_rank": 101},
        {"name": "Universidad Autonoma de Madrid", "country": "Spain", "qs_rank": 102},
        {"name": "University of Barcelona", "country": "Spain", "qs_rank": 103},
    ],
    "Taiwan": [
        {"name": "National Taiwan University", "country": "Taiwan", "qs_rank": 101},
        {"name": "National Tsing Hua University", "country": "Taiwan", "qs_rank": 102},
        {"name": "National Chiao Tung University", "country": "Taiwan", "qs_rank": 103},
    ],
    "Hong_Kong": [
        {"name": "Hong Kong University of Science and Technology", "country": "Hong Kong", "qs_rank": 101},
        {"name": "University of Hong Kong", "country": "Hong Kong", "qs_rank": 102},
        {"name": "Chinese University of Hong Kong", "country": "Hong Kong", "qs_rank": 103},
    ],
    "New_Zealand": [
        {"name": "University of Auckland", "country": "New Zealand", "qs_rank": 101},
        {"name": "Victoria University of Wellington", "country": "New Zealand", "qs_rank": 102},
    ],
}

TOP_50_UNIVERSITIES = [u for unis in TOP_UNIVERSITIES_BY_REGION.values() for u in unis]

SARMAD_RESEARCH_AREAS = [
    "medical image analysis",
    "knowledge distillation",
    "efficient deep learning",
    "large language models",
    "retrieval augmented generation",
    "AI safety",
    "computer vision",
    "transfer learning",
    "multimodal learning",
    "natural language processing",
]


class UniversityAgent:
    """
    Discovers professors using Semantic Scholar PAPER search.
    Strategy: search papers by topic, extract authors, filter by affiliation + h-index.
    This is more reliable than author search with topic+university queries.
    """

    def __init__(self, api_base_url, api_key=None):
        self.api_base_url = api_base_url
        self.headers = {"User-Agent": "ProfessorOutreachSystem/1.0"}
        if api_key:
            self.headers["x-api-key"] = api_key
        self._author_cache = {}

    def _get(self, url, params, retries=3):
        for attempt in range(retries):
            try:
                r = requests.get(url, params=params, headers=self.headers, timeout=15)
                if r.status_code == 429:
                    wait = 10 * (attempt + 1)
                    print(f"    Rate limited — waiting {wait}s...")
                    time.sleep(wait)
                    continue
                r.raise_for_status()
                return r.json()
            except Exception as e:
                if attempt == retries - 1:
                    return None
                time.sleep(3)
        return None

    def search_papers_by_topic(self, research_area, limit=10):
        """Search papers by topic — returns papers with author info."""
        data = self._get(
            f"{self.api_base_url}/paper/search",
            {
                "query": research_area,
                "limit": limit,
                "fields": "title,year,citationCount,authors",
                "sort": "citationCount:desc",
            }
        )
        time.sleep(3)
        return data.get("data", []) if data else []

    def get_author_details(self, author_id):
        """Get full author profile including h-index and affiliations."""
        if author_id in self._author_cache:
            return self._author_cache[author_id]
        data = self._get(
            f"{self.api_base_url}/author/{author_id}",
            {"fields": "name,affiliations,paperCount,citationCount,hIndex"}
        )
        time.sleep(3)
        if data:
            self._author_cache[author_id] = data
        return data

    def get_author_papers(self, author_id, limit=10):
        """Get recent papers for an author."""
        data = self._get(
            f"{self.api_base_url}/author/{author_id}/papers",
            {"fields": "title,abstract,year,citationCount", "limit": limit}
        )
        time.sleep(3)
        if not data:
            return []
        papers = data.get("data", [])
        return sorted(papers, key=lambda x: x.get("citationCount", 0), reverse=True)[:3]

    def affiliation_matches(self, author_data, university_names):
        """Check if author is affiliated with any of the target universities."""
        affiliations = author_data.get("affiliations", [])
        if not affiliations:
            return False
        aff_text = " ".join(
            (a.get("name", "") if isinstance(a, dict) else str(a))
            for a in affiliations
        ).lower()
        for uni in university_names:
            # Check key words from university name
            words = [w for w in uni.lower().split() if len(w) > 3]
            if any(w in aff_text for w in words):
                return True
        return False

    def is_valid_faculty(self, author_data):
        """Professor or Associate Professor level: h-index >= 8, citations >= 200."""
        return (
            author_data.get("hIndex", 0) >= 8 and
            author_data.get("citationCount", 0) >= 200
        )

    def score_professor(self, author_data, papers, research_areas):
        score = 0.0
        score += min(author_data.get("citationCount", 0) / 5000, 3.0)
        score += min(author_data.get("hIndex", 0) / 20, 2.0)
        score += min(author_data.get("paperCount", 0) / 100, 1.0)
        paper_text = " ".join([
            (p.get("title") or "") + " " + (p.get("abstract") or "")[:100]
            for p in papers[:5]
        ]).lower()
        for area in research_areas:
            if area.lower() in paper_text:
                score += 1.5
        return round(score, 2)

    def discover_professors(self, universities, research_areas, top_n=50):
        """
        Strategy: search papers by topic → extract authors → 
        check affiliation against target universities → filter by h-index.
        Optimized: skip author detail calls for already-seen authors.
        """
        all_professors = {}
        seen_author_ids = set()
        uni_names = [u["name"] for u in universities]
        uni_country = {u["name"]: u["country"] for u in universities}

        total = len(research_areas)
        for i, area in enumerate(research_areas, 1):
            print(f"  [{i}/{total}] Searching papers: {area}")

            papers = self.search_papers_by_topic(area, limit=15)

            for paper in papers:
                for author_stub in paper.get("authors", [])[:5]:
                    author_id = author_stub.get("authorId")
                    if not author_id or author_id in seen_author_ids:
                        continue
                    seen_author_ids.add(author_id)

                    # Get full author profile
                    author_data = self.get_author_details(author_id)
                    if not author_data:
                        continue

                    # Quick pre-filter before expensive affiliation check
                    if not self.is_valid_faculty(author_data):
                        continue

                    # Check affiliation matches target universities
                    if not self.affiliation_matches(author_data, uni_names):
                        continue

                    # Get their papers
                    author_papers = self.get_author_papers(author_id, limit=10)
                    score = self.score_professor(author_data, author_papers, research_areas)

                    # Determine country
                    affiliations = author_data.get("affiliations", [])
                    aff_text = " ".join(
                        (a.get("name", "") if isinstance(a, dict) else str(a))
                        for a in affiliations
                    ).lower()
                    country = "Unknown"
                    uni_name_found = "Unknown"
                    for uni_name, uni_c in uni_country.items():
                        words = [w for w in uni_name.lower().split() if len(w) > 3]
                        if any(w in aff_text for w in words):
                            country = uni_c
                            uni_name_found = uni_name
                            break

                    all_professors[author_id] = {
                        "authorId": author_id,
                        "name": author_data.get("name", "Unknown"),
                        "affiliations": affiliations,
                        "university": uni_name_found,
                        "country": country,
                        "hIndex": author_data.get("hIndex", 0),
                        "citationCount": author_data.get("citationCount", 0),
                        "paperCount": author_data.get("paperCount", 0),
                        "relevance_score": score,
                        "recent_papers": author_papers[:3],
                    }
                    print(f"    ✓ {author_data.get('name')} | {uni_name_found} | {country} | h={author_data.get('hIndex',0)}")

        ranked = sorted(all_professors.values(), key=lambda x: x["relevance_score"], reverse=True)
        return ranked[:top_n]

    def get_universities_by_region(self, regions=None):
        if not regions:
            return TOP_50_UNIVERSITIES
        result = []
        for region in regions:
            result.extend(TOP_UNIVERSITIES_BY_REGION.get(region, []))
        return result
