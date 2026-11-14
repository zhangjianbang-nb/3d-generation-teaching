#!/bin/bash
# 全站终验：拼装 → 数据断言 → 图几何 → e2e → 窄屏
set -o pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SK="$HOME/.zcode/skills/ai-domain-research-and-teaching/scripts"
export NODE_PATH=/tmp/node_modules
export PUPPETEER_CORE=/tmp/node_modules/puppeteer-core
cd "$ROOT"
echo "== build =="
python3 tools/build_long.py | tail -2
echo "== assert_all =="
python3 tools/assert_all.py | tail -25
echo "== fig dump =="
python3 -I "$SK/fig_dump_all.py" --site "$ROOT/site" | tail -1
echo "== fig probe =="
node tools/fig_probe.js shots/figtest-all.html | tail -3
echo "== e2e =="
node "$SK/e2e_site.js" "$ROOT/site" | tail -2
echo "== mobile =="
node tools/mobile_probe.js | tail -4
