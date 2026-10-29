"""Fetch the Substack RSS feed and save recent posts to docs/_data/substack.json.

Substack (via Cloudflare) often returns 403 to GitHub Actions runners, so if the
direct fetch fails we fall back to the rss2json.com proxy.
"""
import json
import sys
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime
from email.utils import parsedate_to_datetime

FEED_URL = "https://stephspiel.substack.com/feed"
PROXY_URL = "https://api.rss2json.com/v1/api.json?rss_url=" + urllib.parse.quote(FEED_URL, safe="")
OUT_FILE = "docs/_data/substack.json"
MAX_POSTS = 5
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/124.0 Safari/537.36",
    "Accept": "application/rss+xml, application/xml;q=0.9, */*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}


def fetch(url):
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read()


def from_rss():
    root = ET.fromstring(fetch(FEED_URL))
    return [
        {
            "title": item.findtext("title", "").strip(),
            "description": item.findtext("description", "").strip(),
            "url": item.findtext("link", "").strip(),
            "date": parsedate_to_datetime(item.findtext("pubDate")),
        }
        for item in root.iter("item")
    ]


def from_proxy():
    data = json.loads(fetch(PROXY_URL))
    if data.get("status") != "ok":
        raise RuntimeError(f"rss2json error: {data.get('message')}")
    return [
        {
            "title": item.get("title", "").strip(),
            "description": item.get("description", "").strip(),
            "url": item.get("link", "").strip(),
            "date": datetime.strptime(item["pubDate"], "%Y-%m-%d %H:%M:%S"),
        }
        for item in data["items"]
    ]


try:
    posts = from_rss()
except Exception as e:
    print(f"Direct feed fetch failed ({e}); trying rss2json proxy", file=sys.stderr)
    posts = from_proxy()

for post in posts:
    post["date"] = post["date"].strftime("%B %-d, %Y")

with open(OUT_FILE, "w") as f:
    json.dump(posts[:MAX_POSTS], f, indent=2, ensure_ascii=False)
    f.write("\n")
