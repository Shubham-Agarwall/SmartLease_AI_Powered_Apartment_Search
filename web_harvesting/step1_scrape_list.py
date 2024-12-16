import random
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait

def scrape_property_list(base_url, pages=11, output_path="output/properties_stage_1.csv", user_agent=None):
    """Step 1: Scrape property URLs, titles, and addresses."""
    def get_driver():
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--start-maximized")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        if user_agent:
            options.add_argument(f"user-agent={user_agent}")
        return webdriver.Chrome(options=options)

    def wait_for_page_load(driver, timeout=15):
        WebDriverWait(driver, timeout).until(
            lambda d: d.execute_script('return document.readyState') == 'complete'
        )

    properties = []
    for page in range(1, pages + 1):
        url = f"{base_url}{page}/"
        driver = get_driver()
        try:
            driver.get(url)
            wait_for_page_load(driver)
            for i in range(1, 41):
                try:
                    article_xpath = f'/html/body/div[1]/main/section/div[1]/section[2]/div[2]/ul/li[{i}]/article'
                    article = driver.find_element(By.XPATH, article_xpath)
                    property_url = article.get_attribute("data-url")
                    property_title = article.get_attribute("data-streetaddress")
                    address_xpath = article_xpath + '/header/div[1]/a/div[2]'
                    property_address = driver.find_element(By.XPATH, address_xpath).text.strip()
                    if property_url and property_title:
                        properties.append({
                            "property_url": property_url,
                            "property_title": property_title,
                            "property_address": property_address,
                        })
                except Exception:
                    continue
            time.sleep(random.uniform(1, 3))
        finally:
            driver.quit()

    pd.DataFrame(properties).to_csv(output_path, index=False)
    print(f"Step 1 completed. Data saved to {output_path}")
