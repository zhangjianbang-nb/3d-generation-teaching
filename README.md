# 3D AI 生成 · 领域研究与教学站

一个**离线可读、单入口**的 3D 生成（3D AI Generation）领域研究与教学站点：从可微渲染到前馈大模型，
从 SDS 到多视图扩散，从重拓扑到 PBR 材质，把「表示 → 监督 → 生产」三层主干讲透。

**在线**：<https://zhangjianbang-nb.github.io/3d-generation-teaching/>
**本地**：直接双击 `index.html` 即可（file:// 可用，完全离线：KaTeX 与字体内置，无任何 CDN / 外部请求）

## 规模

| 维度 | 数量 |
|---|---|
| 可见正文 | **5,075,384 字**（CJK/可见 ≈ 1.386） |
| 论文 | 49 篇（逐篇 10 节精读 + 速查表） |
| 算法 | 28 个（每个含机制图 + 配方 + 对照） |
| 理论 | 15 个（可微渲染、表示论、概率流、评测协议…） |
| 研究方向 | 8 个（表示/监督/生产/场景/动态/数据/评测/治理） |
| 故事 | 2 部（贯穿比喻 + 工匠笔记） |
| 考核题 | 63 道（五层难度，含 368 个公式、273 张表） |
| 全书 | 12 卷（从「雾与光」到「选型与未来」） |
| 附录 | 20 篇（术语、工具链、失败模式、治理清单…） |
| 内联 SVG 图 | 183 张（无外部图片，全部数据驱动生成） |

## 怎么读

- `#/home` 总览：四层体系与三条并行主线
- `#/map` 研究方向：8 个方向各自的问题、方法与开放问题
- `#/papers` 论文库：49 篇逐篇精读（含 `abstract_only` 摘要级标注）
- `#/algos` / `#/theory` 算法与理论卡
- `#/story` 故事书：用贯穿比喻讲清「2D 监督怎么长出 3D」
- `#/book` 十二卷全书：专业导读 → 机制展开 → 工匠笔记
- `#/exam` 考核：63 道五层题，答案按需懒加载
- `#/appendix` 附录、`#/evolution` 演进时间线、`#/summary` 一句话结论

## 目录

```
index.html          单页应用入口（含路由、搜索、进度、KaTeX 渲染）
data/*.json         唯一真源（papers/algorithms/theory/directions/stories/assessments/book/appendix…）
data/bundle.js      由 bundle_data.py 从 JSON 打包（首屏只读这一个文件）
vendor/katex/       KaTeX 0.16.9（JS/CSS/字体，本地内置）
tools/              生成与验收流水线（gen_long / build_long / figs / assert_all / gate_all …）
content/            长文片段源（long/ 下按单元分目录，tasks*.json 为写作任务）
research/           检索台账、论文元数据、ChatGPT 外部评审全文与处置
teaching/           故事/理论/题库的人读稿说明
```

> 说明：本仓库把原项目的 `site/` 内容提升到了根目录以适配 GitHub Pages；`tools/` 脚本按原布局
> 以 `--site site` 调用，在本仓库等价于 `--site .`。

## 验收记录（2026-11-14 定稿）

- `tools/assert_all.py`：**20/20 PASS**（总量 ≥500 万可见字符、每单元 ≥500 字、公式配对、重复段落、SVG 卫生、故事结构）
- `tools/fig_probe.js`：**163 张图逐张 0 issue**
- `e2e_site.js`：**21/21 PASS**（搜索、考核展开、进度、移动端菜单）
- `mobile_probe.js`：**ALL PASS**（390px 窄屏横向溢出 0px）
- `verify_site.py --phase all`：**0 error 0 warning**
- 三轮单 subagent 四维验收：77 → 84.0 → **86 PASS**（视觉 86 / 内容 88 / 功能 87 / 风险 80），
  终验遗留 20 条轻微缺陷已披露；终验后 9 条低风险打磨完成并全闸门复核。

## 已知限制

1. `data/bundle.js` 15.3 MB 同步加载（file:// 首屏解析约 1 s，弱机更慢）。
2. 论文短字段（summary/results）与长文前几节存在信息重叠（重复非错误）。
3. 窄屏故事插画为可横滑 SVG（`min-width: 560px`，有「可横滑」提示条）。
4. 长文行宽在 1360px 下约 78 字符（略宽于排版理想的 66）。
5. 全局搜索只覆盖列表页（论文/算法），不进长文正文。

## 许可

- 文字内容（论文精读、故事、理论、题库、全书、附录）：**CC BY 4.0**
- 代码（`index.html` 内联 JS、`tools/` 脚本）：**MIT**

详见 `LICENSE`。

## 外部评审

ChatGPT 评审（2026-11-13）全文归档于 `research/chatgpt/review-20261113.txt`，逐条采纳/驳回见
`research/chatgpt/decisions.md`；已采纳「重建/生成分界」「前馈=计算方式而非生成范式」「补记自回归与 4D/动态」
「三条并行主线」四项修正。
