import pandas as pd
import faiss
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

df = pd.read_csv("data/patents.csv")

texts = df["abstract"].tolist()

embeddings = model.encode(texts)

dimension = embeddings.shape[1]

index = faiss.IndexFlatL2(dimension)

index.add(embeddings)

def search_patents(query, k=3):
    query_embedding = model.encode([query])

    distances, indices = index.search(query_embedding, k)

    results = []

    for i, idx in enumerate(indices[0]):
        results.append({
            "title": df.iloc[idx]["title"],
            "abstract": df.iloc[idx]["abstract"],
            "distance": float(distances[0][i])
        })

    return results