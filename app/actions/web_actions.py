
import re
import webbrowser
from urllib.parse import urlparse


ALLOWED_SITES = {
    "youtube": "https://www.youtube.com",
    "google": "https://www.google.com",
    "gmail": "https://mail.google.com",
    "github": "https://github.com",
    "stackoverflow": "https://stackoverflow.com",
}


def open_website(site: str) -> dict:
    """Open a recognized website in the default browser."""
    cleaned = re.sub(r"\s+", " ", site.strip().lower())

    aliases = {
        "you tube": "youtube",
        "yt": "youtube",
        "google search": "google",
        "stack overflow": "stackoverflow",
    }
    cleaned = aliases.get(cleaned, cleaned)

    url = ALLOWED_SITES.get(cleaned)

    if not url:
        raise ValueError(
            "I don't recognize that website yet. Try YouTube, Google, Gmail, or GitHub."
        )

    parsed = urlparse(url)
    if parsed.scheme != "https" or not parsed.netloc:
        raise ValueError("This website address is not allowed.")

    try:
        opened = webbrowser.open(url, new=2)
    except Exception as exc:
        raise RuntimeError("I couldn't open the website in your browser.") from exc

    if not opened:
        raise RuntimeError(
            "Windows couldn't open the website. Check your default browser."
        )

    return {"site": cleaned, "url": url, "message": f"Opening {cleaned}."}
