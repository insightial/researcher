from langchain_openai import ChatOpenAI
from typing import Any


class LLMProvider:
    """
    LLM provider
    """

    def __init__(self, llm):
        self.llm = llm

    @classmethod
    def create_provider(cls, provider: str, **kwargs: Any):
        """
        Create an LLM provider
        """
        if provider == "openai":
            return cls(ChatOpenAI(**kwargs))
        else:
            raise ValueError(f"Unknown LLM provider: {provider}")

    async def agenerate(self, prompt: str) -> str:
        """
        Generate a response asynchronously
        """
        response = await self.llm.agenerate([prompt])
        return response.generations[0][0].text
