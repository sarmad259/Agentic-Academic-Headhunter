import os
from dotenv import load_dotenv

load_dotenv(override=True)

# API Keys
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
RESEND_API_KEY = os.getenv("RESEND_API_KEY")
SEMANTIC_SCHOLAR_API_KEY = os.getenv("SEMANTIC_SCHOLAR_API_KEY")

# Email Configuration
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_NAME = os.getenv("SENDER_NAME")
GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")

# Semantic Scholar API
SEMANTIC_SCHOLAR_API = "https://api.semanticscholar.org/graph/v1"

# File Paths
RESUME_PATH = "resume.pdf"
PORTFOLIO_PATH = "portfolio.md"
TARGETS_PATH = "targets.json"
DRAFTS_FOLDER = "drafts"
APPROVED_FOLDER = "approved"

# Email Settings
MAX_EMAIL_LENGTH = 180   # words — raised to match prompts
PAPERS_PER_PROFESSOR = 3
MONTHS_LOOKBACK = 36     # 3 years — more papers to work with
