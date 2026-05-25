import os
import smtplib
import time as _time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict
from datetime import datetime, timedelta, timezone


# Country → approximate UTC offset (hours) for send-time optimization
COUNTRY_UTC_OFFSETS = {
    "USA": -5, "Canada": -5, "UK": 0, "Germany": 1, "France": 1,
    "Netherlands": 1, "Belgium": 1, "Switzerland": 1, "Austria": 1,
    "Sweden": 1, "Denmark": 1, "Norway": 1, "Finland": 2, "Italy": 1,
    "Spain": 1, "Poland": 1, "Czech Republic": 1, "Hungary": 1,
    "Portugal": 0, "Turkey": 3, "Japan": 9, "China": 8, "South Korea": 9,
    "Singapore": 8, "Hong Kong": 8, "Taiwan": 8, "Australia": 10,
    "New Zealand": 12,
}
OPTIMAL_SEND_HOUR = 8   # 08:30 AM local professor time
OPTIMAL_SEND_MIN  = 30


def _wait_until_optimal_time(country: str) -> None:
    """
    Sleep until 08:30 AM in the professor's local timezone.
    Falls back to sending immediately if the country is unknown or calculation fails.
    """
    try:
        offset_hours = COUNTRY_UTC_OFFSETS.get(country)
        if offset_hours is None:
            return  # Unknown country → send immediately (safe fallback)

        tz = timezone(timedelta(hours=offset_hours))
        now = datetime.now(tz)
        target = now.replace(hour=OPTIMAL_SEND_HOUR, minute=OPTIMAL_SEND_MIN,
                             second=0, microsecond=0)
        if now >= target:
            target += timedelta(days=1)  # Already past window; send next morning

        wait_seconds = (target - now).total_seconds()
        if wait_seconds > 0:
            wait_mins = int(wait_seconds / 60)
            print(f"  ⏰ Timezone-aware send: waiting {wait_mins}m until 08:30 {country} time...")
            _time.sleep(wait_seconds)
    except Exception:
        pass  # Silent fallback — never block the pipeline


class EmailSender:
    """Sends emails via Gmail SMTP (works for any address, no domain needed)."""

    def __init__(self, api_key: str = None, sender_email: str = None, sender_name: str = None):
        self.sender_email = sender_email or os.getenv("SENDER_EMAIL")
        self.sender_name = sender_name or os.getenv("SENDER_NAME", "Muhammad Sarmad Khan")
        self.app_password = os.getenv("GMAIL_APP_PASSWORD")

    def send_email(self, recipient_email: str, recipient_name: str, subject: str, body: str) -> bool:
        """Send a single email via Gmail SMTP."""
        # Skip invalid emails
        if not recipient_email or any(x in recipient_email for x in ["[FILL", "[SKIP", "[LOOKUP"]):
            print(f"  Skipping {recipient_name} — no valid email address")
            return False

        full_body = f"""{body}

--
Muhammad Sarmad Khan
BS Artificial Intelligence | FAST-NUCES Peshawar
FYP: CollabForms (YOLOv11 + Novel Spatial Clustering) | Independent Research: SCDA/DDA (97.22% accuracy)
khansardarms@gmail.com | IELTS 7.0 | Available Oct 2026"""

        try:
            msg = MIMEMultipart()
            msg["From"] = f"{self.sender_name} <{self.sender_email}>"
            msg["To"] = recipient_email
            msg["Subject"] = subject
            msg.attach(MIMEText(full_body, "plain"))

            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                server.login(self.sender_email, self.app_password)
                server.sendmail(self.sender_email, recipient_email, msg.as_string())

            print(f"  OK Sent to {recipient_name} ({recipient_email})")
            return True

        except Exception as e:
            print(f"  FAIL {recipient_name}: {e}")
            return False

    def process_approved_drafts(self, approved_folder: str) -> Dict:
        """Send all emails from approved folder."""
        if not os.path.exists(approved_folder):
            print(f"No approved folder found at {approved_folder}")
            return {"sent": 0, "failed": 0, "skipped": 0}

        sent_count = 0
        failed_count = 0
        skipped_count = 0

        for filename in sorted(os.listdir(approved_folder)):
            if not filename.endswith(".md"):
                continue

            filepath = os.path.join(approved_folder, filename)

            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()

                metadata, body = self._parse_draft(content)

                email = metadata.get("email", "")
                name = metadata.get("name", filename)

                # Skip invalid emails
                if not email or any(x in email for x in ["[FILL", "[SKIP", "[LOOKUP"]):
                    print(f"  SKIP {name} — no valid email ({email})")
                    skipped_count += 1
                    continue

                subject = metadata.get("subject", "Prospective Masters Student — AI Research (IELTS 7.0)")
                country = metadata.get("country", "")

                # Timezone-aware: wait until 08:30 AM professor's local time (fallback: send now)
                _wait_until_optimal_time(country)

                success = self.send_email(
                    recipient_email=email,
                    recipient_name=name,
                    subject=subject,
                    body=body
                )

                if success:
                    sent_count += 1
                    # Move to sent folder
                    sent_folder = os.path.join(os.path.dirname(approved_folder), "sent")
                    os.makedirs(sent_folder, exist_ok=True)
                    os.rename(filepath, os.path.join(sent_folder, filename))
                else:
                    failed_count += 1

            except Exception as e:
                print(f"  ERROR processing {filename}: {e}")
                failed_count += 1

        return {"sent": sent_count, "failed": failed_count, "skipped": skipped_count}

    def _parse_draft(self, content: str) -> tuple:
        """Parse draft markdown to extract metadata and body."""
        lines = content.split("\n")
        metadata = {}
        body_start = 0

        if lines[0].strip() == "---":
            for i, line in enumerate(lines[1:], 1):
                if line.strip() == "---":
                    body_start = i + 1
                    break
                if ":" in line:
                    key, value = line.split(":", 1)
                    metadata[key.strip().lower()] = value.strip()

        body = "\n".join(lines[body_start:]).strip()

        # Extract just the email body (after ## Email Body header)
        if "## Email Body" in body:
            body = body.split("## Email Body")[-1].strip()

        # Remove trailing instructions
        if "---" in body:
            body = body.split("---")[0].strip()

        return metadata, body
