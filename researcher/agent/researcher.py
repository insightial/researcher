from langchain.memory import ConversationBufferMemory
from llm.provider import LLMProvider
from retriever.tavily import TavilyRetriever


class Researcher:
    def __init__(self, **kwargs):
        memory = kwargs.pop("memory", None)
        if memory is None:
            memory = ConversationBufferMemory(return_messages=True)

        self.memory = memory
        self.llm = LLMProvider.create_provider(
            "openai", model="gpt-3.5-turbo", memory=memory, **kwargs
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
