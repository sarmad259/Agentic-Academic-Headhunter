# Professor Outreach System

An AI-powered system that personalizes and automates academic networking using agentic intelligence.

## Features

- **Profile Analysis**: Extracts skills, research interests, and projects from your resume and portfolio
- **Research Agent**: Uses Semantic Scholar API to find professors' most cited recent papers
- **Intelligence Layer**: Claude generates personalized emails linking your work to their research
- **Human-in-the-Loop**: Review and approve all drafts before sending
- **Automated Sending**: Brevo API sends approved emails

## Directory Structure

```
professor-outreach/
├── main.py                 # Main CLI entry point
├── config.py              # Configuration and environment variables
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
├── resume.pdf            # Your resume (add your actual file)
├── portfolio.md          # Your portfolio (fill in template)
├── targets.json          # List of professors to contact
├── utils/
│   ├── profile_analyzer.py    # Extracts info from resume/portfolio
│   ├── research_agent.py      # Semantic Scholar API integration
│   ├── intelligence_layer.py  # Claude email generation
│   ├── draft_manager.py       # Saves and organizes drafts
│   └── email_sender.py        # Brevo email sending
├── drafts/               # Generated email drafts (review here)
├── approved/             # Move approved drafts here
└── sent/                 # Sent emails archived here
```

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment

Copy `.env.example` to `.env` and fill in:

```bash
cp .env.example .env
```

Required variables:
- `ANTHROPIC_API_KEY`: Get from https://console.anthropic.com/
- `BREVO_API_KEY`: Get from https://app.brevo.com/ (free tier available)
- `SENDER_EMAIL`: Your email address
- `SENDER_NAME`: Your name

### 3. Prepare Your Files

**resume.pdf**: Replace the placeholder with your actual PDF resume

**portfolio.md**: Fill in the template with:
- Technical skills
- Research interests
- Top 3 projects with descriptions and technologies

**targets.json**: Add professors you want to contact:

```json
{
  "professors": [
    {
      "name": "Dr. Jane Smith",
      "email": "jane.smith@university.edu",
      "institution": "MIT",
      "research_keywords": ["machine learning", "computer vision"]
    }
  ]
}
```

## Usage

### Phase 1: Research and Draft

Generate personalized email drafts:

```bash
python main.py draft
```

This will:
1. Analyze your resume and portfolio
2. Research each professor via Semantic Scholar
3. Find their 3 most cited papers from the last 24 months
4. Generate personalized emails with Claude
5. Save drafts to `/drafts` folder

### Phase 2: Review and Approve

1. Open files in `/drafts` folder
2. Review each email draft
3. Edit as needed
4. Move approved drafts to `/approved` folder

### Phase 3: Send Emails

Send all approved emails:

```bash
python main.py send
```

This will:
1. Show you all approved emails
2. Ask for confirmation
3. Send via Brevo API
4. Move sent emails to `/sent` folder

## Email Generation Rules

Each email:
- Links a specific methodology from their research to your skills/projects
- Professional, inquisitive tone
- Under 150 words
- References their most cited recent paper
- Asks a thoughtful question

## API Information

- **Semantic Scholar**: Free, no API key required
- **Anthropic Claude**: Requires API key, pay-per-use
- **Brevo**: Free tier includes 300 emails/day

## Troubleshooting

**"Could not read resume PDF"**: Ensure `resume.pdf` is a valid PDF file

**"Author not found"**: Check professor name spelling in `targets.json`

**"No recent papers found"**: Professor may not have publications in last 24 months

**Email sending fails**: Verify Brevo API key and sender email are correct

## Customization

Edit `config.py` to adjust:
- `MAX_EMAIL_LENGTH`: Word limit for emails (default: 150)
- `PAPERS_PER_PROFESSOR`: Papers to analyze (default: 3)
- `MONTHS_LOOKBACK`: How far back to search (default: 24)

## License

MIT
