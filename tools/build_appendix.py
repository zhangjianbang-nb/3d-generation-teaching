#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase C：速查附录 20 条（长文由 gen_long 生成）。"""
import json, os
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__))); DATA=os.path.join(ROOT,"site","data")
A=[
 ("app-glossary-a","术语表 A–F","从 amortized 到 FID：覆盖前馈推理、体渲染、扩散与评测的基础词条，按英文首字母排列。"),
 ("app-glossary-b","术语表 G–M","从 Gaussian 到 MPM：覆盖高斯泼溅、哈希编码、隐式表面、潜变量与物理仿真的核心词条。"),
 ("app-glossary-c","术语表 N–Z","从 NeRF 到 VSD：覆盖辐射场、SDF、SDS、SLAT、重拓扑与变分蒸馏的后半段词条。"),
 ("app-formulas","公式速查","把体渲染、3DGS 投影、SDF 密度变换、SDS/VSD、三平面、SLAT 与 PBR 的关键公式放在一张表里，配变量解释。"),
 ("app-numbers","数字索引","NeRF 的 5D 输入、Instant-NGP 的 L/T/F、3DGS 的协方差、DreamFusion 的 64×64、TripoSR 的 0.5 秒、Objaverse 的 80 万与 XL 的 1000 万+。"),
 ("app-timeline","时间线","2020 NeRF 到 2025 Hunyuan3D 2.1 / WorldGen：按年份列出关键论文、表示跃迁与路线分叉。"),
 ("app-papers","论文清单","49 篇核验论文的标题、年份、venue、方向、类型与一句话贡献，按方向分组。"),
 ("app-algos","算法清单","28 张算法卡的名字、年份、所属方向、核心公式与后继关系，按流程顺序排列。"),
 ("app-recipes","复现配方","从数据、表示、训练、渲染到评测的复现清单：每个环节的最小可跑配置、常见坑与验收断言。"),
 ("app-debug","失败模式手册","按症状查原因：多面、过饱和、表面糊、薄结构噪、漂浮物、UV 接缝、PBR 失真、场景穿模。"),
 ("app-eval","评测指标","PSNR/SSIM/LPIPS、Chamfer Distance、F-score、新视角几何误差、引擎导入通过率与人工盲评的适用边界。"),
 ("app-datasets","数据集与许可","Objaverse、Objaverse-XL、ShapeNet、Thingi10K 等数据集的规模、来源、许可与清洗建议。"),
 ("app-code","代码与工具","NeRF/3DGS/NeuS/LRM/TRELLIS/MeshAnything 等代表实现的语言、依赖、显存门槛与最小跑通命令。"),
 ("app-hardware","显存与硬件","不同表示/模型的显存量级、训练与推理的硬件门槛、统一内存机型的注意事项。"),
 ("app-myths","常见误区","「多视图一致=几何正确」「一次前向=无需数据」「面数少=质量高」「PBR=彩色贴图」等十个高频误读。"),
 ("app-interview","面试题","3D 生成岗位的 30 道高频题：表示选型、SDS 偏差、多视图一致性、前馈模型、拓扑/PBR/物理。"),
 ("app-teaching","教学脚本","45/90 分钟课程的教学脚本：故事开场、板书、演示、提问、作业与评估。"),
 ("app-open","开放问题","薄结构、背面真实性、拓扑/动画、物理参数、场景一致性、评测协议、数据许可七条开放问题。"),
 ("app-reading","阅读路线","按「先直觉、再理论、再论文、再工程」的四阶段阅读顺序，配每阶段的检查点。"),
 ("app-course","60 分钟速成","给忙人的一条 60 分钟路线：看一张图、读一个故事、做三道题、跑一个最小复现。")
]
out=[{"id":i,"title":t,"summary":s} for i,t,s in A]
json.dump(out,open(os.path.join(DATA,"appendix.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
print("appendix",len(out))
