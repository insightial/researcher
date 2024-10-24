from typing import Any

from langchain.chains import ConversationChain
from langchain_community.chat_models import ChatOpenAI
from langchain_core.memory import BaseMemory


class LLMProvider:
    """
    LLM provider
    """

    def __init__(self, llm, memory: BaseMemory = None):
        self.llm = llm
        self.memory = memory
        if memory:
            self.chain = ConversationChain(llm=llm, memory=memory, verbose=True)

    @classmethod
    def create_provider(cls, provider: str, memory: BaseMemory = None, **kwargs: Any):
        """
        Create an LLM provider
        """
        if provider == "openai":
            llm = ChatOpenAI(**kwargs)
            return cls(llm, memory)
        raise ValueError(f"Unknown LLM provider: {provider}")

    async def agenerate(self, prompt: str) -> str:
        """
        Generate a response asynchronously
        """
        if self.memory:
            response = await self.chain.arun(prompt)
        else:
            response = await self.llm.agenerate([prompt])
            response = response.generations[0][0].text
        return response
