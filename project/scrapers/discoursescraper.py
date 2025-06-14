from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import json
from datetime import datetime

# ✅ Connect to running Chrome instance with your IITM session
options = Options()
options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

# ✅ No need to set user-data-dir or profile here
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

URL = "https://discourse.onlinedegree.iitm.ac.in/c/courses/tds-kb/34/l/latest"
driver.get(URL)
time.sleep(10)  # Wait for page to load

# Scroll to load more posts
for _ in range(10):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)

soup = BeautifulSoup(driver.page_source, "html.parser")

# Extract topics
posts_data = []
topics = soup.select("tr.topic-list-item")

for topic in topics:
    title_tag = topic.select_one("a.title")
    if not title_tag:
        continue

    title = title_tag.text.strip()
    link = "https://discourse.onlinedegree.iitm.ac.in" + title_tag["href"]
    date_tag = topic.select_one("td:nth-last-child(1) time")

    if not date_tag or not date_tag.has_attr("datetime"):
        continue

    date_str = date_tag["datetime"]
    date = datetime.fromisoformat(date_str.replace("Z", "+00:00"))

    if datetime(2025, 1, 1) <= date <= datetime(2025, 4, 14):
        posts_data.append({
            "title": title,
            "url": link,
            "date": date.isoformat()
        })

# Save to JSON
with open("tds_discourse_posts.json", "w", encoding="utf-8") as f:
    json.dump(posts_data, f, indent=2)

print(f"✅ Saved {len(posts_data)} Discourse posts")
driver.quit()
