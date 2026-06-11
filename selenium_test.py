from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time

driver = webdriver.Chrome(
    service=Service(
        ChromeDriverManager().install()
    )
)

driver.get(
    "https://patents.google.com/?q=AI+animal+detection+highway+system"
)

time.sleep(5)

titles = driver.find_elements(
    By.CSS_SELECTOR,
    "h3"
)

print("\nPATENT TITLES FOUND:\n")

for title in titles:
    text = title.text.strip()

    if text:
        print(text)

driver.quit()