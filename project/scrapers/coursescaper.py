from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

# 🔁 UPDATE THIS TO YOUR CHROME PROFILE PATH
chrome_profile_path = r"C:\Users\prana\AppData\Local\Google\Chrome\User Data\Profile 5"

options = Options()
options.add_argument(f"--user-data-dir={chrome_profile_path}")
options.add_argument("profile-directory=Profile 1")  # or "Default"

driver = webdriver.Chrome(options=options)

# Load TDS Jan 2025 Course Content Page
driver.get("https://tds.s-anand.net/#/2025-01/")
time.sleep(15)  # Wait for page & JavaScript to fully load

# Save full HTML dump
with open("tds_course_dump.html", "w", encoding="utf-8") as f:
    f.write(driver.page_source)

print("✅ Saved course content HTML to 'tds_course_dump.html'")
driver.quit()
