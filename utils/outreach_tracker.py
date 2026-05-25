import json
import os
from datetime import datetime
from typing import Dict, List, Optional

TRACKER_FILE = "outreach_tracker.json"

class OutreachTracker:
    """
    Tracks email outreach state per lab.
    Strategy:
    - Email the top professor in a lab first
    - If no response after N days, move to next professor in same lab
    - Never email assistants (TAs/PhD students)
    - One email at a time per lab
    """

    def __init__(self, tracker_path: str = TRACKER_FILE):
        self.tracker_path = tracker_path
        self.data = self._load()

    def _load(self) -> Dict:
        if os.path.exists(self.tracker_path):
            with open(self.tracker_path, "r") as f:
                return json.load(f)
        return {"labs": {}, "emails_sent": [], "last_updated": None}

    def save(self):
        self.data["last_updated"] = datetime.now().isoformat()
        with open(self.tracker_path, "w") as f:
            json.dump(self.data, f, indent=2)

    def get_lab_key(self, university: str, research_area: str) -> str:
        return f"{university}::{research_area}"

    def register_lab(self, university: str, research_area: str, professors: List[Dict]):
        """Register a lab with its ranked list of professors to contact."""
        key = self.get_lab_key(university, research_area)
        if key not in self.data["labs"]:
            self.data["labs"][key] = {
                "university": university,
                "research_area": research_area,
                "professors": professors,  # ordered: full/assoc first
                "current_index": 0,
                "status": "pending",  # pending | emailed | responded | exhausted
                "history": []
            }
            self.save()

    def get_next_professor(self, university: str, research_area: str) -> Optional[Dict]:
        """Get the next professor to email in this lab."""
        key = self.get_lab_key(university, research_area)
        lab = self.data["labs"].get(key)
        if not lab:
            return None

        idx = lab["current_index"]
        if idx >= len(lab["professors"]):
            lab["status"] = "exhausted"
            self.save()
            return None

        return lab["professors"][idx]

    def mark_emailed(self, university: str, research_area: str, professor_name: str, draft_file: str):
        """Mark a professor as emailed."""
        key = self.get_lab_key(university, research_area)
        lab = self.data["labs"].get(key)
        if not lab:
            return

        lab["history"].append({
            "professor": professor_name,
            "emailed_at": datetime.now().isoformat(),
            "draft_file": draft_file,
            "response": None
        })
        lab["status"] = "emailed"
        self.save()

        # Also log in global sent list
        self.data["emails_sent"].append({
            "professor": professor_name,
            "university": university,
            "research_area": research_area,
            "sent_at": datetime.now().isoformat()
        })
        self.save()

    def mark_no_response(self, university: str, research_area: str):
        """Move to next professor in the same lab (no response received)."""
        key = self.get_lab_key(university, research_area)
        lab = self.data["labs"].get(key)
        if not lab:
            return

        lab["current_index"] += 1
        lab["status"] = "pending"

        if lab["current_index"] >= len(lab["professors"]):
            lab["status"] = "exhausted"
            print(f"  Lab exhausted: {university} / {research_area}")

        self.save()

    def mark_responded(self, university: str, research_area: str, professor_name: str):
        """Mark that a professor responded."""
        key = self.get_lab_key(university, research_area)
        lab = self.data["labs"].get(key)
        if not lab:
            return

        lab["status"] = "responded"
        for entry in lab["history"]:
            if entry["professor"] == professor_name:
                entry["response"] = "received"
        self.save()

    def get_status_report(self) -> Dict:
        """Summary of all outreach activity."""
        total_labs = len(self.data["labs"])
        emailed = sum(1 for l in self.data["labs"].values() if l["status"] == "emailed")
        responded = sum(1 for l in self.data["labs"].values() if l["status"] == "responded")
        exhausted = sum(1 for l in self.data["labs"].values() if l["status"] == "exhausted")
        pending = sum(1 for l in self.data["labs"].values() if l["status"] == "pending")

        return {
            "total_labs": total_labs,
            "pending": pending,
            "emailed": emailed,
            "responded": responded,
            "exhausted": exhausted,
            "total_emails_sent": len(self.data["emails_sent"])
        }

    def get_labs_ready_for_followup(self, days_threshold: int = 10) -> List[Dict]:
        """Return labs where email was sent but no response after N days."""
        from datetime import timedelta
        ready = []
        for key, lab in self.data["labs"].items():
            if lab["status"] != "emailed":
                continue
            if not lab["history"]:
                continue
            last = lab["history"][-1]
            sent_at = datetime.fromisoformat(last["emailed_at"])
            if datetime.now() - sent_at >= timedelta(days=days_threshold):
                ready.append(lab)
        return ready
