from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def search_google_patents(query):

    options = Options()

    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(
        service=Service(
            ChromeDriverManager().install()
        ),
        options=options
    )

    patents = []

    try:

        url = (
            "https://patents.google.com/?q="
            + query.replace(" ", "+")
        )

        driver.get(url)

        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located(
                (
                    By.CSS_SELECTOR,
                    "search-result-item"
                )
            )
        )

        results = driver.find_elements(
            By.CSS_SELECTOR,
            "search-result-item"
        )

        for result in results[:10]:

            try:
                title = result.find_element(
                    By.CSS_SELECTOR,
                    "h3"
                ).text.strip()

            except:
                title = "Unknown Patent"

            try:
                abstract = result.text.strip()

            except:
                abstract = ""

            patents.append(
                {
                    "title": title,
                    "abstract": abstract,
                    "distance": 0
                }
            )

    except Exception as e:

        print(
            f"Google Patents Error: {e}"
        )

    finally:

        driver.quit()

    return patents