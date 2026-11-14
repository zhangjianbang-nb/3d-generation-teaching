#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""补齐被演进边引用的 4 张算法卡，修 successors，重算 domain.stats。"""
import json, os
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__))); DATA=os.path.join(ROOT,"site","data")
algs=json.load(open(os.path.join(DATA,"algorithms.json"),encoding="utf-8"))
papers=json.load(open(os.path.join(DATA,"papers.json"),encoding="utf-8"))
dirs=json.load(open(os.path.join(DATA,"directions.json"),encoding="utf-8"))
ids={a["id"] for a in algs}
ADD=[
 {"id":"alg-syncdreamer","name":"3D-aware 同步多视图生成","year":2023,"direction":"d3-multiview","tier":"classic",
  "problem":"逐视角生成的多视图在几何上不一致；如何让 16 个视角共享同一个 3D 代价体、同步去噪？",
  "idea":"每一步把各视角特征反投影到共享 3D 体积，融合后再投影回各视角预测噪声，让几何信息在视角间流动。",
  "how":"参考图编码 + 16 个目标位姿；各视角特征反投影到 3D 体积；3D 卷积/注意力融合；投影回各视角；同步去噪；最后用多视图重建 3D。",
  "flow":["参考图 + 16 位姿","各视角特征反投影","3D 体积融合","投影回各视角","同步去噪","多视图重建"],
  "formula":r"$$\mathbf{V}=\bigoplus_{i=1}^{16}\mathrm{BackProject}(\mathbf{f}_i,\mathbf{c}_i),\qquad \hat{\epsilon}_i=\mathrm{Project}(\mathbf{V},\mathbf{c}_i)$$",
  "pros":["视角一致性优于逐视角生成","覆盖全视角","可直接接重建"],"cons":["16 视角计算量大","背面仍靠幻想","体积分辨率限制细节"],
  "papers":["paper-syncdreamer-2023"],"successors":[]},
 {"id":"alg-worldgen","name":"LLM+程序化+扩散世界组合","year":2025,"direction":"d3-scene-world","tier":"recent",
  "problem":"房间级场景生成无法扩展到可穿越的大世界；纯 3D 生成缺布局与游戏逻辑。",
  "idea":"把世界生成拆成四个模块：LLM 布局推理、程序化地形/建筑、扩散 3D 物体、object-aware 组合；各模块预训练，系统级组合。",
  "how":"文本 → LLM 场景图；程序化生成地形与建筑；扩散模型生成物体；object-aware 分解与放置；导出到游戏引擎；支持布局/尺度/风格控制。",
  "flow":["文本提示","LLM 场景图","程序化地形/建筑","扩散生成物体","组合放置","引擎导出"],
  "formula":r"$$\mathcal{W}=\mathrm{Compose}\!\left(\mathrm{Layout}_{\mathrm{LLM}}(t),\mathrm{Terrain}_{\mathrm{proc}},\{\mathrm{Gen}(o_i)\}\right)$$",
  "pros":["大尺度可穿越","模块化可控","可进游戏引擎"],"cons":["系统复杂","资产质量参差","评测缺标准"],
  "papers":["paper-worldgen-2025"],"successors":[]},
 {"id":"alg-gs-lrm","name":"前馈高斯输出头","year":2024,"direction":"d3-feedforward","tier":"recent",
  "problem":"三平面输出要体渲染、提取网格有损失；能否让前馈模型直接输出 3DGS 参数，实时渲染？",
  "idea":"Transformer 从多视图 token 预测每个高斯的均值、协方差、不透明度、球谐颜色；可微光栅化端到端训练。",
  "how":"多视图 patch 化 + 相机嵌入；Transformer 编码/解码；高斯参数头；可微光栅化渲染；渲染损失训练。",
  "flow":["2–4 视图编码","Transformer 融合","预测高斯参数","光栅化渲染","渲染损失训练"],
  "formula":r"$$\mathcal{G}=\mathrm{Transformer}_\theta(I_{1:K},\mathbf{c}_{1:K}),\qquad \hat{I}=\mathrm{Rasterize}(\mathcal{G},\mathbf{c}')$$",
  "pros":["实时渲染","细节锐","一次前向"],"cons":["显存高","稀疏视图几何不稳","高斯数限制细节"],
  "papers":["paper-gs-lrm-2024"],"successors":[]},
 {"id":"alg-mesh-extraction","name":"等值面/可微网格提取","year":2021,"direction":"d3-scene-recon","tier":"classic",
  "problem":"隐式场/密度场需要转成三角网格才能进引擎；Marching Cubes 不可微，DMTet 可微但分辨率受限。",
  "idea":"在规则网格/四面体上按符号切出等值面；DMTet 用可变形四面体 + SDF 插值让顶点位置可微。",
  "how":"规则网格 Marching Cubes 查表生成三角面；DMTet 初始化四面体、预测顶点 SDF、按符号切面、线性插值顶点；可微渲染回传梯度。",
  "flow":["规则网格/四面体","预测 SDF/密度","按符号切面","插值顶点","输出三角网格"],
  "formula":r"$$\mathcal{M}=\mathrm{MarchingCubes}(s),\quad \text{或}\quad \mathcal{M}=\mathrm{DMTet}(\{s_v\},\{x_v\})$$",
  "pros":["输出直接是网格","DMTet 可微","与渲染管线兼容"],"cons":["分辨率限制细节","MC 不可微","拓扑可能不稳定"],
  "papers":["paper-neus-2021","paper-get3d-2022"],"successors":[]}
]
for a in ADD:
    if a["id"] not in ids:
        algs.append(a); ids.add(a["id"])
fix={"alg-mvdream":["alg-syncdreamer","alg-cross-domain-diffusion"],
     "alg-cross-domain-diffusion":[],
     "alg-lrm-triplane":["alg-gs-lrm","alg-trellis-slat","alg-hunyuan-dit"]}
for a in algs:
    if a["id"] in fix: a["successors"]=fix[a["id"]]
json.dump(algs,open(os.path.join(DATA,"algorithms.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
domain=json.load(open(os.path.join(DATA,"domain.json"),encoding="utf-8"))
core=sum(1 for p in papers if p["type"] in ("foundational","classic"))
recent=sum(1 for p in papers if p["type"] in ("recent","latest"))
domain["stats"]={"directions":len(dirs),"classic_algorithms":sum(1 for a in algs if a["tier"]=="classic"),"core_papers":core,"recent_papers":recent,"total_papers":len(papers)}
json.dump(domain,open(os.path.join(DATA,"domain.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
# 引用完整性自检
pids={p["id"] for p in papers}; dids={d["id"] for d in dirs}
errs=[]
for d in dirs:
    for k in d["key_papers"]:
        if k not in pids: errs.append("dir key_paper "+k)
    for r in d.get("related",[]):
        if r not in dids: errs.append("dir related "+r)
for a in algs:
    if a["direction"] not in dids: errs.append("alg dir "+a["id"])
    for p in a["papers"]:
        if p not in pids: errs.append("alg paper "+p)
    for s in a.get("successors",[]):
        if s not in ids: errs.append("alg succ "+a["id"]+"->"+s)
for p in papers:
    if p["direction"] not in dids: errs.append("paper dir "+p["id"])
    for s in p.get("successors",[]):
        if s not in pids: errs.append("paper succ "+p["id"]+"->"+s)
    for pre in p.get("prereq",[]):
        if pre not in pids: errs.append("paper prereq "+p["id"]+"->"+pre)
ev=json.load(open(os.path.join(DATA,"evolution.json"),encoding="utf-8"))
for e in ev["edges"]:
    if e["from"] not in ids: errs.append("edge from "+e["from"])
    if e["to"] not in ids: errs.append("edge to "+e["to"])
print("algs",len(algs),"papers",len(papers),"stats",domain["stats"])
print("ref errors",len(errs)); [print(" -",x) for x in errs]
