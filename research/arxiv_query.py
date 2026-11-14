#!/usr/bin/env python3
"""按候选标题查 arXiv，严格匹配标题，落盘原始元数据。"""
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "research", "arxiv-raw.json")

TITLES = [
    "NeRF: Representing Scenes as Neural Radiance Fields for View Synthesis",
    "Instant Neural Graphics Primitives with a Multiresolution Hash Encoding",
    "3D Gaussian Splatting for Real-Time Radiance Field Rendering",
    "NeuS: Learning Neural Implicit Surfaces by Volume Rendering for Multi-view Reconstruction",
    "Volume Rendering of Neural Implicit Surfaces",
    "Efficient Geometry-aware 3D Generative Adversarial Networks",
    "GET3D: A Generative Model of High Quality 3D Textured Shapes Learned from Images",
    "DreamFusion: Text-to-3D using 2D Diffusion",
    "Magic3D: High-Resolution Text-to-3D Content Creation",
    "Score Jacobian Chaining: Lifting Pretrained 2D Diffusion Models for 3D Generation",
    "ProlificDreamer: High-Fidelity and Diverse Text-to-3D Generation with Variational Score Distillation",
    "Fantasia3D: Disentangling Geometry and Appearance for High-quality Text-to-3D Content Creation",
    "TextMesh: Generation of Realistic 3D Meshes From Text Prompts",
    "DreamGaussian: Generative Gaussian Splatting for Efficient 3D Content Creation",
    "LucidDreamer: Towards High-Fidelity Text-to-3D Generation via Interval Score Matching",
    "Point-E: A System for Generating 3D Point Clouds from Complex Prompts",
    "Shap-E: Generating Conditional 3D Implicit Functions",
    "Zero-1-to-3: Zero-shot One Image to 3D Object",
    "MVDream: Multi-view Diffusion for 3D Generation",
    "SyncDreamer: Generating Multiview-consistent Images from a Single-view Image",
    "Wonder3D: Single Image to 3D using Cross-Domain Diffusion",
    "LRM: Large Reconstruction Model for Single Image to 3D",
    "TripoSR: Fast 3D Object Reconstruction from a Single Image",
    "InstantMesh: Efficient 3D Mesh Generation from a Single Image with Sparse-view Large Reconstruction Models",
    "CRM: Single Image to 3D Textured Mesh with Convolutional Reconstruction Model",
    "GS-LRM: Large Reconstruction Model for 3D Gaussian Splatting",
    "MeshLRM: Large Reconstruction Model for High-Quality Mesh",
    "LGM: Large Multi-View Gaussian Model for High-Resolution 3D Content Creation",
    "SF3D: Stable Fast 3D Mesh Reconstruction with UV-unwrapped Disentangled Materials",
    "Direct3D: Scalable Image-to-3D Generation via 3D Latent Diffusion Transformer",
    "Structured 3D Latents for Scalable and Versatile 3D Generation",
    "Hunyuan3D 2.0: Scaling Diffusion Models for High Resolution Textured 3D Assets Generation",
    "Hunyuan3D 2.1: From Images to High-Fidelity 3D Assets with Production-Ready PBR Material",
    "CraftsMan: High-fidelity Mesh Generation with 3D Native Generation and Interactive Geometry Refiner",
    "MeshGPT: Generating Triangle Meshes with Decoder-Only Transformers",
    "MeshAnything: Artist-Created Mesh Generation with Autoregressive Transformers",
    "MeshAnything V2: Artist-Created Mesh Generation with Adjacent Mesh Tokenization",
    "Hi3DGen: High-fidelity 3D Geometry Generation from Images via Normal Bridging",
    "Step1X-3D: Towards High-Fidelity and Controllable Generation of Textured 3D Assets",
    "PartCrafter: Structured 3D Mesh Generation via Compositional Latent Diffusion Transformers",
    "Text2Room: Extracting Textured 3D Meshes from 2D Text-to-Image Models",
    "WonderWorld: Interactive 3D Scene Generation from a Single Image",
    "WorldGen: From Text to Traversable and Interactive 3D Worlds",
    "PhysDreamer: Physics-Based Interaction with 3D Objects via Video Generation",
    "pixelNeRF: Neural Radiance Fields from One or Few Images",
    "Objaverse: A Universe of Annotated 3D Objects",
    "Objaverse-XL: A Universe of 10M+ 3D Objects",
    "SceneCraft: An LLM Agent for Synthesizing 3D Scenes as Blender Code",
    "3D Generation on the Web: A Survey of Text-to-3D",
    "A Survey on 3D Gaussian Splatting",
]


def norm(s):
    return re.sub(r"[^a-z0-9]+", " ", s.lower()).strip()


def query(title):
    q = urllib.parse.quote('ti:"%s"' % title)
    url = ("https://export.arxiv.org/api/query?search_query=%s"
           "&start=0&max_results=5&sortBy=relevance" % q)
    req = urllib.request.Request(url, headers={"User-Agent": "3d-survey/1.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8")


def parse(xml):
    ns = {"a": "http://www.w3.org/2005/Atom"}
    root = ET.fromstring(xml)
    out = []
    for e in root.findall("a:entry", ns):
        title = " ".join((e.findtext("a:title", "", ns) or "").split())
        aid = e.findtext("a:id", "", ns) or ""
        published = e.findtext("a:published", "", ns) or ""
        authors = [a.findtext("a:name", "", ns) for a in e.findall("a:author", ns)]
        summary = " ".join((e.findtext("a:summary", "", ns) or "").split())
        cats = [c.get("term") for c in e.findall("a:category", ns)]
        out.append({"title": title, "arxiv_id": aid.rsplit("/", 1)[-1],
                    "published": published[:10], "authors": authors,
                    "summary": summary, "categories": cats})
    return out


def main():
    results, misses = [], []
    for i, title in enumerate(TITLES, 1):
        try:
            xml = query(title)
            cands = parse(xml)
        except Exception as e:
            misses.append({"query": title, "error": str(e)})
            print("ERR", title, e)
            time.sleep(3)
            continue
        nt = norm(title)
        best = None
        for c in cands:
            if norm(c["title"]) == nt:
                best = c
                break
        if best is None:
            misses.append({"query": title, "candidates": [c["title"] for c in cands[:3]]})
            print("MISS", title)
        else:
            best["query"] = title
            results.append(best)
            print("OK  ", title[:60], best["arxiv_id"], best["published"])
        time.sleep(2.5)
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump({"results": results, "misses": misses}, f, ensure_ascii=False, indent=2)
    print("matched", len(results), "misses", len(misses))
    return 0


if __name__ == "__main__":
    sys.exit(main())
