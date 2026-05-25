#!/usr/bin/env python3
"""Quick test to verify all API keys are working."""

import os
from dotenv import load_dotenv

load_dotenv()

def test_groq():
    from groq import Groq
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": "Say 'Groq OK' and nothing else."}],
        max_tokens=10
    )
    print(f"✓ Groq: {response.choices[0].message.content.strip()}")

def test_resend():
    import resend
    resend.api_key = os.getenv("RESEND_API_KEY")
    # Just validate the key by listing domains (no email sent)
    domains = resend.Domains.list()
    print(f"✓ Resend: API key valid")

def test_semantic_scholar():
    import requests
    r = requests.get("https://api.semanticscholar.org/graph/v1/author/search?query=Yann+LeCun&limit=1")
    r.raise_for_status()
    name = r.json()['data'][0]['name']
    print(f"✓ Semantic Scholar: found '{name}'")

if __name__ == "__main__":
    print("Testing API connections...\n")
    for name, fn in [("Groq", test_groq), ("Resend", test_resend), ("Semantic Scholar", test_semantic_scholar)]:
        try:
            fn()
        except Exception as e:
            print(f"✗ {name}: {e}")
