import json  
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import os
import re

BASE_URL = "https://www.shl.com"

def get_driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123 Safari/537.36")
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def scrape_catalog():
    driver = get_driver()
    print("Navigating to product catalog...")

    assessments = []
    seen = set()

    # Loop for section 1 (type=1)
    for section_type in [1, 2]:
        print(f"\n🔍 Scraping Section {section_type}...")
        current_page = 0
        while True:
            start = current_page * 12
            url = f"{BASE_URL}/solutions/products/product-catalog/?start={start}&type={section_type}&type={section_type}"
            print(f"Loading page {current_page + 1}: {url}")
            driver.get(url)
            time.sleep(3)

            soup = BeautifulSoup(driver.page_source, "html.parser")
            links = soup.select("a[href*='/products/product-catalog/view/']")
            if not links:
                print(f"⚠️ No more products found in section {section_type}.")
                break

            print(f"Found {len(links)} product links.")
            for link in links:
                name = link.get_text(strip=True)
                url = link["href"]
                full_url = url if url.startswith("http") else BASE_URL + url

                if full_url in seen:
                    continue
                seen.add(full_url)

                print(f"Scraping: {name} -> {full_url}")
                details = scrape_assessment_details(driver, full_url)
                assessments.append({
                    "assessment_name": name,
                    "url": full_url,
                    **details
                })

            current_page += 1

    driver.quit()
    return assessments

def scrape_assessment_details(driver, url):
    driver.get(url)
    time.sleep(2)
    soup = BeautifulSoup(driver.page_source, "html.parser")

    duration = None
    remote_support = "No"
    adaptive_support = "No"
    test_type = "General"

    text = soup.get_text(separator=' ').lower()

    match = re.search(r'(\d+\s?(min|minutes?|mins?))', text)
    if match:
        duration = match.group(1)

    if "remote proctoring" in text or "remote support" in text or "remote" in text:
        remote_support = "Yes"

    if "adaptive" in text:
        adaptive_support = "Yes"

    if any(kw in text for kw in ["code", "coding", "developer", "programming"]):
        test_type = "Coding"
    elif any(kw in text for kw in ["cognitive", "problem solving", "logical reasoning"]):
        test_type = "Cognitive"
    elif any(kw in text for kw in ["communication", "verbal", "written", "language"]):
        test_type = "Communication"
    elif any(kw in text for kw in ["sales", "management", "business", "customer"]):
        test_type = "Business"

    return {
        "remote_support": remote_support,
        "adaptive_support": adaptive_support,
        "duration": duration,
        "test_type": test_type
    }

if __name__ == "__main__":
    assessments = scrape_catalog()
    if assessments:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        output_path = os.path.join(script_dir, "assessments.json")
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(assessments, f, indent=2, ensure_ascii=False)
        print(f"\n✅ Scraped {len(assessments)} assessments saved to {output_path}")
    else:
        print("⚠️ No assessments scraped.")
