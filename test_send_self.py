"""
Test script: send a real test email to khansardarms@gmail.com
to verify the EmailSender is working correctly after upgrades.
Run: python test_send_self.py
"""
import os
from dotenv import load_dotenv

load_dotenv(override=True)

from utils.email_sender import EmailSender

sender = EmailSender(
    sender_email=os.getenv("SENDER_EMAIL"),
    sender_name=os.getenv("SENDER_NAME", "Muhammad Sarmad Khan")
)

TEST_EMAIL = "khansardarms@gmail.com"

body = """Dear Sarmad,

This is an automated test email from your Professor Outreach System.

If you are reading this, the pipeline is working correctly — including the upgraded EmailSender module with timezone-aware dispatch and self-improving prompt support.

The system is fully operational and ready for the next batch of professor outreach.

Best regards,
Your Agentic Pipeline"""

print("Sending test email to:", TEST_EMAIL)
success = sender.send_email(
    recipient_email=TEST_EMAIL,
    recipient_name="Sarmad (Test)",
    subject="[Pipeline Test] Professor Outreach System — Working Correctly",
    body=body
)

if success:
    print("\n✓ Test email sent successfully! Check your inbox at khansardarms@gmail.com")
else:
    print("\n✗ Test email failed — check GMAIL_APP_PASSWORD and SENDER_EMAIL in .env")
