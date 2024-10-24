import os
from typing import Dict, List

from langchain_community.tools import TavilySearchResults


class TavilyRetriever:
    def __init__(self, **kwargs):
        if not os.getenv("TAVILY_API_KEY"):
            raise ValueError("TAVILY_API_KEY environment variable is not set")

        self.search_tool = TavilySearchResults(**kwargs)

    async def search(self, query: str) -> List[Dict[str, str]]:
        try:
            results = await self.search_tool.ainvoke({"query": query})
            return results
        except Exception as e:
            raise Exception(f"Tavily API request failed: {str(e)}")
