#!/usr/bin/env python3
"""Test the new paper-based professor discovery."""

from utils.university_agent import UniversityAgent, TOP_50_UNIVERSITIES, SARMAD_RESEARCH_AREAS
from config import SEMANTIC_SCHOLAR_API, SEMANTIC_SCHOLAR_API_KEY

agent = UniversityAgent(SEMANTIC_SCHOLAR_API, SEMANTIC_SCHOLAR_API_KEY)
unis = TOP_50_UNIVERSITIES[:20]
areas = ["medical image analysis"]  # just 1 area for quick test

print("Testing paper-based discovery (1 area, top 20 unis)...")
print("Should find 5-10 professors in ~2 minutes\n")

profs = agent.discover_professors(unis, areas, top_n=10)

print(f"\nFound {len(profs)} professors:")
for p in profs:
    print(f"  {p['name']} | {p['university']} | {p['country']} | h={p['hIndex']} | score={p['relevance_score']}")
