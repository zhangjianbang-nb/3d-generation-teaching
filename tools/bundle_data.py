#!/usr/bin/env python3
"""把 site/data/*.json 打包成 site/data/bundle.js。

index.html 只读 bundle.js：这样 file:// 直接打开也不会触发 fetch/CORS 限制。
JSON 仍是唯一真源；每次改完数据都要重跑本脚本。
"""

import argparse
import datetime
import json
import os
import sys

DATA_KEYS = [
    "domain", "directions", "algorithms", "papers", "stories",
    "theory", "assessments", "evolution", "summary", "coverage",
]

# 可选数据：存在就打包，不存在不算缺失（「全书」长文模块）
OPTIONAL_KEYS = ["book", "appendix"]


def load(site):
    data = {}
    missing = []
    for key in DATA_KEYS:
        path = os.path.join(site, "data", key + ".json")
        if not os.path.exists(path):
            missing.append(path)
            continue
        with open(path, "r", encoding="utf-8") as f:
            try:
                data[key] = json.load(f)
            except json.JSONDecodeError as e:
                raise SystemExit(f"JSON 解析失败：{path}\n  {e}")
    for key in OPTIONAL_KEYS:
        path = os.path.join(site, "data", key + ".json")
        if not os.path.exists(path):
            continue
        with open(path, "r", encoding="utf-8") as f:
            data[key] = json.load(f)
    if missing:
        raise SystemExit("缺少数据文件：\n  " + "\n  ".join(missing))
    return data


def extract_bundle(path):
    """从 bundle.js 里解析出 SITE_DATA 对象（用于校验是否与 JSON 一致）。"""
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    marker = "window.SITE_DATA"
    idx = text.find(marker)
    if idx < 0:
        raise ValueError("bundle.js 中未找到 window.SITE_DATA")
    eq = text.find("=", idx)
    if eq < 0:
        raise ValueError("bundle.js 中未找到赋值号")
    obj, _ = json.JSONDecoder().raw_decode(text[eq + 1:].lstrip())
    return obj


def build(site, quiet=True):
    data = load(site)
    payload = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    out = os.path.join(site, "data", "bundle.js")
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(out, "w", encoding="utf-8") as f:
        f.write("window.SITE_DATA = " + payload + ";\n")
        f.write('window.SITE_DATA_GENERATED = "' + now + '";\n')
    if not quiet:
        counts = {
            "directions": len(data["directions"]),
            "algorithms": len(data["algorithms"]),
            "papers": len(data["papers"]),
            "stories": len(data["stories"]),
            "theory": len(data["theory"]),
            "assessments": len(data["assessments"]),
        }
        print("📦 bundle.js 已生成：" + out)
        print("   " + " · ".join(f"{k}={v}" for k, v in counts.items()))
        print(f"   大小 {os.path.getsize(out)/1024:.1f} KB")
    return out


def main():
    ap = argparse.ArgumentParser(description="生成 site/data/bundle.js")
    ap.add_argument("--site", required=True, help="site 目录（含 data/*.json）")
    args = ap.parse_args()
    site = os.path.abspath(os.path.expanduser(args.site))
    if not os.path.isdir(site):
        sys.exit(f"目录不存在：{site}")
    build(site, quiet=False)


if __name__ == "__main__":
    main()
