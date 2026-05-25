#!/usr/bin/env python3
"""Send a job application email to tofail.khan@nu.edu.pk via Gmail SMTP."""

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
load_dotenv(override=True)

from groq import Groq

# --- Generate email with Groq ---
print("Generating job application email...")

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

prompt = """Write a professional job application email from Muhammad Sarmad Khan to a professor/faculty member at FAST-NUCES.

ABOUT SARMAD:
- BS AI student at FAST-NUCES Peshawar (2022-2026)
- Research Trainee at DFKI Germany — benchmarked CNN/ResNet/ViT for brain tumor diagnosis, implemented KDLight knowledge distillation
- AI Engineer at Owlvest — built RAG pipelines, fine-tuned LLMs, designed hallucination mitigation systems
- Projects: Pneumonia Detector (92% accuracy), Kisan Saathi (AI agri platform), Brain Tumor Benchmarking
- Skills: PyTorch, TensorFlow, Python, RAG, Knowledge Distillation, Computer Vision

RECIPIENT: Dr. Tofail Khan, Faculty at FAST-NUCES

TASK:
Write a compelling job/research position application email (under 200 words) that:
1. Mentions his DFKI research experience as the strongest hook
2. Highlights his RAG + LLM production experience at Owlvest
3. Expresses interest in contributing to the department as a research assistant or lab collaborator
4. Ends with a clear ask — a meeting or call to discuss opportunities

Tone: confident, professional, concise. No flattery.
Start with "Dear Dr. Khan," — write only the email body, no subject line."""

response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    max_tokens=400,
    messages=[{"role": "user", "content": prompt}]
)

email_body = response.choices[0].message.content

full_email = f"""{email_body}

--
Muhammad Sarmad Khan
BS Artificial Intelligence | FAST-NUCES Peshawar
Research Trainee | DFKI Germany
khansardarms@gmail.com | p229009@pwr.nu.edu.pk"""

print("\n--- GENERATED EMAIL ---")
print(full_email)
print("-----------------------\n")

# --- Send via Gmail SMTP ---
sender_email = os.getenv("SENDER_EMAIL")
app_password = os.getenv("GMAIL_APP_PASSWORD")
recipient = "tufail.khan@nu.edu.pk"

if not app_password or app_password == "your_gmail_app_password_here":
    print("⚠ GMAIL_APP_PASSWORD not set in .env")
    print("\nTo get one:")
    print("  1. Go to myaccount.google.com/security")
    print("  2. Enable 2-Step Verification")
    print("  3. Search 'App Passwords' → create one for 'Mail'")
    print("  4. Paste the 16-char password into .env as GMAIL_APP_PASSWORD")
else:
    print(f"Sending to {recipient} via Gmail SMTP...")
    msg = MIMEMultipart()
    msg["From"] = f"Muhammad Sarmad Khan <{sender_email}>"
    msg["To"] = recipient
    msg["Subject"] = "Research/Teaching Assistant Opportunity — Muhammad Sarmad Khan (DFKI Research Trainee)"
    msg.attach(MIMEText(full_email, "plain"))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, app_password)
            server.sendmail(sender_email, recipient, msg.as_string())
        print(f"✓ Email sent to {recipient}")
    except Exception as e:
        print(f"✗ Failed: {e}")
