const puppeteer = require('puppeteer');

(async () => {
  try {
    const browser = await puppeteer.launch({ headless: 'new' });
    const page = await browser.newPage();
    await page.setViewport({ width: 1366, height: 768 });

    const artDir = 'C:/Users/nares/.gemini/antigravity/brain/f3eb3d7a-3368-4f7d-ad6c-f8c0de697e83';

    // 1. Landing Page
    console.log('Capturing Landing Page...');
    await page.goto('http://localhost:5173/', { waitUntil: 'networkidle2' });
    await page.screenshot({ path: `${artDir}/user_screen_landing.png` });

    // 2. Member Login Page
    console.log('Capturing Login Page...');
    await page.goto('http://localhost:5173/login', { waitUntil: 'networkidle2' });
    await page.screenshot({ path: `${artDir}/user_screen_login.png` });

    // 3. Admin Dashboard
    console.log('Logging in as Admin...');
    await page.goto('http://localhost:5173/admin/login', { waitUntil: 'networkidle2' });
    await page.type('input[type="text"], input[name="username"], input[name="email"]', 'admin');
    await page.type('input[type="password"]', 'Admin@123');
    await page.click('button[type="submit"]');
    await new Promise(r => setTimeout(r, 1500));
    await page.screenshot({ path: `${artDir}/user_screen_admin_dashboard.png` });

    // Logout Admin
    await page.evaluate(() => localStorage.clear());

    // 4. Member Dashboard
    console.log('Logging in as Member...');
    await page.goto('http://localhost:5173/login', { waitUntil: 'networkidle2' });
    await page.type('input[type="text"], input[name="username"], input[name="email"]', 'naresh56');
    await page.type('input[type="password"]', 'naresh123').catch(() => {});
    await page.click('button[type="submit"]');
    await new Promise(r => setTimeout(r, 1500));
    await page.screenshot({ path: `${artDir}/user_screen_member_dashboard.png` });

    // 5. KYC Verification Page
    console.log('Capturing KYC Verification Page...');
    await page.goto('http://localhost:5173/member/kyc', { waitUntil: 'networkidle2' });
    await page.screenshot({ path: `${artDir}/user_screen_kyc_verification.png` });

    await browser.close();
    console.log('ALL 5 LIVE SCREENS CAPTURED SUCCESSFULLY!');
  } catch (err) {
    console.error('Error capturing screenshots:', err);
  }
})();
