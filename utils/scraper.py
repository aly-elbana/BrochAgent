import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re
from requests_html import HTMLSession

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117 Safari/537.36"
}

session = HTMLSession()

def fetch_website_contents(url, render_js=False, max_chars=50000):
    r = session.get(url, headers=headers) if render_js else requests.get(url, headers=headers)
    if render_js:
        r.html.render(timeout=20)
        raw_html = r.html.html
    else:
        raw_html = r.text

    soup = BeautifulSoup(raw_html, "html.parser")

    title = soup.title.string if soup.title else ""

    meta = {m.get("name") or m.get("property"): m.get("content") for m in soup.find_all("meta") if m.get("content")}

    jsonld = [ld.get_text(strip=True) for ld in soup.find_all("script", type="application/ld+json")]

    text = soup.get_text(" ", strip=True)

    links = [urljoin(url, a.get("href")) for a in soup.find_all("a", href=True)]

    images = [{"src": urljoin(url, img.get("src")), "alt": img.get("alt")} for img in soup.find_all("img")]

    scripts = [s.get_text() for s in soup.find_all("script") if s.string]

    styles = [s.get_text() for s in soup.find_all("style")]

    canonical = None
    can_tag = soup.find("link", rel="canonical")
    if can_tag:
        canonical = urljoin(url, can_tag.get("href"))

    og = {tag.get("property"): tag.get("content") for tag in soup.find_all("meta") if tag.get("property", "").startswith("og:")}

    data = {
        "url": url,
        "canonical": canonical,
        "title": title,
        "meta": meta,
        "opengraph": og,
        "jsonld": jsonld,
        "text": text[:max_chars],
        "links": links,
        "images": images,
        "scripts": scripts,
        "styles": styles,
        "html": raw_html[:max_chars]
    }

    return data


def fetch_website_links(url):
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")
    return [urljoin(url, a.get("href")) for a in soup.find_all("a", href=True)]
