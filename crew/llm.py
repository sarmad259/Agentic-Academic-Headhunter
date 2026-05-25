"""
LLM selector for CrewAI agents.
Priority: DeepSeek-V4-Flash → Qwen3.5 → Groq
"""

import os
import requests
from dotenv import load_dotenv
load_dotenv(override=True)


def get_llm():
    """Return the best available LLM for CrewAI agents."""

    # Try DeepSeek-V4-Flash (cloud) via Ollama
    try:
        r = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": "deepseek-v4-flash:cloud", "prompt": "hi", "stream": False},
            timeout=20
        )
        if r.status_code == 200:
            print("  [LLM] DeepSeek-V4-Flash (Ollama cloud)")
            from crewai import LLM
            return LLM(model="ollama/deepseek-v4-flash:cloud", base_url="http://localhost:11434")
    except Exception:
        pass

    # Try Qwen3.5 397B
    try:
        r = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": "qwen3.5:397b-cloud", "prompt": "hi", "stream": False},
            timeout=20
        )
        if r.status_code == 200:
            print("  [LLM] Qwen3.5-397B (Ollama cloud)")
            from crewai import LLM
            return LLM(model="ollama/qwen3.5:397b-cloud", base_url="http://localhost:11434")
    except Exception:
        pass

    # Groq fallback
    print("  [LLM] Groq/Llama-3.3-70b (fallback)")
    from crewai import LLM
    return LLM(
        model="groq/llama-3.3-70b-versatile",
        api_key=os.getenv("GROQ_API_KEY")
    )
