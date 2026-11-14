#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""批量生成长文 HTML 片段（本地 18891 API，断点续跑，3 路并发）。"""
import argparse, concurrent.futures, json, os, re, time, urllib.request
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TASKS=os.path.join(ROOT,"content","tasks.json")
API="http://127.0.0.1:18891/v1/chat/completions"; MODEL="DeepSeek-V4.1-Flash-1017-TF"
STYLE="""你是《3D AI 生成全书》的技术作者，读者是有工程背景的中文读者。写作要求：
1. 只输出 HTML 片段，不要 markdown 围栏，不要 <html>/<body>/<script>/<style>。
2. 用 <h3>一 · 小标题</h3> 组织 4–6 节；正文用 <p>；列表用 <ul><li>；表格用 <table class="mini"><thead>…</thead><tbody>…</tbody></table>；公式用 <div class="formula">$$…$$</div>；禁止 <pre>。
3. 目标 3600 个汉字，不得少于 3200 字。信息密度高，不写套话，不重复开头，不重复其他部分已经讲过的内容。
4. 每个部分至少出现：一个具体机制、一个公式或伪代码思路、一个系统代价或失败模式、一个具体例子。
5. 不编造实验数字、引用页码、年份；只使用给定事实中的数字，没有就定性表述。禁止“大概/可能/一般来说”糊过去。
6. 不要写“总结”“结语”式收尾；最后一段落在具体机制或工程判断上。
7. 末尾加 <p class="paper-line">对应：{module}/{item_id} · 第 {part}/{parts} 部分</p>。"""
STORY_STYLE="""你是《3D AI 生成全书》的故事作者，读者是有工程背景、但想先建立直觉的中文读者。写作要求：
1. 只输出 HTML 片段，不要 markdown 围栏，不要 <html>/<body>/<script>/<style>。
2. 用 <h3>一 · 场景名</h3> 组织 3–5 幕。每一幕先写具体场景、人物动作与对话，让冲突自己说话；不要写成论文或产品说明。
3. 目标 3600 个汉字，不得少于 3200 字。故事要有推进：旧秩序 → 危机 → 抉择 → 新秩序 → 新问题；人物要有欲望、误判与代价。
4. 每一幕至少包含：一个可感知的细节（声音、气味、时间压力）、一次角色抉择、一个技术机制的“翻译”（让角色用行话或比喻说出表示/渲染/蒸馏/拓扑/材质）。
5. 每个部分末尾加一小节 <h3>工匠笔记</h3>：用 3–5 条把本幕的场景逐条映射到技术概念，并写一条“这个类比哪里不像”。
6. 不编造实验数字、引用页码、年份；只使用给定事实中的数字，没有就定性表述。
7. 末尾加 <p class="paper-line">对应：{module}/{item_id} · 第 {part}/{parts} 部分</p>。"""
def cjk(s): return len(re.findall(r"[\u4e00-\u9fff]",s))
def clean(s):
 s=s.strip(); s=re.sub(r"^```(?:html)?\s*","",s); s=re.sub(r"\s*```$","",s)
 s=re.sub(r"<script[\s\S]*?</script>","",s,flags=re.I); s=re.sub(r"<style[\s\S]*?</style>","",s,flags=re.I)
 if "<html" in s.lower():
  m=re.search(r"<body[^>]*>([\s\S]*?)</body>",s,re.I); s=m.group(1) if m else re.sub(r"<[^>]+>","",s)
 return s.strip()
def balanced(s):
 checks=[("<p","</p>"),("<h3","</h3>"),("<table","</table>"),("<ul","</ul>"),("<div class=\"formula\"","</div>")]
 for a,b in checks:
  if s.count(a)!=s.count(b): return False, a
 if s.count("$$")%2: return False,"$$"
 return True,""
def call(prompt,max_tokens=8192,pad=0):
 prompt=prompt.replace("→"," 到 ")
 if pad: prompt=prompt+"\n请开始写作。"+"。"*pad
 body={"model":MODEL,"messages":[{"role":"user","content":prompt}],"max_tokens":max_tokens,"temperature":0.65,"chat_template_kwargs":{"enable_thinking":False}}
 req=urllib.request.Request(API,data=json.dumps(body).encode(),headers={"Content-Type":"application/json"})
 with urllib.request.urlopen(req,timeout=900) as r: d=json.loads(r.read())
 ch=d["choices"][0]
 return ch["message"]["content"],ch.get("finish_reason")
def build_prompt(t):
 style=STORY_STYLE if t.get("module")=="stories" else STYLE
 return style.format(module=t["module"],item_id=t["item_id"],part=t["part"],parts=t["parts"])+f"""

本次任务：为《{t['title']}》写深读的第 {t['part']}/{t['parts']} 部分。
本部分主题：{t['angle']}
只写这一部分，不要写导语式总结，不要预告其他部分。
前文已经写过的主题（不要重复，也不要换词重讲）：
{t.get('avoid','（无）')}

可用事实（不得超出这些事实编造数字）：
{t['facts']}
"""
def gen_one(t,force=False):
 out=os.path.join(ROOT,t["out"])
 if not force and os.path.exists(out):
  s=open(out,encoding="utf-8").read()
  if cjk(s)>=3000: return ("skip",t["id"],cjk(s))
 prompt=build_prompt(t); last=""
 for attempt in range(3):
  try:
   s,fin=call(prompt); s=clean(s); n=cjk(s); ok,bad=balanced(s)
   if n<2600:
    prompt=build_prompt(t)+f"\n\n上一版只有 {n} 个汉字，明显偏短。请扩写到 3600 字左右，增加具体机制、公式解释、系统代价与例子，不要重复已有句子。"; last=s; continue
   if fin=="length" or not ok:
    prompt=build_prompt(t)+"\n\n上一版被截断或标签不闭合（"+bad+"）。请压缩到 3400 字左右，确保所有标签闭合、公式 $$ 成对，再输出完整片段。"; last=s; continue
   if "<pre" in s.lower():
    s=re.sub(r"<pre[\s\S]*?</pre>",lambda m:'<div class="formula">'+re.sub(r"<[^>]+>","",m.group(0)).strip()+"</div>",s,flags=re.I)
   if "<h3" not in s: s="<h3>一 · "+t["angle"]+"</h3>\n"+s
   os.makedirs(os.path.dirname(out),exist_ok=True); open(out,"w",encoding="utf-8").write(s.strip()+"\n")
   return ("ok",t["id"],n)
  except Exception as e:
   last=f"ERR {e}"; time.sleep(2+attempt*3)
   # 引擎在特定 token 长度上缺 _topk_sel Triton 变体（MissingTritonVariant→500）；
   # 追加几个 token 把长度推离边界再试。
   prompt=prompt+"\n请开始写作。"+"。"*(attempt+1)
 return ("fail",t["id"],str(last)[:200])
def main():
 ap=argparse.ArgumentParser(); ap.add_argument("--workers",type=int,default=3); ap.add_argument("--limit",type=int,default=0); ap.add_argument("--module",default=""); ap.add_argument("--force",action="store_true"); ap.add_argument("--tasks",default=TASKS)
 args=ap.parse_args(); tasks=json.load(open(args.tasks,encoding="utf-8"))
 if args.module: tasks=[t for t in tasks if t["module"]==args.module]
 todo=[]
 for t in tasks:
  out=os.path.join(ROOT,t["out"])
  if args.force or not os.path.exists(out) or cjk(open(out,encoding="utf-8").read())<3000: todo.append(t)
 if args.limit: todo=todo[:args.limit]
 print(f"todo={len(todo)} workers={args.workers}",flush=True)
 done=ok=fail=skip=0; t0=time.time()
 with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as ex:
  futs={ex.submit(gen_one,t,args.force):t for t in todo}
  for fut in concurrent.futures.as_completed(futs):
   st,tid,info=fut.result(); done+=1
   if st=="ok": ok+=1
   elif st=="fail": fail+=1
   else: skip+=1
   el=time.time()-t0; rate=done/el*3600 if el else 0
   print(f"[{done}/{len(todo)}] {st} {tid} cjk={info} elapsed={el/60:.1f}m rate={rate:.0f}/h",flush=True)
   with open(os.path.join(ROOT,"content","gen-progress.jsonl"),"a",encoding="utf-8") as f:
    f.write(json.dumps({"ts":time.strftime("%Y-%m-%d %H:%M:%S"),"status":st,"id":tid,"info":str(info)},ensure_ascii=False)+"\n")
 print(f"DONE ok={ok} fail={fail} skip={skip} elapsed={(time.time()-t0)/60:.1f}m",flush=True)
if __name__=="__main__": main()
