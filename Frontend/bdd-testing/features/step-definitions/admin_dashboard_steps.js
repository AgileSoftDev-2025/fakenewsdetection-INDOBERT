const { Given, Then, Before, After, AfterAll, setDefaultTimeout } = require('@cucumber/cucumber');
const puppeteer = require('puppeteer');
const assert = require('assert');

setDefaultTimeout(60 * 1000);

let browser;
let page;
let testStats = { passed: 0, failed: 0, skipped: 0 };

Before(async function () {
  console.log('\n  Before');
  browser = await puppeteer.launch({ 
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });
  page = await browser.newPage();
  console.log('  ✔ passed\n');
});

After(async function () {
  console.log('\n  After');
  await browser.close();
  console.log('  ✔ passed\n');
});

Given('I am on {string}', { timeout: 10000 }, async function (pageName) {
  const stepText = `Given I am on "${pageName}"`;
  console.log(`  ${stepText}`);
  
  try {
    const response = await page.goto('http://localhost:52330/Frontend/dashboard-admin/index.html', {
      waitUntil: 'domcontentloaded',
      timeout: 8000
    });
    
    console.log(`    Status: ${response.status()}`);
    await page.waitForSelector('body', { timeout: 3000 });
    console.log('    Body content loaded');
    console.log('  ✔ passed');
    testStats.passed++;
    
  } catch (error) {
    console.log(`  ✖ failed — ${error.message}`);
    testStats.failed++;
    throw error;
  }
});

Then('I should see {string}', { timeout: 5000 }, async function (expectedText) {
  const stepText = `Then I should see "${expectedText}"`;
  console.log(`  ${stepText}`);
  
  try {
    await new Promise(resolve => setTimeout(resolve, 500));
  
    const translations = {
      'Total Checked News': 'Total Pengecekan',
      'Total Hoax Detected': 'Hoax Terdeteksi',
      'System Overview': 'Sistem Overview',
      'Machine Learning Version': 'Versi model',
      'Update Model': 'Update Model',
      'Aksi Admin': 'Aksi Admin',
    };
  
    const isVisible = await page.evaluate((text, alt) => {
      const body = (document.body && document.body.innerText) ? document.body.innerText.toLowerCase() : '';
      const t = (text || '').toLowerCase();
      const a = (alt || '').toLowerCase();
      return (t && body.includes(t)) || (a && body.includes(a));
    }, expectedText, translations[expectedText]);
    
    if (isVisible) {
      console.log(`    Found: "${expectedText}"`);
      console.log('  ✔ passed');
      testStats.passed++;
      assert.ok(true);
    } else {
      const currentText = await page.evaluate(() => document.body.innerText);
      console.log(`    Not found on page`);
      console.log(`    Page content: ${currentText.slice(0, 200)}...`);
      console.log('  ✖ failed');
      testStats.failed++;
      assert.fail(`Expected to find "${expectedText}" on the page`);
    }
  } catch (error) {
    console.log(`  ✖ failed — ${error.message}`);
    testStats.failed++;
    throw error;
  }
});

AfterAll(async function () {
  console.log('\n\n========== TEST SUMMARY ==========');
  console.log(`✔ passed:  ${testStats.passed}`);
  console.log(`✖ failed:  ${testStats.failed}`);
  console.log(`⊘ skipped: ${testStats.skipped}`);
  console.log(`━ total:   ${testStats.passed + testStats.failed + testStats.skipped}`);
  console.log('==================================\n');
});