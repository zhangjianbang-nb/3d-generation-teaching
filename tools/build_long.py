#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把 content/long 的分片拼成数据里的 long_html，注入 SVG 图与速查表，重打包 bundle。"""
import html as H, json, os, re, sys, glob
HERE=os.path.dirname(os.path.abspath(__file__)); ROOT=os.path.dirname(HERE)
sys.path.insert(0,HERE); import figs
DATA=os.path.join(ROOT,"site","data")
CN="一二三四五六七八九十"
def cn_num(n):
 if n<=10: return CN[n-1]
 if n<20: return "十"+CN[n-11]
 return CN[n//10-1]+"十"+(CN[n%10-1] if n%10 else "")
def load(n): return json.load(open(os.path.join(DATA,n+".json"),encoding="utf-8"))
def save(n,d):
 json.dump(d,open(os.path.join(DATA,n+".json"),"w",encoding="utf-8"),ensure_ascii=False,indent=1)
def fix_formulas(html):
 def rep(m):
  s=m.group(0).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")
  s=s.replace("&amp;lt;","&lt;").replace("&amp;gt;","&gt;").replace("&amp;amp;","&amp;")
  return s
 html=re.sub(r"\$\$[\s\S]{4,}?\$\$",rep,html)
 def rep_inline(m):
  b=m.group(1)
  if "<" in b or ">" in b: b=b.replace("<","&lt;").replace(">","&gt;")
  return "\\("+b+"\\)"
 html=re.sub(r"\\\((.+?)\\\)",rep_inline,html)
 def rep_span(m):
  attrs,body=m.group(1),m.group(2)
  if "$" in body or "\\(" in body: return m.group(0)
  if re.search(r"\\[a-zA-Z]",body): return "<span%s>\\(%s\\)</span>"%(attrs,body)
  return m.group(0)
 html=re.sub(r"<span([^>]*)>([^<]*)</span>",rep_span,html)
 return html
def renumber(html):
 n=[0]
 def rep(m):
  n[0]+=1
  return "<h3>%s · "%cn_num(n[0])
 return re.sub(r"<h3>(?:[一二三四五六七八九十]+ · )?",rep,html)
def polish(html):
 html=re.sub(r"(?<![.<])\.\.\.(?!\.)","……",html)
 return html
def add_toc(body,prefix=""):
 n=[0]; items=[]
 def rep(m):
  n[0]+=1; t=re.sub(r"<[^>]+>","",m.group(1)).strip()
  sid="%s-sec-%d"%(prefix,n[0]) if prefix else "sec-%d"%n[0]
  items.append((sid,t))
  return '<h3 id="%s">%s</h3>'%(sid,m.group(1))
 body=re.sub(r"<h3>([\s\S]*?)</h3>",rep,body)
 if len(items)<3: return body
 toc='<nav class="long-toc"><b>本页目录</b><ol>'+''.join('<li><button type="button" class="toc-link" data-sec="%s">%s</button></li>'%(i,H.escape(t)) for i,t in items)+'</ol></nav>'
 return toc+body
def footer(module,item_id,n):
 return '<p class="paper-line">本页对应：%s/%s · 共 %d 个片段</p>\n'%(module,item_id,n)
def collect(module,item_id,parts):
 fs=[]
 for p in range(1,parts+1):
  f=os.path.join(ROOT,"content","long",module,f"{item_id}-p{p}.html")
  if os.path.exists(f): fs.append((p,open(f,encoding="utf-8").read()))
 if not fs: return "",0
 body="\n".join(h for _,h in fs)
 body=re.sub(r'<p class="paper-line">[\s\S]*?</p>\s*','',body)
 return add_toc(fix_formulas(polish(renumber(body))),item_id),len(fs)
def after_toc(lh,pre):
 m=re.match(r'(<nav class="long-toc">[\s\S]*?</nav>)',lh)
 if m: return m.group(1)+pre+lh[m.end():]
 return pre+lh
def inject(module,item):
 """返回 (图前, 图后)：结构图放目录之后、正文之前，家族图/速查表收尾。"""
 if module=="papers":
  p=figs.P[item["id"]]; return figs.paper_pipeline(p), figs.paper_family(p)+figs.paper_table(p)
 if module=="algos":
  a=figs.A[item["id"]]; return figs.algo_flow(a), figs.algo_table(a)
 if module=="theory":
  t=figs.T[item["id"]]; return figs.theory_map(t), figs.theory_table(t)
 if module=="directions":
  d=figs.D[item["id"]]; return figs.dir_map(d), figs.dir_table(d)
 if module=="stories":
  s=figs.S[item["id"]]; return figs.story_map(s), figs.story_table(s)
 return "", ""
BASE=os.path.join(ROOT,"content","book-base.json")
STORY=os.path.join(ROOT,"content","book-story.json")
def book_story(sec):
 if not os.path.exists(STORY): return None
 return json.load(open(STORY,encoding="utf-8")).get(sec["id"])
def book_base(sec):
 store={}
 if os.path.exists(BASE): store=json.load(open(BASE,encoding="utf-8"))
 if sec["id"] not in store: store[sec["id"]]=sec.get("html_base") or sec.get("html","")
 json.dump(store,open(BASE,"w",encoding="utf-8"),ensure_ascii=False,indent=1)
 return store[sec["id"]]
def mark_read_levels():
 """摘要级条目必须在数据里自曝，读者才不会把摘要转述当全文机制。"""
 data=load("papers"); changed=False
 for p in data:
  if p.get("read_level") in ("abstract_only","api_verified","unverified"):
   v=p.get("verification") or ""
   if not any(k in v for k in ("摘要级","仅摘要","未读全文","未全文核验")):
    p["verification"]="摘要级（仅摘要，未全文核验）· "+v; changed=True
 if changed: save("papers",data)

def main():
 mark_read_levels()
 tasks=json.load(open(os.path.join(ROOT,"content","tasks.json"),encoding="utf-8"))
 t2=os.path.join(ROOT,"content","tasks2.json")
 if os.path.exists(t2): tasks=tasks+json.load(open(t2,encoding="utf-8"))
 by={}
 for t in tasks: by.setdefault((t["module"],t["item_id"]),[]).append(t)
 stat={}; done=0; total=0
 for (module,item_id),ts in by.items():
  parts=max(x["parts"] for x in ts)
  lh,n=collect(module,item_id,parts)
  stat[module]=stat.get(module,0)+n; total+=parts
  done+=n
  if module=="exams":
   data=load("assessments"); q=next((x for x in data if x["id"]==item_id),None)
   if not q: continue
   m=re.match(r'(<nav class="long-toc">[\s\S]*?</nav>)',lh)
   if m: lh=m.group(1)+figs.exam_formula(q)+lh[m.end():]+figs.exam_table(q)+footer("exams",item_id,n)
   else: lh=figs.exam_formula(q)+lh+figs.exam_table(q)+footer("exams",item_id,n)
   q["long_html"]=lh; save("assessments",data)
  elif module=="book":
   data=load("book"); sec=next((x for x in data["sections"] if x["id"]==item_id),None)
   if not sec: continue
   base=book_base(sec)
   sec.pop("html_base",None)
   st=book_story(sec)
   lead=''
   note=''
   if st:
    lead=('<div class="lead-label">卷首故事</div><div class="book-lead"><p>'+H.escape(st["lead"])+'</p></div>'
          +'<div class="lead-label">专业导读</div>')
    note=('<div class="craft-note"><b>本卷工匠笔记</b><ul>'
          +''.join('<li>'+H.escape(x)+'</li>' for x in st.get("note") or [])+'</ul></div>')
   else:
    lead='<div class="lead-label">专业导读</div>'
   sec["html"]=lead+base+"\n"+lh+note+figs.book_map(sec)+footer("book",item_id,n); save("book",data)
  elif module=="appendix":
   data=load("appendix"); e=next((x for x in data if x["id"]==item_id),None)
   if not e: continue
   e["long_html"]=after_toc(lh,figs.appendix_entry_fig(e))+figs.appendix_entry_table(e)+footer("appendix",item_id,n); save("appendix",data)
  else:
   name={"papers":"papers","algos":"algorithms","theory":"theory","directions":"directions","stories":"stories"}[module]
   data=load(name); ent=next((x for x in data if x["id"]==item_id),None)
   if not ent: continue
   pre,post=inject(module,ent)
   ent["long_html"]=after_toc(lh,pre)+post+footer(module,item_id,n)
   if module=="stories": ent["art"]=figs.story_art(ent)
   save(name,data)
 dom=load("domain"); dom["home_figure"]=figs.home_map(); dom["home_table"]=figs.home_table(); dom["map_figure"]=figs.map_overview()
 save("domain",dom)
 print("parts done %d/%d"% (done,total),stat)
 import bundle_data; bundle_data.build(os.path.join(ROOT,"site"))
 print("bundled")
if __name__=="__main__": main()
