"""Fetch the Substack RSS feed and save recent posts to docs/_data/substack.json."""
import json
import urllib.request
import xml.etree.ElementTree as ET
from email.utils import parsedate_to_datetime

FEED_URL = "https://stephspiel.substack.com/feed"
OUT_FILE = "docs/_data/substack.json"
MAX_POSTS = 5

req = urllib.request.Request(FEED_URL, headers={"User-Agent": "Mozilla/5.0"})
with urllib.request.urlopen(req, timeout=30) as resp:
    root = ET.fromstring(resp.read())

posts = []
for item in root.iter("item"):
    pub = parsedate_to_datetime(item.findtext("pubDate"))
    posts.append({
        "title": item.findtext("title", "").strip(),
        "description": item.findtext("description", "").strip(),
        "url": item.findtext("link", "").strip(),
        "date": pub.strftime("%B %-d, %Y"),
    })

with open(OUT_FILE, "w") as f:
    json.dump(posts[:MAX_POSTS], f, indent=2, ensure_ascii=False)
    f.write("\n")
