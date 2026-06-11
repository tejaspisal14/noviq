import requests
import re

def search_google_patents(query):

    search_url = (
        f"https://patents.google.com/?q={query.replace(' ', '+')}"
    )

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(
        search_url,
        headers=headers
    )

    print("STATUS:", response.status_code)

    matches = re.findall(
        r'publicationNumber":"(.*?)"',
        response.text
    )

    print("FOUND:", len(matches))

    print(matches[:20])