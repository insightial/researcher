from typing import List, Optional

from langgraph.graph import MessagesState


class GraphState(MessagesState):
    question: str
    search_results: Optional[str]
    response: Optional[str]
    chat_history: Optional[List[str]] = []
