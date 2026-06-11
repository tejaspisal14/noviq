from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time


def search_google_patents(query):

    driver = webdriver.Chrome(
        service=Service(
            ChromeDriverManager().install()
        )
    )

    url = (
        "https://patents.google.com/?q="
        + query.replace(" ", "+")
    )

    driver.get(url)

    time.sleep(5)

    patents = []

    results = driver.find_elements(
        By.CSS_SELECTOR,
        "search-result-item"
    )

    for result in results[:10]:

        try:

            title = result.find_element(
                By.CSS_SELECTOR,
                "h3"
            ).text

        except:
            title = "Unknown"

        try:

            abstract = result.text

        except:
            abstract = ""

        patents.append(
            {
                "title": title,
                "abstract": abstract[:1000],
                "distance": 0
            }
        )

    driver.quit()

    return patents