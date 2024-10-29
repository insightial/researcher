import os
from typing import Any
from langchain_openai import OpenAIEmbeddings

_SUPPORTED_PROVIDERS = {
    "openai",
}


class Embeddings:
    def __init__(
        self,
        embedding_provider: str,
        model: str = "text-embedding-3-small",
        **embdding_kwargs: Any,
    ):
        _embeddings = None
        match embedding_provider:
            case "openai":
                _embeddings = OpenAIEmbeddings(model=model, **embdding_kwargs)

            case _:
                raise Exception(
                    f"Embedding not found. Supported providers: {_SUPPORTED_PROVIDERS}"
                )

        self._embeddings = _embeddings

    def get_embeddings(self):
        return self._embeddings
