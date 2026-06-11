import os
import requests
from dotenv import load_dotenv

load_dotenv()

LENS_API_KEY = os.getenv("LENS_API_KEY")

print("LENS KEY FOUND:", LENS_API_KEY is not None)
print("LENS KEY LENGTH:", len(LENS_API_KEY) if LENS_API_KEY else 0)


def fetch_patents(query):

    url = "https://api.lens.org/patent/search"

    headers = {
        "Authorization": LENS_API_KEY,
        "Content-Type": "application/json"
    }

    payload = {
        "query": {
            "match": {
                "abstract": query
            }
        },
        "size": 20
    }

    response = requests.post(
        url,
        headers=headers,
        json=payload
    )

    print("Status Code:", response.status_code)
    print(response.text)

    if response.status_code != 200:
        return []

    data = response.json()

    patents = []

    for patent in data.get("data", []):

        title = (
            patent.get("biblio", {})
            .get("invention_title", "No Title")
        )

        abstract = patent.get("abstract", "No Abstract")

        patents.append({
            "title": title,
            "abstract": abstract
        })

    return patents