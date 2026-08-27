from huggingface_hub import InferenceClient

from app.core.config import settings


class EmbeddingService:
    def __init__(self):
        self.client = InferenceClient(
            provider="hf-inference",
            api_key=settings.hf_token,
        )

        self.model = "BAAI/bge-base-en-v1.5"

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        embeddings = self.client.feature_extraction(
            texts,
            model=self.model,
        )

        return embeddings.tolist()

    def embed_query(self, text: str) -> list[float]:
        embedding = self.client.feature_extraction(
            text,
            model=self.model,
        )

        return embedding.tolist()