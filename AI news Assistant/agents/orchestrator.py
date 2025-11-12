import os
import re
from typing import List, Dict
from .fetchers import MediastackFetcher, GNewsFetcher
from .deduper import dedupe_articles
from .summarizer import summarise_text
from .emailer_sendgrid import send_email_sendgrid

MAX_ARTICLES = int(os.getenv("MAX_ARTICLES_PER_RUN", "8"))


def sanitize_url(url: str) -> str:
    """Remove tracking parameters and validate links."""
    if not url:
        return ""
    url = re.sub(r"(\?|&)utm_[^=]+=[^&]+", "", url)  # strip UTM junk
    if not re.match(r"^https?://", url):
        return ""
    return url.strip()


def clean_text(text: str) -> str:
    """Remove spammy phrases and excess links."""
    text = re.sub(r"http\S+", "", text)  # remove inline URLs
    text = re.sub(r"(click here|read more|free|offer|deal|subscribe)", "", text, flags=re.I)
    return text.strip()


def build_email_html(topic: str, summaries: List[Dict]) -> str:
    """Builds clean, safe HTML email body with minimal links."""
    html = f"""
    <html>
    <body style="font-family: Arial, sans-serif; line-height:1.6; color:#333;">
    <h2>📰 {topic.title()} — Daily News Digest</h2>
    <p>Here’s a short, factual summary of recent updates about <b>{topic}</b>.</p>
    <hr style="border:none;border-top:1px solid #ccc;"/>

    <ul style="padding-left:15px;">
    """

    for s in summaries:
        title = clean_text(s.get("title", "Untitled"))
        summary = clean_text(s.get("summary", ""))
        link = sanitize_url(s.get("url", ""))

        html += f"""
        <li style="margin-bottom:15px;">
            <b>{title}</b><br>
            {summary}
            {"<br><a href='" + link + "' style='color:#1a73e8;text-decoration:none;'>Source</a>" if link else ""}
        </li>
        """

    html += """
    </ul>
    <hr style="border:none;border-top:1px solid #ccc;"/>
    <p style="font-size:0.8em;color:#777;">
      This digest was generated automatically by your AI News Assistant.<br>
      You’re receiving this because you requested topic updates.
    </p>
    </body></html>
    """
    return html


def run_news_pipeline(topic: str, recipient_email: str) -> List[Dict]:
    """
    1. Fetch from multiple sources
    2. Deduplicate
    3. Summarize using Mistral
    4. Send via SendGrid (with spam-safe HTML)
    Returns summaries for display
    """
    # --- 1. Fetchers ---
    m = MediastackFetcher()
    g = GNewsFetcher()

    fetched = []
    try:
        fetched += m.fetch(keywords=topic, limit=MAX_ARTICLES // 2)
    except TypeError:
        fetched += m.fetch(keywords=topic, limit=MAX_ARTICLES // 2)
    fetched += g.fetch(q=topic, max_results=MAX_ARTICLES // 2)

    # --- 2. Deduplicate ---
    unique = dedupe_articles(fetched)[:MAX_ARTICLES]

    # --- 3. Summarize ---
    summaries = []
    for art in unique:
        text = f"{art.get('title', '')}\n\n{art.get('description', '')}"
        try:
            summary = summarise_text(text)
        except Exception as e:
            print("Summarizer error:", e)
            summary = text or "Summary not available."
        summaries.append({
            "title": art.get("title"),
            "url": art.get("url"),
            "summary": summary
        })

    # --- 4. Build & Send Email ---
    if recipient_email:
        html = build_email_html(topic, summaries)
        subj = f"{topic.title()} – AI News Digest"
        success = send_email_sendgrid(recipient_email, subj, html)

        if not success:
            raise RuntimeError("❌ Failed to send email via SendGrid. Check logs and API key.")

    return summaries
