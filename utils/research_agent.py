import requests
import json
import time
from datetime import datetime, timedelta
from typing import List, Dict, Optional


class ResearchAgent:
    """Fetches professor publications using Semantic Scholar API."""

    def __init__(self, api_base_url: str, api_key: str = None):
        self.api_base_url = api_base_url
        self.headers = {"User-Agent": "ProfessorOutreachSystem/1.0"}
        if api_key:
            self.headers["x-api-key"] = api_key
        self._cache = {}  # Simple in-memory cache to avoid duplicate API calls

    def _get(self, url: str, params: dict, retries: int = 3) -> Optional[dict]:
        """GET with retry on rate limit."""
        for attempt in range(retries):
            try:
                r = requests.get(url, params=params, headers=self.headers, timeout=15)
                if r.status_code == 429:
                    wait = 5 * (attempt + 1)
                    print(f"  Rate limited — waiting {wait}s...")
                    time.sleep(wait)
                    continue
                r.raise_for_status()
                return r.json()
            except requests.exceptions.Timeout:
                print(f"  Timeout on attempt {attempt + 1}")
                time.sleep(3)
            except Exception as e:
                print(f"  Error: {e}")
                return None
        return None

    def search_professor(self, name: str, keywords: List[str]) -> Optional[Dict]:
        """Search for a professor by name."""
        cache_key = f"search:{name}"
        if cache_key in self._cache:
            return self._cache[cache_key]

        data = self._get(
            f"{self.api_base_url}/author/search",
            {"query": name, "limit": 5, "fields": "name,affiliations,hIndex,citationCount"}
        )
        time.sleep(2)

        if data and data.get("data"):
            result = data["data"][0]
            self._cache[cache_key] = result
            return result
        return None

    def get_recent_papers(self, author_id: str, months_back: int = 36, limit: int = 3) -> List[Dict]:
        """Fetch recent highly-cited papers for an author."""
        cache_key = f"papers:{author_id}"
        if cache_key in self._cache:
            return self._cache[cache_key]

        year_threshold = (datetime.now() - timedelta(days=months_back * 30)).year

        data = self._get(
            f"{self.api_base_url}/author/{author_id}/papers",
            {"fields": "title,abstract,year,citationCount,venue,url", "limit": 50}
        )
        time.sleep(2)

        if not data:
            return []

        papers = data.get("data", [])
        # Filter by year, sort by citations
        recent = [p for p in papers if p.get("year") and p["year"] >= year_threshold]
        recent.sort(key=lambda x: x.get("citationCount", 0), reverse=True)
        result = recent[:limit]

        self._cache[cache_key] = result
        return result

    def research_professor(self, professor: Dict, months_back: int = 36, papers_limit: int = 3) -> Dict:
        """Full research workflow for a single professor."""
        name = professor.get("name", "Unknown")
        print(f"\n  Researching {name}...")

        # Use existing author_id if available (from discover phase)
        author_id = professor.get("author_id") or professor.get("authorId")

        if not author_id:
            author_data = self.search_professor(name, professor.get("research_keywords", []))
            if not author_data:
                print(f"  ⚠ Not found on Semantic Scholar")
                return {"professor": professor, "author_id": None, "papers": [], "error": "Author not found"}
            author_id = author_data["authorId"]

        print(f"  ✓ Author ID: {author_id}")
        papers = self.get_recent_papers(author_id, months_back, papers_limit)
        print(f"  ✓ Papers: {len(papers)} found")

        return {
            "professor": professor,
            "author_id": author_id,
            "papers": papers
        }

    def research_all_professors(self, targets_path: str, months_back: int = 36, papers_limit: int = 3) -> List[Dict]:
        """Research all professors from targets file."""
        with open(targets_path, "r", encoding="utf-8") as f:
            targets = json.load(f)

        professors = targets.get("professors", [])
        print(f"  Researching {len(professors)} professors...")

        results = []
        for i, professor in enumerate(professors, 1):
            print(f"  [{i}/{len(professors)}]", end="")
            result = self.research_professor(professor, months_back, papers_limit)
            results.append(result)
            time.sleep(2)

        return results
