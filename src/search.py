from src.google_patents import search_google_patents
from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

def search_patents(query, k=10):

    patents = search_google_patents(query)

    if len(patents) == 0:
        return []

    query_embedding = model.encode(
        [query]
    )[0]

    patent_texts = []

    for patent in patents:

        patent_texts.append(
            patent["title"] + " " +
            patent["abstract"]
        )

    patent_embeddings = model.encode(
        patent_texts
    )

    results = []

    for i, patent in enumerate(patents):

        similarity = np.dot(
            query_embedding,
            patent_embeddings[i]
        ) / (
            np.linalg.norm(query_embedding)
            *
            np.linalg.norm(
                patent_embeddings[i]
            )
        )

        patent["distance"] = (
            1 - similarity
        ) * 100

        results.append(patent)

    results.sort(
        key=lambda x: x["distance"]
    )

    return results[:k]