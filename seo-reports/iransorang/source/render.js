const { chromium } = require('playwright');
const path = require('path');

(async () => {
  const [, , input, output] = process.argv;
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto('file://' + path.resolve(input), { waitUntil: 'load' });
  await page.evaluate(() => document.fonts.ready);
  await page.pdf({
    path: output,
    format: 'A4',
    printBackground: true,
    displayHeaderFooter: true,
    headerTemplate: '<div></div>',
    footerTemplate:
      '<div style="width:100%;font-size:8px;color:#5B6B73;padding:0 13mm;display:flex;justify-content:space-between;font-family:Arial,sans-serif;">' +
      '<span>iransorang.com — SEO research &amp; 25-article plan</span>' +
      '<span><span class="pageNumber"></span> / <span class="totalPages"></span></span></div>',
    margin: { top: '15mm', bottom: '17mm', left: '13mm', right: '13mm' },
  });
  await browser.close();
})();
