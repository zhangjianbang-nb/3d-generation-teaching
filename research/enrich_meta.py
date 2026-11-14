#!/usr/bin/env python3
"""补齐漏检论文，并用 Semantic Scholar batch 补 venue/引用数。"""
import json
import os
import re
import time
import urllib.request
import xml.etree.ElementTree as ET

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(ROOT, "research", "arxiv-raw.json")
META = os.path.join(ROOT, "research", "papers-meta.json")

EXTRA_IDS = ["2212.00774", "2408.00653", "2405.14979", "2404.13026",
             "2404.12385", "2403.01248"]
NS = {"a": "http://www.w3.org/2005/Atom"}


def fetch_ids(ids):
    url = "https://export.arxiv.org/api/query?id_list=%s&max_results=20" % ",".join(ids)
    req = urllib.request.Request(url, headers={"User-Agent": "3d-survey/1.0"})
    with urllib.request.urlopen(req, timeout=40) as r:
        return r.read().decode("utf-8")


def parse(xml):
    root = ET.fromstring(xml)
    out = []
    for e in root.findall("a:entry", NS):
        out.append({
            "title": " ".join(e.findtext("a:title", "", NS).split()),
            "arxiv_id": e.findtext("a:id", "", NS).rsplit("/", 1)[-1],
            "published": e.findtext("a:published", "", NS)[:10],
            "authors": [a.findtext("a:name", "", NS) for a in e.findall("a:author", NS)],
            "summary": " ".join(e.findtext("a:summary", "", NS).split()),
            "categories": [c.get("term") for c in e.findall("a:category", NS)],
        })
    return out


def s2_batch(ids):
    url = "https://api.semanticscholar.org/graph/v1/paper/batch?fields=title,venue,year,citationCount,publicationVenue,externalIds"
    body = json.dumps({"ids": ["ARXIV:" + i for i in ids]}).encode()
    req = urllib.request.Request(url, data=body, headers={
        "Content-Type": "application/json", "User-Agent": "3d-survey/1.0"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read().decode())


def main():
    raw = json.load(open(RAW, encoding="utf-8"))
    existing = {r["arxiv_id"].split("v")[0] for r in raw["results"]}
    extra = [e for e in parse(fetch_ids(EXTRA_IDS)) if e["arxiv_id"].split("v")[0] not in existing]
    for e in extra:
        e["query"] = e["title"]
    raw["results"].extend(extra)
    raw["misses"] = [m for m in raw["misses"] if m["query"] not in (
        "Score Jacobian Chaining: Lifting Pretrained 2D Diffusion Models for 3D Generation",
        "MeshLRM: Large Reconstruction Model for High-Quality Mesh",
        "SF3D: Stable Fast 3D Mesh Reconstruction with UV-unwrapped Disentangled Materials",
        "CraftsMan: High-fidelity Mesh Generation with 3D Native Generation and Interactive Geometry Refiner",
        "PhysDreamer: Physics-Based Interaction with 3D Objects via Video Generation",
        "SceneCraft: An LLM Agent for Synthesizing 3D Scenes as Blender Code")]
    json.dump(raw, open(RAW, "w", encoding="utf-8"), ensure_ascii=False, indent=2)

    ids = [r["arxiv_id"].split("v")[0] for r in raw["results"]]
    meta = {}
    for i in range(0, len(ids), 20):
        chunk = ids[i:i + 20]
        try:
            data = s2_batch(chunk)
        except Exception as e:
            print("S2 batch fail", e)
            time.sleep(5)
            data = [None] * len(chunk)
        for aid, item in zip(chunk, data):
            meta[aid] = item or {}
        time.sleep(3)

    for r in raw["results"]:
        base = r["arxiv_id"].split("v")[0]
        r["arxiv_id"] = base
        m = meta.get(base) or {}
        r["venue"] = (m.get("venue") or "").strip()
        r["citation_count"] = m.get("citationCount")
        r["s2_title"] = m.get("title")
        r["s2_year"] = m.get("year")
    json.dump(raw, open(RAW, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    json.dump({"papers": raw["results"], "misses": raw["misses"]},
              open(META, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print("total", len(raw["results"]))
    for r in raw["results"]:
        print(r["arxiv_id"], r["published"][:4], (r.get("venue") or "-")[:28],
              r.get("citation_count"), r["title"][:58])


if __name__ == "__main__":
    main()
