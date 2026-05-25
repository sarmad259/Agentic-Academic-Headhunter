#!/usr/bin/env python3
"""
Professor Outreach System — Agentic Pipeline
============================================
Commands:
  python main.py discover        — Search top unis, find + score + graph professors
  python main.py draft           — LangGraph + DeepSeek/Qwen3: research→match→draft→review
  python main.py draft --crew    — CrewAI: 4 autonomous agents, self-reviewing
  python main.py draft --groq    — Groq/Llama direct (fastest)
  python main.py send            — Send approved emails via Gmail SMTP
  python main.py followup        — Check no-response labs (10-14 days)
  python main.py status          — Outreach tracker summary
  python main.py dashboard       — Web dashboard at http://localhost:5000
"""

import sys
import os
import json
from config import (
    GROQ_API_KEY, RESEND_API_KEY, SENDER_EMAIL, SENDER_NAME,
    SEMANTIC_SCHOLAR_API, SEMANTIC_SCHOLAR_API_KEY,
    RESUME_PATH, PORTFOLIO_PATH, TARGETS_PATH,
    DRAFTS_FOLDER, APPROVED_FOLDER,
    MAX_EMAIL_LENGTH, PAPERS_PER_PROFESSOR, MONTHS_LOOKBACK
)
from utils.profile_analyzer import ProfileAnalyzer
from utils.research_agent import ResearchAgent
from utils.intelligence_layer import IntelligenceLayer
from utils.draft_manager import DraftManager
from utils.email_sender import EmailSender
from utils.university_agent import UniversityAgent, TOP_50_UNIVERSITIES, SARMAD_RESEARCH_AREAS
from utils.outreach_tracker import OutreachTracker
from utils.matching_engine import MatchingEngine
from utils.semantic_graph import SemanticGraph

# LangGraph agent pipeline (uses Qwen3/DeepSeek via Ollama)
try:
    from agents.runner import run_pipeline_for_all
    LANGGRAPH_AVAILABLE = True
except ImportError:
    LANGGRAPH_AVAILABLE = False

# CrewAI pipeline (autonomous agents with self-review)
try:
    from crew.outreach_crew import run_crew_for_all
    CREWAI_AVAILABLE = True
except ImportError:
    CREWAI_AVAILABLE = False


def validate_env():
    missing = []
    if not GROQ_API_KEY:
        missing.append("GROQ_API_KEY")
    if not SENDER_EMAIL:
        missing.append("SENDER_EMAIL")
    if missing:
        print(f"Error: Missing environment variables: {', '.join(missing)}")
        sys.exit(1)


def run_discover_phase():
    """
    Full discovery pipeline:
    1. Search top unis × research areas via Semantic Scholar
    2. Filter to Professor / Associate Professor only
    3. Score each professor against Sarmad's profile (0-100)
    4. Build semantic relationship graph
    5. Save ranked results to targets.json + graph.json
    """
    print("=" * 60)
    print("PHASE 0: AGENTIC PROFESSOR DISCOVERY")
    print("=" * 60)

    # Configurable scan scope — scanning broadly for 300-400 professor targets
    unis_to_scan = TOP_50_UNIVERSITIES  # All 205 universities across 28 regions
    areas_to_scan = SARMAD_RESEARCH_AREAS  # All 10 research areas

    print(f"\nScanning {len(unis_to_scan)} universities × {len(areas_to_scan)} research areas")
    print(f"Regions: {', '.join(set(u['country'] for u in unis_to_scan))}")
    print(f"Areas: {', '.join(areas_to_scan)}")
    print("\nRate-limited to 1 req/sec — this will take a while. Go grab a coffee ☕\n")

    # Step 1: Discover
    agent = UniversityAgent(SEMANTIC_SCHOLAR_API, SEMANTIC_SCHOLAR_API_KEY)
    professors = agent.discover_professors(unis_to_scan, areas_to_scan, top_n=400)

    # Step 2: Match + score
    print("\n[Matching] Scoring professors against your profile...")
    engine = MatchingEngine()
    ranked = engine.rank_professors(professors)

    # Step 3: Build semantic graph
    print("[Graph] Building semantic relationship graph...")
    graph = SemanticGraph()
    graph.build(ranked)
    graph.save("graph.json")

    # Step 4: MERGE with existing targets.json (don't overwrite previous batches)
    existing = []
    if os.path.exists(TARGETS_PATH):
        try:
            with open(TARGETS_PATH) as f:
                existing_data = json.load(f)
                existing = existing_data.get("professors", [])
            print(f"\n  Found {len(existing)} existing professors in {TARGETS_PATH} — merging...")
        except Exception:
            existing = []

    # Deduplicate by authorId
    existing_ids = {
        p.get("authorId") or p.get("author_id")
        for p in existing
        if p.get("authorId") or p.get("author_id")
    }

    new_entries = []
    for p in ranked:
        aid = p.get("authorId")
        if aid and aid in existing_ids:
            continue
        new_entries.append({
            "name": p["name"],
            "email": "[FILL IN EMAIL]",
            "institution": p.get("university", ""),
            "country": p.get("country", ""),
            "research_keywords": areas_to_scan,
            "authorId": p["authorId"],
            "author_id": p["authorId"],
            "h_index": p.get("hIndex", 0),
            "citations": p.get("citationCount", 0),
            "match_score": p.get("match_score", 0),
            "overlap_areas": p.get("overlap_areas", []),
            "status": "Pending"
        })

    merged = existing + new_entries
    # Re-sort by match score
    merged.sort(key=lambda x: x.get("match_score", 0), reverse=True)

    with open(TARGETS_PATH, "w") as f:
        json.dump({"professors": merged}, f, indent=2)

    # Print new additions
    print(f"\n{'#':>3}  {'Name':<30} {'University':<30} {'Score':>6}  {'h-idx':>5}")
    print("-" * 80)
    for i, p in enumerate(new_entries[:20], 1):
        print(f"{i:>3}  {p['name']:<30} {p.get('institution',''):<30} {p.get('match_score',0):>6}  {p.get('h_index',0):>5}")
    if len(new_entries) > 20:
        print(f"  ... and {len(new_entries)-20} more")

    print(f"\n✓ {len(new_entries)} new professors added from this batch")
    print(f"✓ {len(existing)} existing professors kept")
    print(f"✓ Total: {len(merged)} professors in {TARGETS_PATH}")
    print(f"✓ Graph saved to graph.json ({len(graph.triples)} triples)")
    print("\n⚠ Fill in email addresses in targets.json, then run: python main.py draft")
    print("=" * 60)


def run_draft_phase():
    """Research professors and generate context-aware email drafts."""
    print("=" * 60)
    print("PHASE 1: RESEARCH & DRAFT")
    print("=" * 60)
    validate_env()

    print("\n[1/4] Analyzing your profile...")
    analyzer = ProfileAnalyzer(RESUME_PATH, PORTFOLIO_PATH)
    profile = analyzer.analyze_profile()
    print(f"  ✓ Skills: {len(profile['skills'])} | Interests: {len(profile['research_interests'])} | Projects: {len(profile['top_projects'])}")

    print("\n[2/4] Researching professors via Semantic Scholar...")
    agent = ResearchAgent(SEMANTIC_SCHOLAR_API, SEMANTIC_SCHOLAR_API_KEY)
    research_results = agent.research_all_professors(
        TARGETS_PATH, months_back=MONTHS_LOOKBACK, papers_limit=PAPERS_PER_PROFESSOR
    )
    print(f"\n  ✓ Researched {len(research_results)} professors")

    # Step 3: Generate drafts
    # --crew   → CrewAI (4 autonomous agents, self-reviewing)
    # --groq   → Groq direct (fast fallback)
    # default  → LangGraph + DeepSeek/Qwen3/Groq
    if "--crew" in sys.argv and CREWAI_AVAILABLE:
        print("\n[3/4] Running CrewAI — 4 autonomous agents (researcher→matcher→drafter→reviewer)...")
        drafts = run_crew_for_all(research_results)
    elif "--groq" in sys.argv or not LANGGRAPH_AVAILABLE:
        print("\n[3/4] Generating drafts with Groq/Llama...")
        intelligence = IntelligenceLayer(GROQ_API_KEY, MAX_EMAIL_LENGTH)
        drafts = intelligence.generate_all_drafts(profile, research_results)
    else:
        print("\n[3/4] Running LangGraph pipeline (researcher→matcher→drafter→reviewer→finalizer)...")
        drafts = run_pipeline_for_all(research_results, profile)
    successful = [d for d in drafts if d.get("draft")]
    print(f"\n  ✓ Generated {len(successful)} drafts")

    print(f"\n[4/4] Saving drafts to /{DRAFTS_FOLDER}...")
    manager = DraftManager(DRAFTS_FOLDER)
    saved = manager.save_all_drafts(drafts)

    print("\n" + "=" * 60)
    print(f"DONE: {len(saved)} drafts saved to /{DRAFTS_FOLDER}")
    print(f"Next: Review → move to /{APPROVED_FOLDER} → python main.py send")
    print("=" * 60)


def run_send_phase():
    """Send approved emails via Gmail SMTP, one per lab."""
    print("=" * 60)
    print("PHASE 2: SEND APPROVED EMAILS")
    print("=" * 60)
    validate_env()

    if not os.path.exists(APPROVED_FOLDER):
        print(f"No /{APPROVED_FOLDER} folder. Move approved drafts there first.")
        sys.exit(1)

    approved = [f for f in os.listdir(APPROVED_FOLDER) if f.endswith(".md")]
    if not approved:
        print(f"No approved drafts in /{APPROVED_FOLDER}")
        sys.exit(0)

    print(f"\nFound {len(approved)} approved email(s):")
    for f in approved:
        print(f"  - {f}")

    confirm = input("\nSend these emails? (yes/no): ").strip().lower()
    if confirm != "yes":
        print("Cancelled.")
        sys.exit(0)

    tracker = OutreachTracker()
    sender = EmailSender(sender_email=SENDER_EMAIL, sender_name=SENDER_NAME)
    results = sender.process_approved_drafts(APPROVED_FOLDER)

    for f in approved:
        tracker.data["emails_sent"].append({
            "file": f,
            "sent_at": __import__("datetime").datetime.now().isoformat()
        })
    tracker.save()

    print("\n" + "=" * 60)
    print(f"DONE: {results['sent']} sent, {results['failed']} failed")
    print("Run 'python main.py status' to see summary")
    print("=" * 60)


def run_followup_phase():
    """Check no-response labs (10-14 days) and queue next professor in same lab."""
    print("=" * 60)
    print("PHASE 3: FOLLOW-UP CHECK (10-14 day rule)")
    print("=" * 60)

    tracker = OutreachTracker()
    ready = tracker.get_labs_ready_for_followup(days_threshold=10)

    if not ready:
        print("\nNo labs ready for follow-up yet (< 10 days since last email).")
        return

    print(f"\n{len(ready)} lab(s) with no response after 10+ days:")
    for lab in ready:
        last = lab["history"][-1]
        print(f"  - {lab['university']} / {lab['research_area']}")
        print(f"    Last emailed: {last['professor']} on {last['emailed_at'][:10]}")

    confirm = input("\nMove to next professor in these labs? (yes/no): ").strip().lower()
    if confirm != "yes":
        print("Cancelled.")
        return

    for lab in ready:
        tracker.mark_no_response(lab["university"], lab["research_area"])
        next_prof = tracker.get_next_professor(lab["university"], lab["research_area"])
        if next_prof:
            print(f"  ✓ {lab['university']}: next → {next_prof['name']}")
        else:
            print(f"  ✗ {lab['university']}: lab exhausted")

    tracker.save()
    print("\nRun 'python main.py draft' to generate drafts for next round.")
    print("=" * 60)


def run_status():
    """Show outreach tracker summary."""
    print("=" * 60)
    print("OUTREACH STATUS")
    print("=" * 60)
    tracker = OutreachTracker()
    r = tracker.get_status_report()
    print(f"\n  Total labs     : {r['total_labs']}")
    print(f"  Pending        : {r['pending']}")
    print(f"  Emailed        : {r['emailed']}")
    print(f"  Responded      : {r['responded']}")
    print(f"  Exhausted      : {r['exhausted']}")
    print(f"  Emails sent    : {r['total_emails_sent']}")
    ready = tracker.get_labs_ready_for_followup(days_threshold=10)
    if ready:
        print(f"\n  ⚠ {len(ready)} lab(s) need follow-up (10+ days, no response)")
        print("  Run: python main.py followup")
    print("=" * 60)


def run_dashboard():
    """Launch the web dashboard."""
    print("Starting dashboard at http://localhost:5000 ...")
    print("Press Ctrl+C to stop.\n")
    os.system("python dashboard/app.py")


COMMANDS = {
    "discover": run_discover_phase,
    "draft": run_draft_phase,
    "send": run_send_phase,
    "followup": run_followup_phase,
    "status": run_status,
    "dashboard": run_dashboard,
}


def main():
    if len(sys.argv) < 2 or sys.argv[1] not in COMMANDS:
        print(__doc__)
        print(f"Available: {', '.join(COMMANDS.keys())}")
        sys.exit(1)
    COMMANDS[sys.argv[1]]()


if __name__ == "__main__":
    main()
