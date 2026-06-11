from src.patent_fetcher import fetch_patents

patents = fetch_patents(
    "AI animal detection highway system"
)

print("Patents Found:", len(patents))

for patent in patents[:3]:
    print()
    print(patent["title"])