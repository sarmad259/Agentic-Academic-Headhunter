import os
from typing import Dict, List
from datetime import datetime


class DraftManager:
    """Manages email drafts — saving, organizing, and tracking."""

    def __init__(self, drafts_folder: str):
        self.drafts_folder = drafts_folder
        os.makedirs(drafts_folder, exist_ok=True)

    def save_draft(self, draft: Dict) -> str:
        professor = draft["professor"]
        filename = self._create_filename(professor.get("name", "unknown"))
        filepath = os.path.join(self.drafts_folder, filename)
        content = self._format_draft(draft)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"  ✓ Saved: {filename}")
        return filepath

    def save_all_drafts(self, drafts: List[Dict]) -> List[str]:
        filepaths = []
        for draft in drafts:
            if draft.get("draft"):
                try:
                    filepath = self.save_draft(draft)
                    filepaths.append(filepath)
                except Exception as e:
                    print(f"  ✗ Failed to save draft for {draft.get('professor', {}).get('name', '?')}: {e}")
        return filepaths

    def _create_filename(self, professor_name: str) -> str:
        safe_name = "".join(c if c.isalnum() else "_" for c in professor_name)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"{safe_name}_{timestamp}.md"

    def _format_draft(self, draft: Dict) -> str:
        professor = draft["professor"]
        papers = draft.get("papers_referenced", [])

        # Safe field access — discovered professors may not have email yet
        name = professor.get("name", "Unknown")
        email = professor.get("email", "[EMAIL NOT SET]")
        institution = professor.get("institution") or professor.get("university", "Unknown")
        keywords = ", ".join(professor.get("research_keywords", []))
        subject = draft.get("subject", "Prospective Masters Student — Medical AI Research (SCDA/DDA, IELTS 7.0)")
        context = draft.get("context_used", "default")
        status = draft.get("status", "")

        content = f"""---
Name: {name}
Email: {email}
Institution: {institution}
Subject: {subject}
Context: {context}
Status: {status}
Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
---

# Email Draft — {name}

**Institution:** {institution}
**Email:** {email}
**Research:** {keywords}
**Match Score:** {professor.get("match_score", "N/A")}

## Referenced Papers
"""
        for i, paper in enumerate(papers[:3], 1):
            content += f"\n{i}. **{paper.get('title', 'Untitled')}** ({paper.get('year', 'N/A')}, {paper.get('citationCount', 0)} citations)\n"

        content += f"\n## Email Body\n\n{draft['draft']}\n\n"
        content += "---\n"
        content += "**Next steps:** Review → edit if needed → move to `/approved` → `python main.py send`\n"
        return content
