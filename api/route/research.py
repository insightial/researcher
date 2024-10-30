import logging
from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel

from researcher.history import BaseChatHistoryManager
from researcher.state import GraphState
from researcher.utils.thread import get_threads_for_user_from_db

from .auth import get_current_user

# Set up a simple logger for console output during development
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

router = APIRouter()


# Define the ChatRequest model to validate incoming chat requests
class ChatRequest(BaseModel):
    prompt: str
    thread_id: str
    files: Optional[List[str]] = []


# The /chat endpoint that accepts a chat request
@router.post("/chat")
async def chat(
    chat_request: ChatRequest,
    request: Request,
    current_user: dict = Depends(get_current_user),
):
    # Fetch threads for the user
    user_threads = await get_threads_for_user_from_db(current_user["username"])
    logger.info("Chat request received: %s", chat_request.model_dump())

    # Verify thread ownership
    if not any(thread["id"] == chat_request.thread_id for thread in user_threads):
        raise HTTPException(status_code=404, detail="Thread not found")

    # Get graph from app state
    graph = request.state.graph

    history = await BaseChatHistoryManager.create_history(
        memory_type="postgres",
        table_name="chat_history",
        session_id=chat_request.thread_id,
    )

    session_history = await history.get_session_history()
    chat_history = [msg.content for msg in session_history]

    # Set up the initial graph state with previous chat history and new question
    graph_state = GraphState(
        question=chat_request.prompt,
        chat_history=chat_history,
        files=chat_request.files,
    )

    await history.add_memory(chat_request.prompt, message_type="human")

    # Process the user's prompt
    response = await graph.ainvoke(
        graph_state,
        config={
            "configurable": {
                "max_iterations": 10,
                "thread_id": chat_request.thread_id,
            }
        },
    )

    await history.add_memory(response["response"], message_type="ai")
    return {"response": response["response"]}
