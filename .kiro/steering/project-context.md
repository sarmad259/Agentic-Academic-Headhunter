# Professor Outreach System — Project Context

## Owner
- **Name:** Muhammad Sarmad Khan
- **Email:** khansardarms@gmail.com (Resend registered + Gmail SMTP sender)
- **Secondary Email:** p229009@pwr.nu.edu.pk
- **Location:** Haripur, KPK, Pakistan
- **Institute:** FAST-NUCES Peshawar, BS Artificial Intelligence (2022–2026)
- **Expected Graduation:** June 1, 2026 (Hope Certificate issued — final degree pending)
- **CGPA:** 2.35/4.0 (64.9%) — German equivalent ~3.3-3.5
- **IELTS:** 7.0 Academic ✅ (April 22, 2026)

## Project Goal
Agentic system that discovers professors at top-50 universities across multiple regions, personalizes outreach emails based on their research, and manages the full send/follow-up pipeline for Masters/PhD scholarship applications.

## Target Programs
- **Primary:** Masters in CS / AI / Data Science
- **Geography:** Europe > China > Turkey
- **Funding required:** Full funding (tuition + stipend €800-1000/month minimum)
- **Start date:** October 2026 or later
- **Realistic options:** Türkiye Burslari, Stipendium Hungaricum, CSC China (with Dr. Saif LOR), selected German universities

## LLM Stack (priority order in agents/nodes.py)
1. **DeepSeek-V4-Flash** (`deepseek-v4-flash:cloud`) — 284B MoE, 13B activated, 1M context
   - Draft node: non-thinking mode (fast)
   - Review node: thinking mode (careful analysis)
2. **Qwen3.5-397B** (`qwen3.5:397b-cloud`) — fallback
3. **Groq Llama-3.3-70b** — always-available fallback (API key in .env)
- **Email Sending:** Gmail SMTP (smtplib) — sends to any address, no domain needed
- **Research Data:** Semantic Scholar API (authenticated)
- **Dashboard:** Flask + vanilla JS
- **Language:** Python 3.10

## API Keys (stored in .env — never hardcode)
- `GROQ_API_KEY` — Groq console: console.groq.com
- `RESEND_API_KEY` — Resend (kept as fallback)
- `SEMANTIC_SCHOLAR_API_KEY` — Authenticated key
- `SENDER_EMAIL` — khansardarms@gmail.com
- `SENDER_NAME` — Muhammad Sarmad Khan
- `GMAIL_APP_PASSWORD` — 16-char Gmail App Password (no spaces)

## Gmail SMTP — WORKING
Sending via smtplib + Gmail App Password. Confirmed working to external addresses.
Dr. Saif Ur Rehman Khan's email available for verification if professors request it.

## Sarmad's Full Profile (CRITICAL — use this for all email generation)

### PRIMARY NOVEL WORK — CollabForms FYP
- Supervised by Dr. Omer Usman Khan (FAST-NUCES Peshawar)
- Novel proximity-based spatial clustering algorithm for checkbox-label association in document forms
- Custom YOLOv11: 70% mAP@50, 112ms CPU inference
- Reflexion-inspired LLM refinement loop with persistent cross-session rule memory (extends Reflexion to cross-task transfer learning)
- Full-stack: Django, React, PostgreSQL, Docker, ONNX

### Independent Research — Diabetic Retinopathy
- NOT attributed to any supervisor (was a training program, not formal supervision)
- Developed SCDA (Spatial Channel Dual Attention) + DDA (Dynamic Depthwise Attention) mechanisms
- 97.22% accuracy, +5.91% over CIBM 2025 baseline
- Resolved Type 1 diabetes recall collapse: 50% → 96.9%
- First application of Lion optimizer to retinal pathology

### Production AI
- RAG pipelines + hallucination mitigation at Owlvest

### Technical Skills
- AI/ML: LLMs, RAG, CNN/ANN, Knowledge Distillation, NLP, Computer Vision, Transfer Learning, Attention Mechanisms
- Engineering: Scalable Pipelines, Inference Optimization, Git, Docker, Linux, Vercel
- Languages: Python (Expert), C/C++, JavaScript, SQL, TensorFlow, PyTorch

### Notable Projects
1. **Eco-Farm Tech (Kisan Saathi)** — React + Node.js + Supabase + Gemini API, multilingual AI chatbot, plant disease detection, deployed on Vercel
2. **Previsio** — Interactive ML platform with Streamlit, real-time model training
3. **Pneumonia Detector** — ANN 92% accuracy, Flask inference

### Achievements
- 🥇 1st Place: KPITB Digital Payment Challenge 2025 (National level)
- Finalist: NICAT Aerospace Hackathon
- ACM Coding Competition organizer

### Recommendation Letters Available
- ✅ Dr. Saif Ur Rehman Khan (DFKI Germany / CSU China) — research supervisor
- ✅ Dr. Omar Khan (FAST-NUCES, PhD Politecnico di Torino)
- ✅ Dr. Usman Abbasi (FAST-NUCES, Oxford-affiliated)

### GPA Framing (use ONLY if directly asked, never volunteer)
"While my GPA (64.9%) reflects challenges balancing coursework with intensive research, my independent research output — achieving 97.22% accuracy with novel SCDA/DDA attention mechanisms — demonstrates graduate-level capability."

## Email Generation Rules
### Subject Lines to Use
- "Prospective Masters Student — Medical AI Research Experience (IELTS 7.0)"
- "Research Inquiry: CNN Attention Mechanisms for Medical Imaging"
- "Graduate Application — DFKI Research Background in Medical AI"

### Always Emphasize
1. Research under DFKI-affiliated professor (Dr. Saif Ur Rehman Khan)
2. Novel SCDA/DDA contributions achieving 97.22% accuracy
3. IELTS 7.0
4. Production-level deployed systems
5. Available October 2026 or later

### Never Do
- Apologize for GPA upfront
- Use desperate language
- Send generic mass emails
- Mention GPA unless asked

## Context-Aware Email Angles (intelligence_layer.py)
- Medical imaging → SCDA/DDA attention mechanisms, 97.22% diabetic retinopathy accuracy
- Computer vision → ResNet50/VGG19 transfer learning, attention mechanisms
- Knowledge distillation / efficient AI → KDLight at DFKI, lightweight deployment
- LLM / RAG → Owlvest RAG pipeline + hallucination mitigation
- AI Safety → hallucination evaluation system at Owlvest
- Multimodal → Kisan Saathi (vision + language platform)
- NLP → LLM fine-tuning + low-latency inference
- Transfer learning → ResNet50/VGG19 on retinal datasets, +5.91% over baseline
- Default → SCDA/DDA research + DFKI affiliation as primary hook

## Directory Structure
```
/
├── main.py                      # CLI: discover | draft | send | followup | status | dashboard
├── config.py                    # All env vars (override=True)
├── requirements.txt
├── .env                         # Real keys — never commit
├── portfolio.md                 # Sarmad's full profile
├── targets.json                 # Professor targets (with match scores)
├── graph.json                   # Semantic relationship graph
├── outreach_tracker.json        # Email state per lab
├── utils/
│   ├── university_agent.py      # Top-50 unis by region (7 regions)
│   ├── research_agent.py        # Semantic Scholar paper fetching
│   ├── intelligence_layer.py    # Groq context-aware drafts
│   ├── matching_engine.py       # 0-100 match scoring
│   ├── semantic_graph.py        # RDF-style relationship graph
│   ├── profile_analyzer.py      # Reads resume + portfolio
│   ├── draft_manager.py         # Saves drafts to /drafts
│   ├── email_sender.py          # Gmail SMTP sending
│   └── outreach_tracker.py      # 10-14 day follow-up tracking
├── dashboard/
│   ├── app.py                   # Flask dashboard
│   └── templates/index.html     # Professor list + Kanban + Graph
├── drafts/                      # Review here
├── approved/                    # Move approved here
└── sent/                        # Archive
```

## CLI Commands
```bash
python main.py discover    # Search top-50 unis by region, score + graph professors
python main.py draft       # Research papers + generate personalized drafts
python main.py send        # Send approved emails via Gmail SMTP
python main.py followup    # Check no-response labs (10-14 day rule)
python main.py status      # Outreach summary
python main.py dashboard   # Web dashboard at http://localhost:5000
```

## Outreach Strategy
1. Search top-50 universities across 7 regions (USA, Germany, UK, Canada, Japan, China, Australia)
2. Filter: Professor + Associate Professor only (h-index >= 10, citations >= 500)
3. Score 0-100 against Sarmad's profile via MatchingEngine
4. Build semantic graph (professor → lab → research area)
5. Email ONE professor per lab at a time
6. No response in 10-14 days → move to next professor in same lab
7. Never email assistants or PhD students
8. Track all state in outreach_tracker.json

## Rate Limits
- Semantic Scholar: 1 req/sec — code uses time.sleep(2)
- Groq: 14,400 req/day — no issue
- Gmail SMTP: 500 emails/day — no issue

## Known Issues / Next Steps
- [x] Gmail SMTP working — sends to any address
- [x] Matching engine built (0-100 score)
- [x] Semantic graph built
- [x] Dashboard built (Flask, http://localhost:5000)
- [x] 216 universities across 28 regions (rank 1-50 + 100-300)
- [x] Discover uses paper search strategy (more reliable than author search)
- [x] Discover MERGES results — run multiple batches, all saved to same targets.json
- [x] LangGraph pipeline working
- [x] CrewAI pipeline working — 4 autonomous agents, self-correcting reviewer
- [x] Prescriptive feedback loop — reviewer gives exact fix text, not vague feedback
- [x] DeepSeek-V4-Flash + Qwen3.5 + Groq fallback chain
- [x] fix_affiliations.py — fixes missing university names after discover
- [x] targets_top50.json — backup of first batch (37 professors)
- [x] Pipeline visual page at localhost:5000/pipeline
- [x] Batch .bat files: START, DISCOVER, DRAFT, SEND, STATUS
- [ ] Fill in professor email addresses in targets.json
- [ ] Run DISCOVER.bat again for 100-300 batch (will auto-merge)
- [ ] Run fix_affiliations.py after each discover batch
- [ ] Generate drafts with: python main.py draft --crew
- [ ] Final degree certificate available June 2026
