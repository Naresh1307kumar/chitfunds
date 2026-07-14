import puppeteer from 'puppeteer-core';

(async () => {
  const browser = await puppeteer.launch({
    executablePath: "C:\\\\Program Files\\\\Google\\\\Chrome\\\\Application\\\\chrome.exe",
    headless: true,
  });

  const page = await browser.newPage();

  page.on('console', msg => {
    console.log(`[CONSOLE] [${msg.type()}] ${msg.text()}`);
  });

  page.on('pageerror', err => {
    console.error(`[EXCEPTION] ${err.toString()}`);
  });

  page.on('requestfailed', request => {
    console.log(`[REQ FAIL] ${request.url()} - ${request.failure().errorText}`);
  });

  console.log('Navigating to http://localhost:5173/ ...');
  try {
    await page.goto('http://localhost:5173/', { waitUntil: 'networkidle2', timeout: 5000 });
  } catch (e) {
    console.log('Navigation finished with some timeout / idle state.');
  }

  // Wait another second for any async rendering
  await new Promise(resolve => setTimeout(resolve, 2000));

  await browser.close();
  console.log('Done checking console.');
})();
