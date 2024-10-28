from typing import Any

from langchain_openai import ChatOpenAI

_SUPPORTED_PROVIDERS = ["openai"]


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
            llm = ChatOpenAI(**kwargs)
            return cls(llm)
        raise ValueError(
            f"Unknown LLM provider: {provider} - Supported providers: {"".join(_SUPPORTED_PROVIDERS)}"
        )

    async def agenerate(self, prompt: str) -> str:
        """
        Generate a response asynchronously
        """
        response = await self.llm.agenerate([prompt])
        response = response.generations[0][0].text
        return response
