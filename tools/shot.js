const puppeteer=require('puppeteer-core');
(async()=>{
 const [url,out,width='1360',mobile='0']=process.argv.slice(2);
 const b=await puppeteer.launch({executablePath:'/snap/bin/chromium',headless:'new',args:['--no-sandbox','--disable-gpu','--hide-scrollbars','--allow-file-access-from-files']});
 const p=await b.newPage();
 await p.setViewport({width:+width,height:900,deviceScaleFactor:1,isMobile:mobile==='1'});
 await p.goto(url,{waitUntil:'networkidle0',timeout:60000});
 await new Promise(r=>setTimeout(r,800));
 const diag=await p.evaluate(()=>{
  const svgs=[...document.querySelectorAll('svg')].length;
  const figs=[...document.querySelectorAll('figure')].length;
  const tables=[...document.querySelectorAll('table')].length;
  const h=document.body.scrollHeight;
  const over=[...document.querySelectorAll('body *')].filter(e=>{const r=e.getBoundingClientRect();return r.width>0&&r.right>document.documentElement.clientWidth+2}).slice(0,5).map(e=>e.tagName+'.'+(e.className||''));
  return {h,svgs,figs,tables,over};
 });
 console.log(JSON.stringify(diag));
 await p.screenshot({path:out,fullPage:true});
 await b.close();
})();
