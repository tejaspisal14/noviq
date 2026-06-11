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

links = driver.find_elements(
    By.TAG_NAME,
    "a"
)

for link in links[:100]:

    text = link.text.strip()

    href = link.get_attribute("href")

    if len(text) > 20:

        print("\nTITLE:")
        print(text)

        print("URL:")
        print(href)

driver.quit()