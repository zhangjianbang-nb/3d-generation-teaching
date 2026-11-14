#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase C：按模块生成深读任务清单（每片段目标 3600 汉字）。"""
import json, os, re
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__))); DATA=os.path.join(ROOT,"site","data")
OUT=os.path.join(ROOT,"content","tasks.json")
PART=3600
SUB={"papers":"papers","algos":"algos","theory":"theory","directions":"directions","stories":"stories","exams":"exams","book":"book","appendix":"appendix"}
ANGLES={
 "papers":[
  "问题现场：这篇论文之前的主流做法、具体痛点、为什么非改不可；用一个具体场景开场。",
  "方法总览：核心架构、数据流、关键模块与它们的分工；画清楚输入到输出的每一步。",
  "公式与训练：目标函数、变量含义、梯度/采样、训练配方与关键超参；给出一个数值玩具例子。",
  "实验与证据：数据集、基线、主要结果、消融；只使用给定事实中的数字，讲清提升来自哪里。",
  "边界与影响：失效条件、被谁继承或替代、工程复现清单与验收断言；写清哪里不能照搬。"],
 "algos":[
  "机制推导：问题、核心思想、公式逐步解释、与相邻算法的数学差别。",
  "系统与实现：复杂度、显存/通信、伪代码思路、工程坑与调参顺序。",
  "对比与失效：与相邻算法逐项对比、失效条件、选型建议、三道练习。"],
 "theory":[
  "直觉与定义：一句话、严格定义、为什么需要、常见误解。",
  "推导与例子：公式推导、符号解释、数值例子、伪代码思路。",
  "边界与系统：失效条件、系统取值、与相邻理论的差别、练习。"],
 "directions":[
  "问题全景：这个方向要解决什么、边界在哪、为什么其他方向替代不了。",
  "路线对比：主要技术路线、代表工作、代价对比、选型判据。",
  "论文串联：关键论文之间的继承、改进、替代关系；按年代讲清断裂与延续。",
  "系统与评测：工程瓶颈、评测指标、开放问题与下一步。"],
 "stories":[
  "第一幕扩展：场景、人物、冲突；把故事背景展开成可拍的画面。",
  "第二幕扩展：危机爆发、抉择、代价；让技术机制通过角色行动被看见。",
  "第三幕扩展与对话：解决、新问题、角色辩论；辩论要映射真实的技术分歧。",
  "映射细化与教学用法：每个角色/道具对应哪个机制，为什么像、哪里不像；45/90 分钟怎么讲。"],
 "exams":[
  "答案深化：三档答案（及格/良好/满分）、机制解析、数字底账、评分演练。",
  "变体与追问：3 个变体题、5 个追问、扣分点、常见错误与教学建议。"],
 "book":[
  "叙事开场：这一卷要回答的问题、一个具体场景、为什么上一卷的答案不够。",
  "机制一：核心概念、公式、数据流；用一个例子走通。",
  "机制二：训练、推理或系统；讲清代价与失败模式。",
  "证据与反例：论文、模型配方、实验数字、失败案例；只使用给定事实。",
  "工程笔记与自测：代码思路、调参、检查清单、五道自测题。"],
 "appendix":[
  "主体内容：按条目主题展开，给出定义、分类与一张速查表。",
  "深化与例子：具体案例、数字、代码或表格；讲清一个容易错的细节。",
  "速查与练习：清单、对比表、自测题与延伸阅读。"]}
def load(n): return json.load(open(os.path.join(DATA,n+".json"),encoding="utf-8"))
def strip_html(s,limit=1200):
 s=re.sub(r"<[^>]+>"," ",s or ""); s=re.sub(r"\s+"," ",s).strip(); return s[:limit]
def join(xs): return "；".join(str(x) for x in xs if x)
def facts_paper(p):
 exp=p.get("experiments") or {}
 return "\n".join([f"论文：{p.get('title','')} / {p.get('title_zh','')}（{p.get('year','')}，{p.get('venue','')}）",
  f"摘要：{p.get('summary','')}",f"背景：{p.get('background','')}",f"问题：{p.get('problem','')}",
  f"核心思想：{p.get('core_idea','')}",f"架构：{strip_html(p.get('architecture',''),700)}",
  f"公式：{p.get('formula','')}",f"训练：{strip_html(p.get('training',''),500)}",
  f"实验：数据集 {exp.get('datasets','')}；基线 {exp.get('baselines','')}；结果 {exp.get('results','')}；消融 {exp.get('ablations','')}",
  f"局限：{'；'.join(p.get('limitations',[]) if isinstance(p.get('limitations'),list) else [str(p.get('limitations',''))])}",
  f"影响：{p.get('impact','')}"])[:3200]
def facts_algo(a):
 return "\n".join([f"算法：{a.get('name','')}（{a.get('year','')}，{a.get('tier','')}）",f"问题：{a.get('problem','')}",
  f"核心思想：{a.get('idea','')}",f"工作原理：{a.get('how','')}",f"公式：{a.get('formula','')}",
  f"流程：{join(a.get('flow',[]))}",f"优势：{join(a.get('pros',[]))}",f"不足：{join(a.get('cons',[]))}"])[:2800]
def facts_theory(t):
 return "\n".join([f"理论：{t.get('title','')}",f"一句话：{t.get('plain','')}",f"定义：{t.get('definition','')}",
  f"公式：{t.get('formula','')}",f"推导：{t.get('derivation','')}",f"例子：{t.get('example','')}",
  f"伪代码：{t.get('pseudocode','')}",f"失效条件：{join(t.get('limits',[]))}",f"系统取值：{t.get('system_note','')}"])[:3200]
def facts_dir(d,papers):
 titles=[p.get("title","") for pid in d.get("key_papers",[]) for p in papers if p["id"]==pid]
 return "\n".join([f"方向：{d.get('name','')}（{d.get('name_en','')}）",f"核心问题：{d.get('question','')}",
  f"为什么重要：{d.get('why','')}",f"关键技术：{join(d.get('core_tech',[]))}",f"关键论文：{join(titles)}",
  f"近年：{d.get('recent','')}",f"挑战：{join(d.get('challenges',[]))}"])[:3000]
def facts_story(s):
 roles="；".join(f"{r.get('role','')}→{r.get('maps_to','')}：{r.get('duty','')}" for r in s.get("roles",[]))
 plot="；".join(f"{x.get('act','')}：{strip_html(x.get('text',''),420)}" for x in s.get("plot",[]))
 mapping="；".join(f"{m.get('concept','')}={m.get('entity','')}" for m in s.get("mapping",[]))
 return "\n".join([f"故事：{s.get('title','')}",f"场景：{s.get('scene','')}",f"角色：{roles}",
  f"剧情：{plot}",f"映射：{mapping}",f"类比边界：{join(s.get('boundaries',[]))}"])[:4200]
def facts_exam(q):
 return "\n".join([f"题目（第 {q.get('level')} 层 / {q.get('module')}）：{q.get('question','')}",
  f"参考答案：{q.get('answer','')}",f"解析：{q.get('explanation','')}",f"判分点：{join(q.get('key_points',[]))}",
  f"常见错误：{join(q.get('common_errors',[]))}",f"评分标准：{q.get('rubric','')}"])[:2200]
def facts_book(sec,ctx):
 return "\n".join([f"卷：{sec.get('label','')} {sec.get('title','')}（{sec.get('en','')}）",
  f"本卷导语：{strip_html(sec.get('html',''),1600)}",f"全书结构：{ctx['book_toc']}",
  f"相关理论卡：{ctx['theory_titles']}",f"相关算法卡：{ctx['algo_titles']}",f"相关论文：{ctx['paper_titles']}",
  f"领域趋势：{ctx['trends']}",f"开放问题：{ctx['open_problems']}",f"未来机会：{ctx['future']}"])[:4000]
def facts_appendix(ap,ctx):
 extra={"app-glossary-a":"术语候选："+ctx['algo_titles']+"；"+ctx['theory_titles'],
  "app-glossary-b":"术语候选："+ctx['theory_titles']+"；"+ctx['paper_titles'],
  "app-glossary-c":"术语候选："+ctx['paper_titles']+"；"+ctx['dir_names'],
  "app-formulas":"公式素材："+ctx['formulas'],"app-numbers":"论文实验数字："+ctx['paper_numbers'],
  "app-timeline":"论文年份与标题："+ctx['paper_years'],"app-papers":"论文清单："+ctx['paper_list'],
  "app-algos":"算法清单："+ctx['algo_list'],"app-recipes":"配方线索："+ctx['paper_list'],
  "app-debug":"失效与缺口："+ctx['limitations'],"app-eval":"评测素材："+ctx['paper_numbers'],
  "app-datasets":"数据集线索："+ctx['paper_list'],"app-code":"实现素材："+ctx['algo_how'],
  "app-hardware":"系统素材："+ctx['algo_how'],"app-myths":"误区素材："+ctx['limitations'],
  "app-interview":"题库素材："+ctx['exam_qa'],"app-teaching":"教学素材："+ctx['exam_qa']+"；故事："+ctx['story_titles'],
  "app-open":"开放问题："+ctx['open_problems']+"；趋势："+ctx['trends'],"app-reading":"阅读线索："+ctx['paper_list']+"；方向："+ctx['dir_names'],
  "app-course":"教学素材："+ctx['exam_qa']+"；故事："+ctx['story_titles']}.get(ap["id"],"")
 return "\n".join([f"附录条目：{ap.get('title','')}",f"条目说明：{ap.get('summary','')}",extra,f"全书结构：{ctx['book_toc']}"])[:3800]
def main():
 papers=load("papers");algos=load("algorithms");theory=load("theory");dirs=load("directions");stories=load("stories");exams=load("assessments");book=load("book");app=load("appendix");summary=load("summary");coverage=load("coverage")
 ctx={"book_toc":join(f"{s.get('label','')} {s.get('title','')}" for s in book["sections"]),
  "theory_titles":join(t.get("title","") for t in theory),"algo_titles":join(a.get("name","") for a in algos),
  "paper_titles":join(p.get("title","") for p in papers),"trends":join(summary.get("trends",[]))[:900],
  "open_problems":join(summary.get("open_problems",[]))[:900],"future":join(summary.get("future",[]))[:600],
  "exam_qa":join(f"{q.get('question','')}（要点：{join(q.get('key_points',[]))}）" for q in exams)[:3000],
  "paper_numbers":join(f"{p.get('title','')}：{(p.get('experiments') or {}).get('results','')}" for p in papers)[:3000],
  "paper_years":join(f"{p.get('year','')} {p.get('title','')}" for p in sorted(papers,key=lambda x:str(x.get("year",""))))[:2200],
  "paper_list":join(f"{p.get('title','')}（{p.get('year','')}，{p.get('venue','')}）：{p.get('core_idea','')}" for p in papers)[:3200],
  "algo_list":join(f"{a.get('name','')}（{a.get('year','')}）：{a.get('idea','')}" for a in algos)[:2600],
  "formulas":join(f"{a.get('name','')}：{a.get('formula','')}" for a in algos)+"；"+join(f"{t.get('title','')}：{t.get('formula','')}" for t in theory),
  "algo_how":join(f"{a.get('name','')}：{a.get('how','')}" for a in algos)[:3000],
  "limitations":join(f"{p.get('title','')}：{join(p.get('limitations',[]) if isinstance(p.get('limitations'),list) else [str(p.get('limitations',''))])}" for p in papers)+"；领域缺口："+join(g.get("item","") for g in coverage.get("gaps",[])),
  "story_titles":join(s.get("title","") for s in stories),"dir_names":join(d.get("name","") for d in dirs)}
 tasks=[]
 def add(mod,item_id,title,facts,parts):
  angles=ANGLES[mod]; assert parts<=len(angles),(mod,parts)
  for i in range(parts):
   tasks.append({"id":f"{item_id}-p{i+1}","module":mod,"sub":SUB[mod],"item_id":item_id,"title":title,
    "part":i+1,"parts":parts,"angle":angles[i],"target":PART,"facts":facts,
    "avoid":"；".join(angles[:i]) if i else "（无）","out":f"content/long/{SUB[mod]}/{item_id}-p{i+1}.html"})
 for p in papers: add("papers",p["id"],p.get("title",p["id"]),facts_paper(p),5)
 for a in algos: add("algos",a["id"],a.get("name",a["id"]),facts_algo(a),3)
 for t in theory: add("theory",t["id"],t.get("title",t["id"]),facts_theory(t),3)
 for d in dirs: add("directions",d["id"],d.get("name",d["id"]),facts_dir(d,papers),4)
 for s in stories: add("stories",s["id"],s.get("title",s["id"]),facts_story(s),4)
 for q in exams: add("exams",q["id"],q.get("id",""),facts_exam(q),2)
 for sec in book["sections"]: add("book",sec["id"],sec.get("title",sec["id"]),facts_book(sec,ctx),5)
 for ap in app: add("appendix",ap["id"],ap.get("title",ap["id"]),facts_appendix(ap,ctx),3)
 json.dump(tasks,open(OUT,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
 from collections import Counter
 print("tasks:",len(tasks));print(Counter(t["module"] for t in tasks));print("planned CJK:",len(tasks)*PART)
if __name__=="__main__": main()
