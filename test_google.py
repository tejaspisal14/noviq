from src.google_patents import search_google_patents

patents = search_google_patents(
    "AI animal detection highway system"
)

for p in patents:

    print("\nTITLE:")
    print(p["title"])

    print("\nABSTRACT:")
    print(p["abstract"][:300])

    print("-" * 50)