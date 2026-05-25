#!/usr/bin/env python3
"""
Test the full LangGraph + Qwen3 pipeline for one professor.
Run: python test_langgraph.py
"""

from agents.runner import run_pipeline_for_professor

prof = {
    "name": "Prof. Hiroshi Tanaka",
    "institution": "University of Tokyo",
    "research_keywords": ["medical imaging", "attention mechanism", "diabetic retinopathy"],
    "author_id": None
}

papers = [{
    "title": "Dual-Branch Spatial-Channel Attention for Retinal Lesion Segmentation",
    "year": 2024,
    "citationCount": 134,
    "abstract": "We propose a dual-branch architecture combining spatial and channel attention for retinal lesion boundary detection in diabetic retinopathy, achieving SOTA on DRIVE and STARE datasets."
}]

print("Running LangGraph pipeline with Qwen3...")
print("Graph: researcher → matcher → drafter → reviewer → finalizer\n")

result = run_pipeline_for_professor(prof, papers, {})

print("\n" + "="*60)
print("SUBJECT:", result.get("subject"))
print("ANGLE:", result.get("context_used"))
print("ATTEMPTS:", result.get("draft_attempts"))
print("REVIEW PASSED:", result.get("review_passed"))
print("\n--- FINAL DRAFT ---")
draft = result.get("draft", "")
if draft:
    print(draft)
else:
    print("EMPTY — Error:", result.get("error"))
print("="*60)
