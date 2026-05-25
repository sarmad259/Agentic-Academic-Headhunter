#!/usr/bin/env python3
"""
Professor Outreach Dashboard — Full Backend
Run: python dashboard/app.py
Open: http://localhost:5000
"""

import json, os, sys, smtplib, subprocess
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from flask import Flask, render_template, jsonify, request

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from dotenv import load_dotenv
load_dotenv(override=True)
from utils.outreach_tracker import OutreachTracker

app = Flask(__name__)
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def rpath(f): return os.path.join(ROOT, f)

def load_json(path):
    p = rpath(path)
    if os.path.exists(p):
        with open(p, encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_json(path, data):
    with open(rpath(path), "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

# ── Pages ──────────────────────────────────────────────────────────────────────

@app.route("/")
def index(): return render_template("index.html")

@app.route("/pipeline")
def pipeline(): return render_template("pipeline.html")

# ── Professors API ─────────────────────────────────────────────────────────────

@app.route("/api/professors")
def get_professors():
    targets = load_json("targets.json")
    profs = targets.get("professors", [])
    country  = request.args.get("country", "")
    area     = request.args.get("area", "")
    status   = request.args.get("status", "")
    min_score = request.args.get("min_score", 0, type=float)
    if country:  profs = [p for p in profs if p.get("country","").lower() == country.lower()]
    if area:     profs = [p for p in profs if any(area.lower() in k.lower() for k in p.get("research_keywords",[]))]
    if status:   profs = [p for p in profs if p.get("status","").lower() == status.lower()]
    if min_score: profs = [p for p in profs if float(p.get("match_score",0)) >= min_score]
    return jsonify(profs)

@app.route("/api/professors/<int:idx>", methods=["PATCH"])
def update_professor(idx):
    targets = load_json("targets.json")
    profs = targets.get("professors", [])
    if idx >= len(profs): return jsonify({"error": "not found"}), 404
    data = request.json
    profs[idx].update(data)
    save_json("targets.json", targets)
    return jsonify(profs[idx])

@app.route("/api/professors/<int:idx>/draft", methods=["POST"])
def generate_draft(idx):
    """Generate email draft for a single professor via Groq."""
    targets = load_json("targets.json")
    profs = targets.get("professors", [])
    if idx >= len(profs): return jsonify({"error": "not found"}), 404
    prof = profs[idx]

    try:
        from groq import Groq
        client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        keywords = ", ".join(prof.get("research_keywords", []))
        prompt = f"""Write a cold outreach email from Muhammad Sarmad Khan to {prof['name']} at {prof.get('institution', prof.get('university',''))}.

SARMAD'S PROFILE:
- Final year BS AI, FAST-NUCES Peshawar, Pakistan. IELTS 7.0.
- Research under Dr. Saif Ur Rehman Khan (DFKI Germany): developed SCDA + DDA attention mechanisms for diabetic retinopathy, achieving 97.22% accuracy (+5.91% over CIBM 2025 baseline). Resolved Type 1 diabetes recall collapse 50%→96.9%.
- Also built RAG pipelines + hallucination mitigation at Owlvest.
- Available October 2026+. Seeking fully funded Masters/PhD.

PROFESSOR RESEARCH AREAS: {keywords}

Write under 180 words. Reference their research area specifically. Connect to Sarmad's SCDA/DDA work. End with ask for funded position. No GPA mention. No flattery. Start with "Dear Prof. {prof['name'].split()[-1]}," — body only."""

        resp = client.chat.completions.create(
            model="llama-3.3-70b-versatile", max_tokens=400,
            messages=[{"role": "user", "content": prompt}]
        )
        draft = resp.choices[0].message.content

        # Save draft file
        os.makedirs(rpath("drafts"), exist_ok=True)
        safe = "".join(c if c.isalnum() else "_" for c in prof["name"])
        fname = f"{safe}_{datetime.now().strftime('%Y%m%d')}.md"
        fpath = rpath(f"drafts/{fname}")
        with open(fpath, "w", encoding="utf-8") as f:
            f.write(f"---\nName: {prof['name']}\nEmail: {prof.get('email','')}\n")
            f.write(f"Institution: {prof.get('institution', prof.get('university',''))}\n")
            f.write(f"Subject: Prospective Masters Student — Medical AI Research (SCDA/DDA, IELTS 7.0)\n---\n\n")
            f.write(draft)
            f.write(f"\n\n--\nMuhammad Sarmad Khan\nBS AI | FAST-NUCES Peshawar\nResearch: SCDA/DDA | Diabetic Retinopathy\nSupervisor: Dr. Saif Ur Rehman Khan (DFKI Germany)\nkhansardarms@gmail.com | IELTS 7.0")

        # Update status
        profs[idx]["status"] = "Draft Ready"
        profs[idx]["draft_file"] = fname
        save_json("targets.json", targets)

        return jsonify({"draft": draft, "file": fname})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/professors/<int:idx>/send", methods=["POST"])
def send_email(idx):
    """Send email to professor via Gmail SMTP."""
    targets = load_json("targets.json")
    profs = targets.get("professors", [])
    if idx >= len(profs): return jsonify({"error": "not found"}), 404
    prof = profs[idx]

    data = request.json
    body = data.get("body", "")
    subject = data.get("subject", "Prospective Masters Student — Medical AI Research (SCDA/DDA, IELTS 7.0)")
    recipient = prof.get("email", "")

    if not recipient or "[FILL" in recipient:
        return jsonify({"error": "Email address not set for this professor"}), 400

    sender = os.getenv("SENDER_EMAIL")
    password = os.getenv("GMAIL_APP_PASSWORD")

    full_body = f"""{body}

--
Muhammad Sarmad Khan
BS Artificial Intelligence | FAST-NUCES Peshawar
Research: SCDA/DDA Attention Mechanisms | Diabetic Retinopathy Detection
Supervisor: Dr. Saif Ur Rehman Khan (DFKI Germany)
khansardarms@gmail.com | IELTS 7.0"""

    try:
        msg = MIMEMultipart()
        msg["From"] = f"Muhammad Sarmad Khan <{sender}>"
        msg["To"] = recipient
        msg["Subject"] = subject
        msg.attach(MIMEText(full_body, "plain"))
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender, password)
            server.sendmail(sender, recipient, msg.as_string())

        profs[idx]["status"] = "Emailed"
        profs[idx]["last_contact"] = datetime.now().strftime("%Y-%m-%d")
        save_json("targets.json", targets)

        # Archive to sent
        os.makedirs(rpath("sent"), exist_ok=True)
        draft_file = prof.get("draft_file")
        if draft_file and os.path.exists(rpath(f"drafts/{draft_file}")):
            os.rename(rpath(f"drafts/{draft_file}"), rpath(f"sent/{draft_file}"))

        return jsonify({"success": True, "sent_to": recipient})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ── Drafts API ─────────────────────────────────────────────────────────────────

@app.route("/api/drafts")
def list_drafts():
    folder = rpath("drafts")
    if not os.path.exists(folder): return jsonify([])
    files = []
    for f in os.listdir(folder):
        if f.endswith(".md"):
            with open(os.path.join(folder, f), encoding="utf-8") as fp:
                content = fp.read()
            files.append({"filename": f, "content": content})
    return jsonify(files)

@app.route("/api/drafts/<filename>")
def get_draft(filename):
    path = rpath(f"drafts/{filename}")
    if not os.path.exists(path): return jsonify({"error": "not found"}), 404
    with open(path, encoding="utf-8") as f:
        return jsonify({"filename": filename, "content": f.read()})

@app.route("/api/drafts/<filename>", methods=["PUT"])
def update_draft(filename):
    path = rpath(f"drafts/{filename}")
    with open(path, "w", encoding="utf-8") as f:
        f.write(request.json.get("content", ""))
    return jsonify({"success": True})

# ── Stats & Filters ────────────────────────────────────────────────────────────

@app.route("/api/status")
def get_status():
    targets = load_json("targets.json")
    profs = targets.get("professors", [])
    statuses = {}
    for p in profs:
        s = p.get("status", "Pending")
        statuses[s] = statuses.get(s, 0) + 1
    drafts_count = len([f for f in os.listdir(rpath("drafts")) if f.endswith(".md")]) if os.path.exists(rpath("drafts")) else 0
    sent_count = len([f for f in os.listdir(rpath("sent")) if f.endswith(".md")]) if os.path.exists(rpath("sent")) else 0
    return jsonify({
        "total": len(profs),
        "by_status": statuses,
        "drafts_ready": drafts_count,
        "emails_sent": sent_count,
    })

@app.route("/api/filters")
def get_filters():
    targets = load_json("targets.json")
    profs = targets.get("professors", [])
    countries = sorted(set(p.get("country","") for p in profs if p.get("country","")))
    areas = sorted(set(kw for p in profs for kw in p.get("research_keywords",[])))
    statuses = sorted(set(p.get("status","Pending") for p in profs))
    return jsonify({"countries": countries, "areas": areas, "statuses": statuses})

@app.route("/api/graph")
def get_graph():
    return jsonify(load_json("graph.json"))

if __name__ == "__main__":
    print("Dashboard running at http://localhost:5000")
    app.run(debug=True, port=5000)
