// 验收截图：页顶 4 张（首页/论文/考题/移动端故事）+ 细节 2 张（论文目录图/考题答案）
const puppeteer=require('puppeteer-core');
(async()=>{
 const root=process.argv[2], out=process.argv[3]||'/tmp';
 const b=await puppeteer.launch({executablePath:'/snap/bin/chromium',headless:true,pipe:true,
   userDataDir:'/home/whu/tmp-cr-shots',
   args:['--no-sandbox','--disable-gpu','--hide-scrollbars','--allow-file-access-from-files','--disable-dev-shm-usage']});
 const base='file://'+root+'/index.html';
 const shot=async(url,w,h,y,name,mobile)=>{
   const p=await b.newPage(); await p.setViewport({width:w,height:h,isMobile:!!mobile});
   await p.goto(url,{waitUntil:'networkidle0'}); await new Promise(r=>setTimeout(r,700));
   await p.evaluate(v=>window.scrollTo(0,v),y); await new Promise(r=>setTimeout(r,500));
   await p.screenshot({path:out+'/'+name}); await p.close();
 };
 await shot(base+'#/home',1360,900,0,'acc-home.png');
 await shot(base+'#/papers/paper-nerf-2020',1360,900,0,'acc-paper.png');
 await shot(base+'#/exam',1360,900,0,'acc-exam.png');
 await shot(base+'#/story/story-xiaoni-seven-lives',390,844,0,'acc-mobile-story.png',true);
 // 细节：论文目录 + 流水线图
 await shot(base+'#/papers/paper-nerf-2020',1360,900,3260,'acc-paper-toc.png');
 // 细节：展开第一题答案
 {
   const p=await b.newPage(); await p.setViewport({width:1360,height:900});
   await p.goto(base+'#/exam',{waitUntil:'networkidle0'}); await new Promise(r=>setTimeout(r,700));
   await p.evaluate(()=>{const b=document.querySelector('[data-reveal]'); if(b) b.click();});
   await new Promise(r=>setTimeout(r,900));
   await p.evaluate(()=>{const a=document.querySelector('.answer'); if(a) a.scrollIntoView({block:'start'});});
   await new Promise(r=>setTimeout(r,500));
   await p.screenshot({path:out+'/acc-exam-answer.png'}); await p.close();
 }
 await b.close(); console.log('shots ok');
})();
