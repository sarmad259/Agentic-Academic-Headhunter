"""
CrewAI Agents for Professor Outreach System.
Each agent has a role, goal, and backstory — they collaborate autonomously.
"""

from crewai import Agent
from crew.llm import get_llm


def make_agents():
    llm = get_llm()

    researcher = Agent(
        role="Academic Research Analyst",
        goal=(
            "Find and summarize the most relevant and recent research work of a professor. "
            "Identify their key methodologies, specific techniques, and research direction."
        ),
        backstory=(
            "You are an expert at reading academic papers and extracting the core technical "
            "contributions. You know how to identify what makes a paper novel and what specific "
            "techniques a professor is known for. You always cite specific paper titles and methods."
        ),
        llm=llm,
        verbose=True,
        allow_delegation=False,
    )

    matcher = Agent(
        role="Research Profile Matcher",
        goal=(
            "Find the strongest connection between a professor's research and "
            "Sarmad Khan's profile. Identify the most compelling overlap to use in outreach."
        ),
        backstory=(
            "You are a strategic academic advisor who specializes in identifying research synergies. "
            "You know Sarmad's work deeply: SCDA/DDA attention mechanisms for diabetic retinopathy "
            "(97.22% accuracy, +5.91% over CIBM 2025 baseline, recall collapse fix 50%→96.9%), "
            "RAG pipelines at Owlvest, and Kisan Saathi multimodal platform. "
            "You always find the most specific, genuine connection — never generic."
        ),
        llm=llm,
        verbose=True,
        allow_delegation=False,
    )

    drafter = Agent(
        role="Academic Email Specialist",
        goal=(
            "Write a highly personalized, professional cold outreach email from Sarmad Khan "
            "to a professor. The email must be specific, concise, and compelling."
        ),
        backstory=(
            "You are an expert at writing cold academic outreach emails that actually get replies. "
            "You know that professors ignore generic emails. You always reference a specific technique "
            "from their paper by name, connect it to Sarmad's SCDA/DDA work with exact numbers, "
            "and make a clear ask. You never use flattery, never mention GPA, always stay under 180 words."
        ),
        llm=llm,
        verbose=True,
        allow_delegation=False,
    )

    reviewer = Agent(
        role="Quality Control Reviewer",
        goal=(
            "Review the email draft and ensure it meets all quality standards. "
            "If it fails, rewrite it yourself to pass all checks."
        ),
        backstory=(
            "You are a strict quality reviewer who has seen thousands of academic cold emails. "
            "You check: specific technique named? SCDA/DDA or 97.22% mentioned? Under 180 words? "
            "No flattery? No GPA? Clear funding ask? IELTS 7.0? October 2026? "
            "If the draft fails ANY check, you rewrite it yourself — you never delegate, "
            "you never just give feedback, you always output a complete email."
        ),
        llm=llm,
        verbose=True,
        allow_delegation=False,  # No delegation — reviewer fixes it directly
    )

    return researcher, matcher, drafter, reviewer
