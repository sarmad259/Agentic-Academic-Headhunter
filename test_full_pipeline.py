#!/usr/bin/env python3
"""
Full pipeline test: Generate a personalized email for a fake Japanese professor
and send it to pool44384@gmail.com
"""

import os
from dotenv import load_dotenv
load_dotenv(override=True)

from groq import Groq
import resend

# --- Fake professor (Japanese, medical imaging) ---
professor = {
    "name": "Dr. Hiroshi Tanaka",
    "email": "khansardarms@gmail.com",  # Resend free tier: can only send to registered email
    "institution": "University of Tokyo",
    "research_keywords": ["medical imaging", "deep learning", "brain tumor segmentation"]
}

fake_paper = {
    "title": "Efficient Vision Transformer Pruning for Real-Time Brain Tumor Segmentation",
    "year": 2024,
    "citationCount": 87,
    "abstract": "We propose a structured pruning methodology for Vision Transformers (ViT) applied to brain MRI segmentation, achieving 3x inference speedup with less than 1% accuracy drop using a teacher-student distillation framework."
}

# --- Generate email with Groq ---
print("Generating personalized email with Groq/Llama...")

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

prompt = f"""You are helping Muhammad Sarmad Khan, a BS AI student at FAST-NUCES Pakistan, write a cold outreach email to a professor for a research/PhD position.

SARMAD'S RELEVANT ANGLE:
- He is a Research Trainee at DFKI Germany under Dr. Saif Ur Rehman
- He benchmarked CNN, ResNet, and ViT for brain tumor diagnosis
- He implemented KDLight knowledge distillation for lightweight model deployment
- He wants to discuss how his distillation work relates to the professor's ViT pruning research

PROFESSOR:
- Name: {professor['name']}
- Institution: {professor['institution']}

THEIR RECENT PAPER:
- Title: "{fake_paper['title']}" ({fake_paper['year']}, {fake_paper['citationCount']} citations)
- Abstract: {fake_paper['abstract']}

TASK:
Write a cold outreach email (under 150 words) that:
1. References the teacher-student distillation framework from their paper specifically
2. Connects it to Sarmad's KDLight implementation at DFKI
3. Asks for a brief research discussion or call
4. Tone: professional, direct, no flattery

Write only the email body starting with "Dear Prof. Tanaka,". No subject line, no signature."""

response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    max_tokens=400,
    messages=[{"role": "user", "content": prompt}]
)

email_body = response.choices[0].message.content
print("\n--- GENERATED EMAIL ---")
print(email_body)
print("-----------------------\n")

# --- Send via Resend ---
print(f"Sending to {professor['email']}...")

resend.api_key = os.getenv("RESEND_API_KEY")

full_email = f"""{email_body}

--
Muhammad Sarmad Khan
BS Artificial Intelligence | FAST-NUCES Peshawar
Research Trainee | DFKI Germany
khansardarms@gmail.com"""

r = resend.Emails.send({
    "from": "onboarding@resend.dev",
    "to": [professor["email"]],
    "subject": f"Research Inquiry — {fake_paper['title'][:55]}...",
    "text": full_email
})

print(f"✓ Email sent! ID: {r['id']}")
print(f"  Check inbox: {professor['email']}")
