# ChatGPT 外部评审处置（2026-11-13）

评审全文：`research/chatgpt/review-20261113.txt`（6,412 字符，会话 `6af68c9a-f6b4-83e8-8a94-cc444a8dbe5a`）。

## 采纳

| # | 评审意见 | 处置 | 落点 |
|---|---|---|---|
| 1 | 「重建」与「生成」是两个问题，D1 名称应改为「三维表示、重建与可微渲染」 | 采纳，方向改名 | `directions.json` d3-scene-recon |
| 2 | 前馈（feed-forward）是计算方式，不是生成范式；应把「架构 / 生成范式 / 输出表示」分开 | 采纳，新增「四层知识体系」一节，明确四层=表示/生成范式/输出结构/应用场景 | `summary.json` sections[1] |
| 3 | 漏了自回归 3D 生成 | 部分采纳：自回归已在 d3-mesh-topo 的 core_tech（MeshGPT/MeshAnything），但未单列方向；在四层体系与方向页正文中点名，不新增第 9 方向（会破坏 8 方向计数与论文归属） | `directions.json` d3-mesh-topo + `summary.json` |
| 4 | 漏了 4D/动态 3D 生成 | 采纳为「场景主线的下一段」，写入 d3-scene-world 的 recent 与 challenges；同时在 coverage.gaps 保留「视频/4D 未纳入论文库」的披露 | `directions.json` d3-scene-world、`coverage.json` |
| 5 | 场景生成覆盖不足 | 驳回（评审只看到 8 个方向名，未看到 d3-scene-world 已含 Text2Room/WonderWorld/WorldGen/SceneCraft/PhysDreamer）；保留方向与 5 篇论文，正文补 4D 说明 | `directions.json` d3-scene-world |
| 6 | 物理约束应独立 | 部分采纳：PhysDreamer 已在 d3-scene-world；不单列方向，避免与场景重复；在四层体系「应用场景」层写明物理是可交互世界的前置 | `summary.json` |
| 7 | 演进主线不要写成线性历史，应有三条并行路线（表示 / 生成范式 / 应用） | 采纳，写入 evolution.external_review 与四层体系 | `evolution.json`、`summary.json` |
| 8 | 数据、评测、效率、失败模式应作为横向专题，不硬凑成独立方向 | 部分采纳：d3-data-production 保留为方向（因为 Objaverse/PBR/UV 有独立论文群），但在四层体系中明确它是横向专题而非生成范式 | `summary.json` |

## 驳回

| # | 评审意见 | 驳回理由 |
|---|---|---|
| 1 | 「MOPD 的三个方向混入 3D 地图」 | 评审把上一轮 MOPD 会话的上下文带进来了；本任务从未把 MOPD 方向写入 3D 地图，8 个方向全部是 3D 生成。属评审侧串台，不采纳。 |
| 2 | 建议扩为 D1–D8 新八方向（把 4D、自回归、物理各自独立） | 会让 49 篇论文的归属与 28 个算法的方向计数全部重排，且与「按解决什么问题划分」的既定口径冲突；改为在现有方向内补记 + 四层体系说明。 |
| 3 | 49 篇不足以覆盖完整 | 同意「不足以覆盖完整」，但本次是工程向精选而非穷尽综述；已在 coverage.gaps 披露 4D、版权/水印、CAD 结合三项缺口，不假装完整。 |

## 未处置（需后续版本）

- 4D/动态生成的论文与算法未入库（coverage.gaps 已披露）。
- 自回归 3D 生成未单列方向（仅作为 d3-mesh-topo 的技术标签）。
- 版权、水印、安全未单列。
