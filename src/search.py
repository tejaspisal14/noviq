from src.google_patents import search_google_patents
from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

def search_patents(query, k=15):

    patents = search_google_patents(
        query
    )

    if not patents:
        return []

    query_embedding = model.encode(
        [query],
        normalize_embeddings=True
    )[0]

    patent_texts = []

    for patent in patents:

        patent_texts.append(
            f"""
            {patent['title']}
            {patent['abstract']}
            """
        )

    patent_embeddings = model.encode(
        patent_texts,
        normalize_embeddings=True
    )

    ranked_patents = []

    for i, patent in enumerate(patents):

        similarity = float(
            np.dot(
                query_embedding,
                patent_embeddings[i]
            )
        )

        patent["similarity"] = round(
            similarity * 100,
            2
        )

        patent["distance"] = round(
            (1 - similarity) * 100,
            2
        )

        ranked_patents.append(
            patent
        )

    ranked_patents.sort(
        key=lambda x: x["similarity"],
        reverse=True
    )

    return ranked_patents[:k]