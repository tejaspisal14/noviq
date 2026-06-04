from src.search import search_patents
from src.analyzer import analyze_novelty

query = input("Enter invention idea: ")

results = search_patents(query)

print("\nTop Similar Patents:\n")

for patent in results:
    similarity = max(0, 100 - patent["distance"] * 10)

    print("=" * 50)
    print(f"Title: {patent['title']}")
    print(f"Similarity Score: {similarity:.2f}%")
    print(f"Abstract: {patent['abstract']}")
    print()

print("\nGenerating Noviq Analysis...\n")

analysis = analyze_novelty(query, results)

print("=" * 50)
print("NOVIQ ANALYSIS")
print("=" * 50)
print(analysis)