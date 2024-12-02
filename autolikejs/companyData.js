const { Builder, By, Key, until } = require("selenium-webdriver");
const chrome = require("selenium-webdriver/chrome");
const options = new chrome.Options();
options.addArguments("--headless"); // Run in headless mode
options.addArguments("--disable-gpu");
options.addArguments("--no-sandbox");
options.addArguments("--disable-dev-shm-usage");

const scrap = async (url) => {
  let driver = await new Builder()
    .forBrowser("chrome")
    .setChromeOptions(options)
    .build();

  let object = {};
  await driver.get(url);
  const element = await driver.findElement(
    By.xpath('//section[@class="main-content"]')
  );
  const htmlContent = await element.getAttribute("innerHTML");
  object.html = htmlContent;
  let lists = await driver.findElements(By.xpath('//li'))
  for (let list of lists) {
    console.log(list)
  }
};

const fs = require("fs");

try {
  // Read data.json file synchronously
  const data = fs.readFileSync("data.json", "utf8");

  // Parse JSON data
  const jsonArray = JSON.parse(data);
  let scrapedData = jsonArray.map((item) => {
    return scrap(item.get_absolute_url);
  });

  console.log(scrapedData);
} catch (err) {
  console.error("Error reading file:", err);
}
