"""
ai_helper.py
Optional helper. If OPENAI_API_KEY isn't set, it returns a friendly message.
"""

import os

try:
    import openai
except Exception:
    openai = None  # still let the app run


def call_ai(prompt: str, max_tokens: int = 150):
    key = os.getenv("OPENAI_API_KEY")
    if not key or not openai:
        return "AI disabled (no OPENAI_API_KEY or openai package unavailable)."
    openai.api_key = key
    try:
        # Adjust model string to whatever you have access to.
        resp = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[{"role": "system", "content": "Be concise and helpful."},
                      {"role": "user", "content": prompt}],
            max_tokens=max_tokens,
            temperature=0.2
        )
        return resp["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return f"OpenAI error: {e}"
