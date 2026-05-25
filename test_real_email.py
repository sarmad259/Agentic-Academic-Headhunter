#!/usr/bin/env python3
"""Test the updated email generation on Prof. Cho (computer vision / spatial reasoning)."""

import os, smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
load_dotenv(override=True)

from utils.intelligence_layer import IntelligenceLayer

il = IntelligenceLayer(os.getenv("GROQ_API_KEY"))

prof = {
    "name": "Minsu Cho",
    "institution": "POSTECH",
    "research_keywords": ["computer vision", "object detection", "spatial reasoning", "human object interaction"]
}

papers = [{
    "title": "Relational Context Learning for Human-Object Interaction Detection",
    "year": 2023,
    "citationCount": 89,
    "abstract": "We propose a transformer-based architecture with two decoder branches that model relational context — spatial and semantic relationships between humans and objects — for HOI detection, achieving state-of-the-art on HICO-DET and V-COCO benchmarks."
}]

result = il.generate_email_draft({}, {"professor": prof, "papers": papers})

print("--- DRAFT ---")
print(result["draft"])
print(f"\nWords: {len(result['draft'].split())}")
print(f"Angle: {result.get('context_used')}")
print(f"Subject: {result.get('subject')}")

draft = result["draft"]
checks = {
    "Specific technique named": any(t in draft for t in ["Relational Context", "dual decoder", "two decoder", "HOI", "relational context"]),
    "Sarmad work named": any(t in draft for t in ["SCDA", "DDA", "CollabForms", "spatial clustering", "YOLOv11"]),
    "Exact number": any(t in draft for t in ["97.22", "5.91", "96.9", "70%", "112ms"]),
    "IELTS": "IELTS" in draft,
    "October 2026": "2026" in draft,
    "Funding ask": any(t in draft.lower() for t in ["funded", "position", "phd", "masters"]),
    "No flattery": not any(t in draft.lower() for t in ["deeply inspired", "renowned", "prestigious", "writing to express"]),
    "Under 180 words": len(draft.split()) <= 180,
}

print("\n--- QUALITY CHECKS ---")
for check, passed in checks.items():
    print(f"  {'OK' if passed else 'FAIL'} {check}")

send = input("\nSend to Gmail for review? (y/n): ").strip().lower()
if send == "y":
    sender = os.getenv("SENDER_EMAIL")
    password = os.getenv("GMAIL_APP_PASSWORD")
    full = f"""{draft}\n\n--\nMuhammad Sarmad Khan\nBS AI | FAST-NUCES Peshawar\nSCDA/DDA + CollabForms Research\nDFKI Germany | khansardarms@gmail.com | IELTS 7.0"""
    msg = MIMEMultipart()
    msg["From"] = f"Muhammad Sarmad Khan <{sender}>"
    msg["To"] = "khansardarms@gmail.com"
    msg["Subject"] = result.get("subject", "Test Draft")
    msg.attach(MIMEText(full, "plain"))
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as s:
        s.login(sender, password)
        s.sendmail(sender, "khansardarms@gmail.com", msg.as_string())
    print("Sent to khansardarms@gmail.com")
