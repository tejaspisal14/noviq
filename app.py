from src.search import search_patents

query = input("Enter invention idea: ")

results = search_patents(query)

print("\nTop Similar Patents:\n")

for _, row in results.iterrows():
    print(row["title"])