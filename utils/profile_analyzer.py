import re
from typing import Dict, List

# Hardcoded profile — always accurate, no parsing errors
SARMAD_PROFILE = {
    "name": "Muhammad Sarmad Khan",
    "email": "khansardarms@gmail.com",
    "institution": "FAST-NUCES Peshawar",
    "degree": "BS Artificial Intelligence (2022-2026)",
    "ielts": "7.0 Academic",
    "availability": "October 2026 or later",
    "seeking": "Fully funded Masters/PhD position",

    "research_interests": [
        "Medical Image Analysis and AI-assisted diagnosis",
        "Attention Mechanisms (Spatial, Channel, Dynamic Depthwise)",
        "Transfer Learning for low-resource medical datasets",
        "Document Understanding and Form Automation",
        "Object Detection and Spatial Reasoning",
        "LLM Refinement and Agentic AI Systems",
        "Knowledge Distillation and Efficient Deep Learning",
        "Large Language Models and Retrieval-Augmented Generation",
        "Computer Vision and Deep Neural Architectures",
        "AI Safety and Hallucination Mitigation",
    ],

    "skills": [
        "PyTorch", "TensorFlow", "Python (Expert)",
        "YOLOv11", "ONNX Runtime", "OpenCV",
        "CNN", "ResNet50", "VGG19", "Vision Transformer",
        "Attention Mechanisms", "Transfer Learning", "Knowledge Distillation",
        "LLMs", "RAG pipelines", "LLM fine-tuning", "Reflexion/Self-Refinement",
        "Django", "Flask", "React", "Node.js", "Docker", "Git", "Linux",
    ],

    "top_projects": [
        {
            "name": "CollabForms — AI-Powered University Form Automation (FYP) — PRIMARY",
            "description": (
                "End-to-end AI system that digitizes physical university forms through a multi-stage pipeline: "
                "custom YOLOv11 object detection, novel proximity-based spatial clustering algorithm for "
                "checkbox-label association, OCR extraction, and a Reflexion-inspired LLM refinement loop "
                "with persistent cross-session rule memory."
            ),
            "technologies": "YOLOv11, ONNX, OpenCV, Tesseract OCR, Django, React, PostgreSQL, Docker",
            "impact": (
                "70% mAP@50 on custom NUCES form dataset. 112ms average inference time on CPU. "
                "Novel spatial clustering algorithm solves checkbox-label association problem "
                "that standard OCR pipelines cannot address. "
                "LLM refinement loop extends Reflexion to cross-session persistent learning."
            ),
            "supervisor": "Dr. Omer Usman Khan (FAST-NUCES Peshawar)",
        },
        {
            "name": "Diabetic Retinopathy Detection (Independent Research)",
            "description": (
                "Independent research extending a published CIBM 2025 architecture with novel SCDA "
                "(Spatial Channel Dual Attention) and DDA (Dynamic Depthwise Attention) mechanisms "
                "for diabetic retinopathy detection. First application of Lion optimizer to retinal pathology."
            ),
            "technologies": "PyTorch, ResNet50, VGG19, Transfer Learning, Custom Attention Mechanisms, Lion Optimizer",
            "impact": (
                "97.22% accuracy, +5.91% over published CIBM 2025 baseline. "
                "Resolved Type 1 diabetes recall collapse from 50% to 96.9%."
            ),
        },
        {
            "name": "CollabForms — AI-Powered University Form Automation (FYP)",
            "description": (
                "End-to-end AI system that digitizes physical university forms through a multi-stage pipeline: "
                "custom YOLOv11 object detection, novel proximity-based spatial clustering algorithm for "
                "checkbox-label association, OCR extraction, and a Reflexion-inspired LLM refinement loop "
                "with persistent cross-session rule memory."
            ),
            "technologies": "YOLOv11, ONNX, OpenCV, Tesseract OCR, Django, React, PostgreSQL, Docker",
            "impact": (
                "70% mAP@50 on custom NUCES form dataset. 112ms average inference time on CPU. "
                "Novel spatial clustering algorithm solves checkbox-label association problem "
                "that standard OCR pipelines cannot address. "
                "LLM refinement loop extends Reflexion to cross-session persistent learning."
            ),
            "supervisor": "Dr. Omer Usman Khan (FAST-NUCES Peshawar)",
        },
        {
            "name": "Pneumonia Detector",
            "description": "Medical image classifier detecting pneumonia from chest X-rays using ANN, deployed as Flask web app.",
            "technologies": "Python, ANN, Flask, TensorFlow",
            "impact": "92% classification accuracy, optimized for web-based inference.",
        },
        {
            "name": "Kisan Saathi — Eco-Farm Tech",
            "description": "Full-stack AI agriculture platform with multilingual chatbot for plant disease detection and crop advisory.",
            "technologies": "React, Node.js, Supabase, Gemini API, Python",
            "impact": "Deployed on Vercel in production, serving real-time AI advisory to farmers.",
        },
    ],

    "achievements": [
        "1st Place: KPITB Digital Payment Challenge 2025 (National level)",
        "Finalist: NICAT Aerospace Hackathon",
        "ACM Coding Competition organizer",
    ],

    "recommendation_letters": [
        "Dr. Omer Usman Khan — FAST-NUCES Peshawar (FYP supervisor)",
        "Dr. Omar Khan — FAST-NUCES (PhD, Politecnico di Torino)",
        "Dr. Usman Abbasi — FAST-NUCES (Oxford-affiliated)",
    ],

    "key_stats": {
        "accuracy": "97.22%",
        "improvement_over_baseline": "+5.91%",
        "recall_improvement": "50% → 96.9%",
        "baseline_paper": "CIBM 2025",
        "novel_mechanisms": "SCDA (Spatial Channel Dual Attention) and DDA (Dynamic Depthwise Attention)",
        "optimizer_novelty": "First application of Lion optimizer to retinal pathology",
        "fyp_map": "70% mAP@50",
        "fyp_inference": "112ms average inference on CPU",
        "fyp_novel": "proximity-based spatial clustering algorithm for checkbox-label association",
        "fyp_llm": "Reflexion-inspired cross-session persistent LLM refinement loop",
    }
}


class ProfileAnalyzer:
    """Returns Sarmad's profile."""

    def __init__(self, resume_path: str = None, portfolio_path: str = "portfolio.md"):
        self.portfolio_path = portfolio_path

    def analyze_profile(self) -> Dict:
        profile = dict(SARMAD_PROFILE)
        try:
            with open(self.portfolio_path, "r", encoding="utf-8") as f:
                profile["portfolio_text"] = f.read()
        except Exception:
            profile["portfolio_text"] = ""
        return profile

    def get_email_context(self, research_angle: str = "default") -> str:
        stats = SARMAD_PROFILE["key_stats"]
        return (
            f"Muhammad Sarmad Khan, BS AI student at FAST-NUCES Peshawar, Pakistan. "
            f"IELTS {SARMAD_PROFILE['ielts']}. "
            f"FYP (CollabForms): {stats['fyp_novel']} achieving {stats['fyp_map']} "
            f"with {stats['fyp_inference']}, plus {stats['fyp_llm']}. "
            f"Independent research: developed {stats['novel_mechanisms']} for diabetic retinopathy, "
            f"achieving {stats['accuracy']} ({stats['improvement_over_baseline']} over {stats['baseline_paper']} baseline). "
            f"Available {SARMAD_PROFILE['availability']}. Seeking {SARMAD_PROFILE['seeking']}."
        )
