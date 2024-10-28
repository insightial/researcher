import logging

from fastapi import APIRouter, Depends, HTTPException

from researcher.utils.message import get_messages_by_session_id
from researcher.utils.thread import get_threads_for_user_from_db

from .auth import get_current_user

# Set up a simple logger for console output during development
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/messages/thread/")
async def get_messages_by_thread_id(
    thread_id: str, current_user: dict = Depends(get_current_user)
):
    """
    Endpoint to get messages by a thread id
    """

    # Check if the thread belongs to the current user
    threads = await get_threads_for_user_from_db(current_user["username"])
    if not any(thread["id"] == thread_id for thread in threads):
        raise HTTPException(status_code=404, detail="Thread not found")

    messages = await get_messages_by_session_id(thread_id)
    if not messages:
        return {"messages": []}
    return {"messages": messages}
