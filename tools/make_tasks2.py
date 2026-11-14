#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第二轮扩写任务：在首轮 5 部分之外，为每个条目补工程/对照/评测/落地/教学视角。"""
import json, os, sys
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,HERE)
import make_tasks as M
ROOT=M.ROOT; DATA=M.DATA
PART=3600
A2={
 "papers":[
  "工程复现：从零复现的目录结构、数据准备、超参与验收断言；写清最小可跑版本与常见崩溃点。",
  "对照实验：与同期/后继 2–3 个方法逐项对比（表示、监督、速度、显存、失败模式）；给出一张决策表。",
  "数据与评测：训练数据来源、评测协议、指标口径与作弊风险；讲清一个容易误读的数字。",
  "产业落地：把它放进真实生产管线的位置、上下游接口、成本与合规风险；给出上线检查清单。",
  "教学拆解：如果给一位新工程师讲这篇论文，45 分钟怎么排；三个类比、两个常见误解、五道自测题。"],
 "algos":[
  "复杂度账本：时间/显存/带宽逐项估算，给出一个具体规模下的数值；讲清瓶颈在哪。",
  "替代方案对照：与 2 个相邻算法做同一任务的对比，给出选型判据与最小复现坑。"],
 "theory":[
  "数值与实现：离散化误差、稳定性、边界条件；给一个可跑的玩具数值例子。"],
 "directions":[
  "路线分歧：两条主线的根本分歧、各自证据、什么条件下会合流。",
  "产业案例：三个真实产品/管线中的用法、成本与失败复盘。"],
 "book":[
  "工程案例：这一卷的概念在一个真实项目里的落地、接口、验收与失败复盘。"],
 "appendix":[
  "详解与索引：把这一条展开成可查的清单/对照表，并给出交叉引用与常见误用。"],
 "stories":[
  "尾声与番外：主角在新场景里遇到的新问题；用 3 个短场景把边界讲清。"]}
PARTS={"papers":10,"algos":5,"theory":4,"directions":6,"book":6,"appendix":4,"stories":5}
def main():
 papers=M.load("papers"); algs=M.load("algorithms"); theory=M.load("theory"); dirs=M.load("directions")
 stories=M.load("stories"); book=M.load("book")["sections"]; apps=M.load("appendix")
 summary=M.load("summary"); coverage=M.load("coverage")
 ctx={"book_toc":M.join(f"{s.get('label','')} {s.get('title','')}" for s in book),
  "theory_titles":M.join(t.get("title","") for t in theory),"algo_titles":M.join(a.get("name","") for a in algs),
  "paper_titles":M.join(p.get("title","") for p in papers),"trends":M.join(summary.get("trends",[]))[:900],
  "open_problems":M.join(summary.get("open_problems",[]))[:900],"future":M.join(summary.get("future",[]))[:600],
  "exam_qa":M.join(f"{q.get('question','')}（要点：{M.join(q.get('key_points',[]))}）" for q in M.load("assessments"))[:3000],
  "paper_numbers":M.join(f"{p.get('title','')}：{(p.get('experiments') or {}).get('results','')}" for p in papers)[:3000],
  "paper_years":M.join(f"{p.get('year','')} {p.get('title','')}" for p in sorted(papers,key=lambda x:str(x.get("year",""))))[:2200],
  "paper_list":M.join(f"{p.get('title','')}（{p.get('year','')}，{p.get('venue','')}）：{p.get('core_idea','')}" for p in papers)[:3200],
  "algo_list":M.join(f"{a.get('name','')}（{a.get('year','')}）：{a.get('idea','')}" for a in algs)[:2600],
  "formulas":M.join(f"{a.get('name','')}：{a.get('formula','')}" for a in algs)+"；"+M.join(f"{t.get('title','')}：{t.get('formula','')}" for t in theory),
  "algo_how":M.join(f"{a.get('name','')}：{a.get('how','')}" for a in algs)[:3000],
  "limitations":M.join(f"{p.get('title','')}：{M.join(p.get('limitations',[]) if isinstance(p.get('limitations'),list) else [str(p.get('limitations',''))])}" for p in papers)+"；领域缺口："+M.join(g.get("item","") for g in coverage.get("gaps",[])),
  "story_titles":M.join(s.get("title","") for s in stories),"dir_names":M.join(d.get("name","") for d in dirs)}
 old=json.load(open(os.path.join(ROOT,"content","tasks.json"),encoding="utf-8"))
 have={}; have_angles={}
 for t in old:
  have.setdefault((t["module"],t["item_id"]),[]).append(t["part"])
  have_angles.setdefault((t["module"],t["item_id"]),[]).append(t["angle"])
 tasks=[]
 def add(mod,item,base_part,angle,facts,title,outdir):
  p=base_part+1
  tasks.append({"id":f"{item['id']}-p{p}","module":mod,"sub":mod,"item_id":item["id"],
   "title":title,"part":p,"parts":PARTS[mod],"angle":angle,
   "target":PART,"facts":facts,"out":f"content/long/{outdir}/{item['id']}-p{p}.html",
   "avoid":"；".join(have_angles.get((mod,item["id"]),[]))})
 for p in papers:
  base=max(have.get(("papers",p["id"]),[0]))
  for i,a in enumerate(A2["papers"]): add("papers",p,base+i,a,M.facts_paper(p),p.get("title",""),"papers")
 for a in algs:
  base=max(have.get(("algos",a["id"]),[0]))
  for i,ang in enumerate(A2["algos"]): add("algos",a,base+i,ang,M.facts_algo(a),a.get("name",""),"algos")
 for t in theory:
  base=max(have.get(("theory",t["id"]),[0]))
  add("theory",t,base,A2["theory"][0],M.facts_theory(t),t.get("title",""),"theory")
 for d in dirs:
  base=max(have.get(("directions",d["id"]),[0]))
  for i,ang in enumerate(A2["directions"]): add("directions",d,base+i,ang,M.facts_dir(d,papers),d.get("name",""),"directions")
 for s in stories:
  base=max(have.get(("stories",s["id"]),[0]))
  add("stories",s,base,A2["stories"][0],M.facts_story(s),s.get("title",""),"stories")
 for sec in book:
  base=max(have.get(("book",sec["id"]),[0]))
  add("book",sec,base,A2["book"][0],M.facts_book(sec,ctx),sec.get("title",""),"book")
 for e in apps:
  base=max(have.get(("appendix",e["id"]),[0]))
  add("appendix",e,base,A2["appendix"][0],M.facts_appendix(e,ctx),e.get("title",""),"appendix")
 json.dump(tasks,open(os.path.join(ROOT,"content","tasks2.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=1)
 from collections import Counter
 print("tasks2",len(tasks),Counter(t["module"] for t in tasks),"planned cjk",len(tasks)*PART)
if __name__=="__main__": main()
