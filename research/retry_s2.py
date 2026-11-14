#!/usr/bin/env python3
"""重试 S2 元数据（小批量），失败则保留空值。"""
import json
import os
import time
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(ROOT, "research", "arxiv-raw.json")


def s2_batch(ids):
    url = "https://api.semanticscholar.org/graph/v1/paper/batch?fields=title,venue,year,citationCount,publicationVenue,externalIds"
    body = json.dumps({"ids": ["ARXIV:" + i for i in ids]}).encode()
    req = urllib.request.Request(url, data=body, headers={
        "Content-Type": "application/json", "User-Agent": "3d-survey/1.0"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read().decode())


def main():
    raw = json.load(open(RAW, encoding="utf-8"))
    todo = [r["arxiv_id"] for r in raw["results"] if not r.get("venue")]
    print("retry", len(todo))
    got = {}
    for i in range(0, len(todo), 5):
        chunk = todo[i:i + 5]
        try:
            data = s2_batch(chunk)
        except Exception as e:
            print("fail", chunk, e)
            data = [None] * len(chunk)
        for aid, item in zip(chunk, data):
            if item:
                got[aid] = item
                print("OK", aid, item.get("venue"), item.get("citationCount"))
        time.sleep(4)
    for r in raw["results"]:
        m = got.get(r["arxiv_id"])
        if m:
            r["venue"] = (m.get("venue") or "").strip()
            r["citation_count"] = m.get("citationCount")
            r["s2_year"] = m.get("year")
    json.dump(raw, open(RAW, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print("filled", len(got))


if __name__ == "__main__":
    main()
