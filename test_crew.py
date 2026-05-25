#!/usr/bin/env python3
"""Test CrewAI pipeline for one professor."""

from crew.outreach_crew import run_crew_for_professor

prof = {
    "name": "Prof. Hiroshi Tanaka",
    "institution": "University of Tokyo",
    "research_keywords": ["medical imaging", "attention mechanism", "diabetic retinopathy"],
}

papers = [{
    "title": "Dual-Branch Spatial-Channel Attention for Retinal Lesion Segmentation",
    "year": 2024,
    "citationCount": 134,
    "abstract": "We propose a dual-branch architecture combining spatial and channel attention for retinal lesion boundary detection in diabetic retinopathy, achieving SOTA on DRIVE and STARE datasets."
}]

print("Running CrewAI pipeline...")
print("Agents: Researcher → Matcher → Drafter → Reviewer (self-correcting)\n")

result = run_crew_for_professor(prof, papers)

print("\n" + "="*60)
print("STATUS:", result.get("status", "unknown"))
print("SUBJECT:", result.get("subject"))
print("\n--- FINAL EMAIL ---")
print(result.get("draft") or f"ERROR: {result.get('error')}")
print("="*60)
