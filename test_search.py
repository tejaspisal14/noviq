# test_search.py

from src.search import search_patents

results = search_patents(
    "AI animal detection highway system"
)

for patent in results[:5]:

    print("\nTITLE:")
    print(patent["title"])

    print("\nDISTANCE:")
    print(patent["distance"])

    print("-" * 50)