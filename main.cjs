const { Builder, By, Key, until } = require('selenium-webdriver');
const chrome = require('selenium-webdriver/chrome');
const chromedriver = require('chromedriver');

async function convertDocsendToPDF() {
  let driver = await new Builder()
    .forBrowser('chrome')
    .setChromeOptions(new chrome.Options()
      // .headless()
      .addArguments('--disable-gpu')
      .addArguments('--no-sandbox')
      // .addArguments('--ignore-ssl-errors=yes')
      // .addArguments('--ignore-certificate-errors')
    )
    .build();

  try {
    // Navigate to the website
    await driver.get('http://deck2pdf.c           om');

    // Find the input field and enter the text
    let inputField = await driver.findElement(By.id('docsendURL'));
    await inputField.sendKeys('https://docsend.com/view/mcy8h43sjjf5hchf');

    // Find and click the convert button
    let convertButton = await driver.findElement(By.className('btn-primary'));
    await convertButton.click();

    // Wait for the file to be ready for download
    let timeout = 1200000; // 120 seconds
    let linkElement = await driver.wait(until.elementLocated(By.xpath("//a[contains(@href, '/tmp/') and contains(@href, '.pdf')]")), timeout);

    // Click the link when it's available
    await linkElement.click();

    // Sleep is usually a bad practice in automation scripts, since it can lead to unnecessary waits.
    // Here it's replaced by waiting for a specific condition or element.
    // If needed, you can wait for the download to finish using specific conditions.

  } catch (err) {
    console.error(`An error occurred: ${err}`);
  } finally {
    await driver.quit();
  }
}

// convertDocsendToPDF();

/*
const puppeteer = require('puppeteer');

async function convertDocsendToPDF() {
  // Launch a new headless browser
  const browser = await puppeteer.launch({ args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-gpu'] });

  try {
    // Create a new page
    const page = await browser.newPage();
    page.setDefaultNavigationTimeout(60000)
    // Navigate to the website
    await page.goto('http://deck2pdf.com');

    // Find the input field and enter the text
    await page.type('#docsendURL', 'https://docsend.com/view/mcy8h43sjjf5hchf');

    // Find and click the convert button
    await Promise.all([
      page.click('.btn-primary'), // Click the convert button
      page.waitForNavigation({ waitUntil: 'networkidle0' }), // Wait for the network to be idle
    ]);
    
    // Wait for the file to be ready for download
    const downloadLinkSelector = "a[href*='/tmp/'][href*='.pdf']";
    await page.waitForSelector(downloadLinkSelector); // Wait for selector to appear in page

    // Click the link to start the download
    const link = await page.$(downloadLinkSelector);
    const url = await page.evaluate(el => el.href, link);
    console.log(`Download URL: ${url}`);

    // Note: Puppeteer cannot directly download files in headless mode to your file system,
    // you need to handle the download in your specific environment or use non-headless mode.

  } catch (err) {
    console.error(`An error occurred: ${err}`);
  } finally {
    if (browser) {
      await browser.close();
    }
  }
}

convertDocsendToPDF();*/