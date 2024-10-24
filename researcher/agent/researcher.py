from langchain.memory import ConversationBufferMemory
from llm.provider import LLMProvider
from memory import BaseMemoryManager
from retriever.tavily import TavilyRetriever


class Researcher:
    def __init__(self, **kwargs):
        memory_manager = kwargs.pop("memory_manager", None)
        if memory_manager is None:
            memory_manager = BaseMemoryManager()

        self.memory = memory_manager.get_memory()

        # Remove 'memory' from kwargs to avoid passing it twice
        llm_kwargs = {k: v for k, v in kwargs.items() if k != "memory"}

        self.llm = LLMProvider.create_provider(
            "openai", model="gpt-3.5-turbo", memory=self.memory, **llm_kwargs
        )

        default_tavily_params = {
            "max_results": 10,
            "search_depth": "advanced",
            "include_images": False,
            "include_answer": False,
        }
        tavily_params = {**default_tavily_params, **kwargs}
        self.retriever = TavilyRetriever(**tavily_params)

    async def research(self, question: str) -> str:
        # Retrieve information from the internet
        search_results = await self.retriever.search(question)

        # Generate a prompt for the LLM
        prompt = f"""
        Search Results:
        {search_results}

        Question: {question}

        Based on the search results, please provide a comprehensive answer to the question.
        """

        # Get the response from the LLM
        response = await self.llm.agenerate(prompt)

        return response

    def get_memory(self):
        return self.memory
