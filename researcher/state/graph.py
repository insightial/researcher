from typing import List, Optional

from langgraph.graph import MessagesState


class GraphState(MessagesState):
    question: str
    search_results: Optional[str] = None
    response: Optional[str] = None
    chat_history: Optional[List[str]] = []
    files: Optional[List[str]] = []
    vector_store_results: Optional[List[str]] = []
