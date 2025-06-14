from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import json
import argparse
from datetime import datetime, timedelta
import re

class TDSDiscourseScraperEnhanced:
    def __init__(self):
        # Connect to running Chrome instance with IITM session
        options = Options()
        options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()), 
            options=options
        )
    
    def scrape_discourse_posts(self, start_date, end_date, course_code="tds-kb"):
        """Scrape Discourse posts within date range"""
        URL = f"https://discourse.onlinedegree.iitm.ac.in/c/courses/{course_code}/34/l/latest"
        self.driver.get(URL)
        time.sleep(10)
        
        # Scroll to load more posts
        for _ in range(15):  # Increased scrolling
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
        
        soup = BeautifulSoup(self.driver.page_source, "html.parser")
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
            
            if start_date <= date <= end_date:
                # Scrape individual post content
                post_content = self.scrape_post_content(link)
                posts_data.append({
                    "title": title,
                    "url": link,
                    "date": date.isoformat(),
                    "content": post_content
                })
        
        return posts_data
    
    def scrape_post_content(self, url):
        """Scrape content from individual post"""
        try:
            self.driver.get(url)
            time.sleep(3)
            soup = BeautifulSoup(self.driver.page_source, "html.parser")
            
            # Extract main post content
            posts = soup.select(".topic-post")
            content_parts = []
            
            for post in posts[:5]:  # Get first 5 posts in thread
                post_body = post.select_one(".cooked")
                if post_body:
                    content_parts.append(post_body.get_text().strip())
            
            return "\n\n".join(content_parts)
        except Exception as e:
            print(f"Error scraping {url}: {e}")
            return ""
    
    def close(self):
        self.driver.quit()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Scrape TDS Discourse posts')
    parser.add_argument('--start-date', required=True, help='Start date (YYYY-MM-DD)')
    parser.add_argument('--end-date', required=True, help='End date (YYYY-MM-DD)')
    parser.add_argument('--output', default='tds_discourse_posts_enhanced.json', help='Output file')
    
    args = parser.parse_args()
    
    start_date = datetime.fromisoformat(args.start_date)
    end_date = datetime.fromisoformat(args.end_date)
    
    scraper = TDSDiscourseScraperEnhanced()
    try:
        posts = scraper.scrape_discourse_posts(start_date, end_date)
        
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(posts, f, indent=2)
        
        print(f"✅ Scraped {len(posts)} posts to {args.output}")
    finally:
        scraper.close()