#!/usr/bin/env python3
"""Send a test email to verify the full pipeline works."""

import os
from dotenv import load_dotenv
load_dotenv()

import resend

resend.api_key = os.getenv("RESEND_API_KEY")
sender_email = os.getenv("SENDER_EMAIL")
sender_name = os.getenv("SENDER_NAME")

print(f"Sending test email to {sender_email}...")
# On Resend free tier without a verified domain, 'to' must be your Resend account email
resend_account_email = os.getenv("RESEND_ACCOUNT_EMAIL") or os.getenv("SENDER_EMAIL")

try:
    response = resend.Emails.send({
        "from": f"Professor Outreach System <onboarding@resend.dev>",
        "to": [resend_account_email],
        "subject": "✓ Professor Outreach System — Test Email",
        "text": f"""Hi {sender_name},

This is a test email from your Professor Outreach System.

If you're reading this, your Resend API key is working correctly and the system is ready to send emails.

— Professor Outreach System
"""
    })
    print(f"✓ Email sent! ID: {response['id']}")
    print(f"  Check your inbox at {sender_email}")
except Exception as e:
    print(f"✗ Failed: {e}")
