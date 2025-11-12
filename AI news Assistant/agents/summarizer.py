import os
import requests
import html

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
OPENROUTER_KEY = os.getenv("OPENROUTER_API_KEY")
MISTRAL_MODEL = os.getenv("MISTRAL_MODEL", "mistralai/mistral-7b-instruct")

def summarise_text(text: str, max_tokens: int = 220) -> str:
    """
    Summarize text using OpenRouter Mistral model.
    Produces short factual summaries formatted safely for email (no spammy phrasing).
    """
    if not text or not text.strip():
        return "No content available to summarize."

    if not OPENROUTER_KEY:
        raise RuntimeError("OPENROUTER_API_KEY not set in env")

    # Clean and limit text to avoid overloading model
    text = text.strip()
    if len(text) > 4000:
        text = text[:4000] + "..."

    prompt = (
        "You are a neutral, factual news summarizer. "
        "Summarize the following article briefly in 2–3 sentences. "
        "Then include 2–3 short, neutral bullet points (no emojis, no calls to action). "
        "Avoid exaggerations, promotions, or emotional words.\n\n"
        f"ARTICLE:\n{text}"
    )

    payload = {
        "model": MISTRAL_MODEL,
        "messages": [
            {"role": "system", "content": "You are a concise and factual assistant for summarizing news articles."},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": max_tokens,
        "temperature": 0.3
    }

    headers = {
        "Authorization": f"Bearer {OPENROUTER_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost",
        "X-Title": "AI News Assistant"
    }

    try:
        r = requests.post(OPENROUTER_URL, json=payload, headers=headers, timeout=30)
        if r.status_code != 200:
            print("DEBUG RESPONSE:", r.text)
        r.raise_for_status()
        data = r.json()
        summary = data["choices"][0]["message"]["content"].strip()

        # Clean up output for email use
        summary = html.escape(summary)
        summary = summary.replace("\n- ", "<br>• ").replace("\n", "<br>")
        return summary

    except Exception as e:
        print("Summarizer error:", e)
        safe_text = html.escape(text[:800]) + "..." if len(text) > 800 else html.escape(text)
        return safe_text
