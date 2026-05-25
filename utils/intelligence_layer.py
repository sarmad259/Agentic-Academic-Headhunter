import os
from groq import Groq
from typing import Dict, List

GOLD_STANDARD_FOLDER = "gold_standard"


def _load_gold_standard_examples(folder: str = GOLD_STANDARD_FOLDER, max_examples: int = 2) -> str:
    """
    Load up to `max_examples` approved email drafts from the gold_standard/ folder.
    These are used as few-shot examples to self-improve the LLM drafts over time.
    Returns an empty string (and never crashes) if the folder is empty or missing.
    """
    try:
        if not os.path.exists(folder):
            return ""
        files = [f for f in os.listdir(folder) if f.endswith(".md")]
        if not files:
            return ""
        examples = []
        for fname in sorted(files)[:max_examples]:
            with open(os.path.join(folder, fname), "r", encoding="utf-8") as fh:
                content = fh.read()
            # Extract only the email body (after ## Email Body header if present)
            if "## Email Body" in content:
                body = content.split("## Email Body")[-1].strip()
                if "---" in body:
                    body = body.split("---")[0].strip()
            else:
                body = content.strip()[:600]  # Fallback: first 600 chars
            examples.append(f"[EXAMPLE EMAIL]\n{body}\n[END EXAMPLE]")
        if not examples:
            return ""
        return (
            "\n\nHIGH-QUALITY EXAMPLE EMAILS (study the tone, flow, and specificity):\n"
            + "\n\n".join(examples)
            + "\n\nMatch this tone and level of specificity in your email.\n"
        )
    except Exception:
        return ""  # Silent fallback — never break the pipeline


# Context map: professor research area → which of Sarmad's work to highlight
CONTEXT_MAP = {
    "medical imaging": {
        "angle": "medical AI and attention mechanisms",
        "highlight": "novel SCDA (Spatial Channel Dual Attention) and DDA (Dynamic Depthwise Attention) mechanisms for diabetic retinopathy detection, achieving 97.22% accuracy (+5.91% over the published CIBM 2025 baseline) under DFKI-affiliated supervision",
        "hook": "my independent research extending a published CIBM 2025 architecture with novel attention mechanisms achieving 97.22% accuracy"
    },
    "computer vision": {
        "angle": "deep learning architectures for visual recognition",
        "highlight": "transfer learning with ResNet50 and VGG19 for retinal pathology with novel SCDA/DDA attention mechanisms (97.22% accuracy), and a custom YOLOv11 model for document form detection achieving 70% mAP@50",
        "hook": "my work spanning medical image classification (97.22% accuracy) and document object detection (YOLOv11, 70% mAP@50)"
    },
    "attention mechanism": {
        "angle": "attention mechanisms in deep learning",
        "highlight": "novel SCDA (Spatial Channel Dual Attention) and DDA (Dynamic Depthwise Attention) mechanisms — first application of Lion optimizer to retinal pathology, resolving Type 1 diabetes recall collapse from 50% to 96.9%",
        "hook": "my independent development of two novel attention mechanisms achieving 97.22% accuracy on diabetic retinopathy detection"
    },
    "transfer learning": {
        "angle": "transfer learning for medical domains",
        "highlight": "transfer learning with ResNet50 and VGG19 on retinal datasets, extending a published architecture to a new pathology with +5.91% accuracy improvement",
        "hook": "my independent research on transfer learning for diabetic retinopathy, achieving +5.91% over the published CIBM 2025 baseline"
    },
    "document": {
        "angle": "document understanding and form automation",
        "highlight": "CollabForms — a novel proximity-based spatial clustering algorithm that resolves checkbox-label associations in university forms (a problem standard OCR cannot address), combined with a Reflexion-inspired LLM refinement loop with persistent cross-session rule memory, achieving 70% mAP@50 with 112ms inference",
        "hook": "my FYP research on AI-powered form automation where I designed a novel spatial clustering algorithm and extended the Reflexion framework to cross-session persistent learning"
    },
    "object detection": {
        "angle": "object detection and spatial reasoning",
        "highlight": "custom YOLOv11 model trained on real university forms achieving 70% mAP@50, with a novel proximity-based spatial clustering algorithm for checkbox-label association and OpenCV contour-based bounding box refinement",
        "hook": "my FYP work combining YOLO detection with novel spatial reasoning algorithms for document understanding"
    },
    "ocr": {
        "angle": "document OCR and information extraction",
        "highlight": "CollabForms pipeline combining YOLOv11 detection, novel spatial clustering for checkbox-label association, parallelized Tesseract OCR with OpenCV contour refinement, and a self-improving LLM structuring loop",
        "hook": "my FYP research solving the checkbox-label association problem that standard OCR pipelines cannot address"
    },
    "agentic": {
        "angle": "agentic AI and self-improving systems",
        "highlight": "Reflexion-inspired iterative LLM refinement loop with persistent cross-session rule memory — extends Reflexion beyond single-task episodic improvement to cross-task transfer learning without model retraining",
        "hook": "my FYP research extending the Reflexion framework to persistent cross-session rule accumulation, enabling genuine cross-task transfer learning"
    },
    "knowledge distillation": {
        "angle": "efficient model deployment",
        "highlight": "KDLight knowledge distillation for lightweight model deployment in medical settings, alongside novel attention mechanism research at DFKI",
        "hook": "my work on model compression and efficient deployment for clinical AI systems"
    },
    "llm": {
        "angle": "LLM systems and evaluation",
        "highlight": "RAG pipeline development and hallucination mitigation systems built in production at Owlvest, plus a Reflexion-inspired self-improving LLM refinement loop in CollabForms with persistent cross-session rule memory",
        "hook": "my production LLM engineering experience combined with research on self-improving LLM systems"
    },
    "rag": {
        "angle": "retrieval-augmented generation",
        "highlight": "RAG pipeline design and LLM fine-tuning for low-latency inference at Owlvest",
        "hook": "my hands-on experience building production RAG systems with hallucination evaluation"
    },
    "ai safety": {
        "angle": "AI reliability and evaluation",
        "highlight": "evaluation systems to monitor and mitigate hallucination in reasoning models, built at Owlvest",
        "hook": "my experience designing safety-oriented evaluation frameworks for production LLMs"
    },
    "multimodal": {
        "angle": "multimodal AI systems",
        "highlight": "Kisan Saathi — a deployed multimodal AI platform combining plant disease vision detection with multilingual language advisory",
        "hook": "my experience building and deploying a production multimodal AI system serving real users"
    },
    "nlp": {
        "angle": "natural language processing",
        "highlight": "LLM fine-tuning and RAG pipeline development for low-latency inference at Owlvest, plus LLM-based structured information extraction in CollabForms",
        "hook": "my production NLP experience building reliable LLM inference and extraction systems"
    },
    "default": {
        "angle": "medical AI and deep learning research",
        "highlight": "novel SCDA/DDA attention mechanisms for diabetic retinopathy detection achieving 97.22% accuracy (independent research), and CollabForms FYP with novel spatial clustering algorithm and Reflexion-inspired LLM refinement",
        "hook": "my two independent research contributions: CollabForms FYP (novel spatial clustering, 70% mAP@50) and SCDA/DDA attention mechanisms (97.22% accuracy on diabetic retinopathy)"
    }
}

PRIORITY_ORDER = [
    "attention mechanism", "document", "object detection", "ocr", "agentic",
    "medical imaging", "transfer learning", "knowledge distillation",
    "ai safety", "rag", "llm", "multimodal", "nlp", "computer vision", "default"
]


class IntelligenceLayer:
    """Uses Groq (free tier) to generate context-aware personalized email drafts."""

    def __init__(self, api_key: str, max_words: int = 200):
        self.client = Groq(api_key=api_key)
        self.max_words = max_words
        self.model = "llama-3.3-70b-versatile"

    def _detect_context(self, professor: Dict, papers: List[Dict]) -> Dict:
        search_text = " ".join(professor.get("research_keywords", [])).lower()
        for paper in papers[:2]:
            search_text += " " + paper.get("title", "").lower()
            search_text += " " + (paper.get("abstract") or "")[:200].lower()

        for key in PRIORITY_ORDER:
            if key in search_text:
                return CONTEXT_MAP[key]
        return CONTEXT_MAP["default"]

    def generate_email_draft(self, profile: Dict, research_result: Dict) -> Dict:
        professor = research_result["professor"]
        papers = research_result["papers"]

        if not papers:
            return {"professor": professor, "draft": None, "error": "No recent papers found"}

        context = self._detect_context(professor, papers)
        prompt = self._build_prompt(professor, papers, context)

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                max_tokens=512,
                messages=[{"role": "user", "content": prompt}]
            )
            draft = response.choices[0].message.content
            return {
                "professor": professor,
                "papers_referenced": papers,
                "draft": draft,
                "subject": self._pick_subject(context["angle"]),
                "context_used": context["angle"]
            }
        except Exception as e:
            print(f"Error generating draft for {professor['name']}: {e}")
            return {"professor": professor, "draft": None, "error": str(e)}

    def _build_prompt(self, professor: Dict, papers: List[Dict], context: Dict) -> str:
        papers_text = ""
        for i, paper in enumerate(papers[:3], 1):
            papers_text += f"\n{i}. \"{paper.get('title', 'Untitled')}\" ({paper.get('year', 'N/A')}, {paper.get('citationCount', 0)} citations)"
            if paper.get("abstract"):
                papers_text += f"\n   {paper['abstract'][:200]}..."

        last_name = professor.get("name", "Professor").split()[-1]

        return (
            f"Write a cold outreach email from Muhammad Sarmad Khan to Prof. {professor['name']} "
            f"at {professor.get('institution', professor.get('university', ''))}.\n\n"
            "SARMAD'S BACKGROUND (use what is most relevant, do not list everything):\n"
            "- BS AI, FAST-NUCES Peshawar, Pakistan | IELTS 7.0 | Available October 2026\n"
            "- FYP CollabForms (primary novel work, supervised by Dr. Omer Usman Khan FAST-NUCES): "
            "designed a novel proximity-based spatial clustering algorithm for checkbox-label association "
            "in document forms (standard OCR cannot solve this). Custom YOLOv11: 70% mAP@50, 112ms CPU inference. "
            "Reflexion-inspired LLM refinement with persistent cross-session rule memory.\n"
            "- Independent research: developed SCDA (Spatial Channel Dual Attention) + DDA (Dynamic Depthwise Attention) "
            "mechanisms for diabetic retinopathy. 97.22% accuracy, +5.91% over CIBM 2025 baseline, "
            "resolved recall collapse 50% to 96.9%\n"
            "- Production: RAG pipelines + hallucination mitigation at Owlvest\n"
            "- Seeking fully funded Masters/PhD\n\n"
            f"BEST ANGLE FOR THIS PROFESSOR: {context['angle']}\n"
            f"SPECIFIC HOOK: {context['hook']}\n\n"
            f"PROFESSOR'S RECENT PAPERS:{papers_text}\n\n"
            "WRITE THE EMAIL:\n\n"
            "Write it like a real human reaching out, not a template. Three natural paragraphs:\n\n"
            "Paragraph 1: Show you genuinely read their paper. Name ONE specific technique by its actual name. "
            "Explain why it caught your attention by connecting it to a real problem you have worked on. "
            "Sound curious and genuine, not transactional.\n\n"
            "Paragraph 2: Share your most relevant work naturally. Use exact numbers but present them as "
            "results you are proud of, not credentials you are listing. Mention both research contributions "
            "if both connect, or just the stronger one.\n\n"
            "Paragraph 3: IELTS 7.0, October 2026. End with a soft genuine request, not a command. "
            "For example: 'I would love to know if there might be an opportunity to contribute to your group' "
            "or 'Would you be open to a brief conversation about whether my work could be relevant?'\n\n"
            "HARD RULES:\n"
            f"- Under {self.max_words} words total\n"
            f"- Start with: Dear Prof. {last_name},\n"
            "- Name the professor's specific technique (not 'your research' or 'your work')\n"
            "- At least one exact number: 97.22%, +5.91%, 50% to 96.9%, 70% mAP@50, or 112ms\n"
            "- NO GPA mention\n"
            "- NO commanding phrases: 'I believe I am a strong fit', 'I am confident', 'makes me an ideal candidate'\n"
            "- NO flattery: 'deeply inspired', 'renowned', 'prestigious', 'I am honored', 'I am excited to'\n"
            "- NO generic phrases: 'my background aligns', 'I am writing to express'\n"
            "- Sound like a curious capable student making a genuine human request, not a salesperson\n"
            "- Email body ONLY, no subject line, no signature block"
            + _load_gold_standard_examples()
        )

    def _pick_subject(self, angle: str) -> str:
        subjects = {
            "medical AI and attention mechanisms": "Prospective Masters Student — Medical AI Research (SCDA/DDA, IELTS 7.0)",
            "document understanding and form automation": "Graduate Application — Document AI Research + Medical CV Background (IELTS 7.0)",
            "object detection and spatial reasoning": "Research Inquiry: YOLOv11 + Spatial Clustering for Document Understanding",
            "agentic AI and self-improving systems": "Graduate Application — Agentic AI Research (Reflexion Extension, IELTS 7.0)",
            "attention mechanisms in deep learning": "Graduate Application — Novel Attention Mechanisms for Medical AI (DFKI Research)",
            "transfer learning for medical domains": "Prospective Masters Student — Transfer Learning Research (DFKI, IELTS 7.0)",
            "LLM systems and evaluation": "Research Inquiry — LLM Systems + Self-Improving Refinement Research (IELTS 7.0)",
        }
        return subjects.get(angle, "Prospective Masters Student — AI Research (Medical CV + Document AI, IELTS 7.0)")

    def generate_all_drafts(self, profile: Dict, research_results: List[Dict]) -> List[Dict]:
        drafts = []
        for result in research_results:
            if result.get("papers"):
                print(f"  Drafting for {result['professor']['name']}...", end=" ")
                draft = self.generate_email_draft(profile, result)
                print(f"[{draft.get('context_used', 'default')}]")
                drafts.append(draft)
            else:
                print(f"  Skipping {result['professor']['name']} — no recent papers")
        return drafts
