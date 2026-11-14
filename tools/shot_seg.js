const puppeteer=require('puppeteer-core');
(async()=>{
 const [url,out,width='1360',y='0',mobile='0',h='900']=process.argv.slice(2);
 const b=await puppeteer.launch({executablePath:'/snap/bin/chromium',headless:true,pipe:true,userDataDir:'/home/whu/tmp-cr-shots',args:['--no-sandbox','--disable-gpu','--hide-scrollbars','--allow-file-access-from-files','--disable-dev-shm-usage']});
 const p=await b.newPage();
 await p.setViewport({width:+width,height:+h,deviceScaleFactor:1,isMobile:mobile==='1'});
 await p.goto(url,{waitUntil:'networkidle0',timeout:60000});
 await new Promise(r=>setTimeout(r,600));
 await p.evaluate(v=>window.scrollTo(0,v),+y);
 await new Promise(r=>setTimeout(r,500));
 await p.screenshot({path:out});
 await b.close();
})();
