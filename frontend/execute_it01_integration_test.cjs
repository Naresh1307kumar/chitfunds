const puppeteer = require('puppeteer');

(async () => {
  console.log('=== STARTING INTEGRATION TEST IT-01 ===');
  const browser = await puppeteer.launch({
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });

  const page = await browser.newPage();
  await page.setViewport({ width: 1366, height: 900 });

  // 1. Open Homepage
  console.log('1. Opening http://localhost:5173/...');
  await page.goto('http://localhost:5173/', { waitUntil: 'networkidle2' });
  await new Promise(r => setTimeout(r, 1500));

  // 2. Click Dashboard / Login
  console.log('2. Navigating to Login/Dashboard...');
  const loginBtn = await page.$('a[href="/login"], a[href="/member/dashboard"], .btn-primary');
  if (loginBtn) {
    await loginBtn.click();
  } else {
    await page.goto('http://localhost:5173/login', { waitUntil: 'networkidle2' });
  }
  await new Promise(r => setTimeout(r, 1500));

  // If redirected to login
  if (page.url().includes('/login')) {
    console.log('Logging in as User ID 1 (ramesh)...');
    await page.waitForSelector('input[name="username"], input[type="text"]');
    await page.type('input[name="username"], input[type="text"]', 'ramesh');
    await page.type('input[name="password"], input[type="password"]', 'ramesh1234');
    
    const submitBtn = await page.$('button[type="submit"]');
    if (submitBtn) await submitBtn.click();
    await new Promise(r => setTimeout(r, 2000));
  }

  console.log('Current URL after login:', page.url());

  // 3. Navigate to Payment Module (/member/payments)
  console.log('3. Opening Payment Module...');
  await page.goto('http://localhost:5173/member/payments', { waitUntil: 'networkidle2' });
  await new Promise(r => setTimeout(r, 2000));

  // Take screenshot of Initial State (Pending Due)
  await page.screenshot({ path: 'it01_step1_initial_due.png', fullPage: true });
  console.log('Saved it01_step1_initial_due.png');

  // 4. Click "Pay via Instant UPI / QR" if available
  const payButtons = await page.$$('button');
  let clickedPay = false;
  for (const btn of payButtons) {
    const text = await page.evaluate(el => el.textContent, btn);
    if (text.includes('Pay') || text.includes('UPI')) {
      console.log('Clicking Pay button:', text.trim());
      await btn.click();
      clickedPay = true;
      break;
    }
  }

  if (clickedPay) {
    await new Promise(r => setTimeout(r, 2000));
    // Click submit in Razorpay modal
    const modalButtons = await page.$$('button');
    for (const mbtn of modalButtons) {
      const mtext = await page.evaluate(el => el.textContent, mbtn);
      if (mtext.includes('Submit Payment Request')) {
        console.log('Submitting Payment Request in modal:', mtext.trim());
        await mbtn.click();
        await new Promise(r => setTimeout(r, 2500));
        break;
      }
    }
  }

  // 5. Open Admin Session to Verify/Approve the payment
  console.log('5. Opening Admin session to verify payment...');
  const adminPage = await browser.newPage();
  await adminPage.setViewport({ width: 1366, height: 900 });
  await adminPage.goto('http://localhost:5173/admin/login', { waitUntil: 'networkidle2' });
  await new Promise(r => setTimeout(r, 1500));

  // Admin login
  const adminUser = await adminPage.$('input[name="username"], input[type="text"]');
  if (adminUser) {
    await adminPage.type('input[name="username"], input[type="text"]', 'admin');
    await adminPage.type('input[name="password"], input[type="password"]', 'admin123');
    const adminSub = await adminPage.$('button[type="submit"]');
    if (adminSub) await adminSub.click();
    await new Promise(r => setTimeout(r, 2000));
  }

  // Navigate to Admin Payments Verification
  await adminPage.goto('http://localhost:5173/admin/payments', { waitUntil: 'networkidle2' });
  await new Promise(r => setTimeout(r, 2000));

  // Click "Verify" on pending payment
  const verifyBtns = await adminPage.$$('button');
  for (const vbtn of verifyBtns) {
    const vtext = await adminPage.evaluate(el => el.textContent, vbtn);
    if (vtext.includes('Verify') || vtext.includes('Approve')) {
      console.log('Admin clicking Verify button:', vtext.trim());
      await vbtn.click();
      await new Promise(r => setTimeout(r, 2500));
      break;
    }
  }

  await adminPage.screenshot({ path: 'it01_step2_admin_verified.png', fullPage: true });
  console.log('Saved it01_step2_admin_verified.png');
  await adminPage.close();

  // 6. Return to Member Page and verify reflection in Payment Module & Installment Tracker
  console.log('6. Refreshing Member Page to verify integration...');
  await page.reload({ waitUntil: 'networkidle2' });
  await new Promise(r => setTimeout(r, 2000));

  // Capture final screenshot of Payment Module + Transaction History
  await page.screenshot({ path: 'it01_evidence_payment_module.png', fullPage: true });
  console.log('Saved it01_evidence_payment_module.png');

  // Also check Member Dashboard (Installment Tracker)
  await page.goto('http://localhost:5173/member/dashboard', { waitUntil: 'networkidle2' });
  await new Promise(r => setTimeout(r, 2000));

  await page.screenshot({ path: 'it01_evidence_installment_tracker.png', fullPage: true });
  console.log('Saved it01_evidence_installment_tracker.png');

  await browser.close();
  console.log('=== INTEGRATION TEST IT-01 EXECUTED SUCCESSFULLY ===');
})();
