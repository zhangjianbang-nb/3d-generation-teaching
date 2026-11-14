// 【模板】窄屏断言：标题不被截断、SVG 不被压成 6px 字、页面不横向溢出。
// 复制到 <run>/tools/mobile_probe.js 后改 CASES 里的三条路由（挑长标题页 + 带图页 + 长文页）。
// tools/mobile_probe.js —— 390px 窄屏断言：标题不被截断、SVG 不被压成 6px 字、页面不横向溢出。
// 用法：node tools/mobile_probe.js
const path = require('path');
const puppeteer = require('/tmp/node_modules/puppeteer-core');

const RUN = path.resolve(__dirname, '..');
const CASES = [
  { hash: '#/papers/paper-nerf-2020', sel: '.detail-head h1' },
  { hash: '#/algos/alg-sds', sel: '.detail-head h1' },
  { hash: '#/story/story-xiaoni-seven-lives', sel: '.detail-head h1' },
];

(async () => {
  const browser = await puppeteer.launch({
    executablePath: '/snap/bin/chromium',
    headless: true,
    pipe: true,
    args: ['--headless=new', '--no-sandbox', '--disable-gpu', '--hide-scrollbars'],
    defaultViewport: { width: 390, height: 844, isMobile: true, deviceScaleFactor: 1 },
  });
  const page = await browser.newPage();
  let fail = 0;
  for (const c of CASES) {
    await page.goto('file://' + path.join(RUN, 'site', 'index.html') + c.hash,
                    { waitUntil: 'load', timeout: 60000 });
    await new Promise(r => setTimeout(r, 900));
    const r = await page.evaluate((sel) => {
      const h1 = document.querySelector(sel);
      const cs = h1 ? getComputedStyle(h1) : null;
      const fig = document.querySelector('figure.diagram');
      const svg = fig ? fig.querySelector('svg') : null;
      const sb = svg ? svg.getBoundingClientRect() : null;
      const fb = fig ? fig.getBoundingClientRect() : null;
      return {
        h1: h1 ? h1.textContent.trim().slice(0, 40) : null,
        clamp: cs ? cs.webkitLineClamp : null,
        clipped: h1 ? (h1.scrollHeight > h1.clientHeight + 2) : null,
        h1h: h1 ? Math.round(h1.getBoundingClientRect().height) : 0,
        svgW: sb ? Math.round(sb.width) : 0,
        figW: fb ? Math.round(fb.width) : 0,
        figScrollW: fig ? fig.scrollWidth : 0,
        pageOverflow: document.documentElement.scrollWidth - 390,
      };
    }, c.sel);
    const okClamp = r.clamp === 'none' && r.clipped === false;
    const okSvg = !r.svgW || (r.svgW >= 560 && r.figScrollW > r.figW + 20);
    const okPage = r.pageOverflow <= 1;
    if (!okClamp || !okSvg || !okPage) fail++;
    console.log(`${c.hash}  h1=${r.h1h}px clamp=${r.clamp} 截断=${r.clipped} | svg=${r.svgW}/${r.figW} 可滚=${r.figScrollW > r.figW + 20} | 页面溢出=${r.pageOverflow}px  ${okClamp && okSvg && okPage ? 'OK' : 'FAIL'}`);
  }
  await browser.close();
  console.log(fail ? `窄屏断言 ${fail} 项 FAIL` : '窄屏断言 ALL PASS');
  process.exit(fail ? 1 : 0);
})().catch(e => { console.error('FAIL', e.message); process.exit(2); });
