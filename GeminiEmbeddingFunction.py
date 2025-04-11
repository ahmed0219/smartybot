from chromadb import EmbeddingFunction
from google.generativeai import embed_content

class GeminiEmbeddingFunction(EmbeddingFunction):
    document_mode = True

    def __call__(self, input: list[str]) -> list[list[float]]:
        task = "retrieval_document" if self.document_mode else "retrieval_query"
        embeddings = []

        for text in input:
            try:
                response = embed_content(
                    model="models/embedding-001",
                    content=text,
                    task_type=task,
                )
                embeddings.append(response["embedding"])
            except Exception as e:
                print(f"Error embedding: {e}")
                embeddings.append([0.0] * 768)  # fallback vector

        return embeddings