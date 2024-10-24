import logging
import uuid

from agent.researcher import Researcher
from fastapi import APIRouter, Depends, HTTPException
from langchain.memory import ConversationBufferMemory
from pydantic import BaseModel

from .auth import get_current_user

# Set up a simple logger for console output during development
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

router = APIRouter()

# In-memory storage for threads (replace with database in production)
threads = {}


class Query(BaseModel):
    question: str


class ChatRequest(BaseModel):
    prompt: str
    thread_id: str


@router.post("/create_thread")
async def create_thread(current_user: dict = Depends(get_current_user)):
    thread_id = str(uuid.uuid4())
    memory = ConversationBufferMemory(return_messages=True)
    researcher = Researcher(memory=memory)
    threads[thread_id] = {
        "user": current_user["username"],
        "researcher": researcher,
    }
    return {"thread_id": thread_id}


@router.get("/get_threads")
async def get_threads(current_user: dict = Depends(get_current_user)):
    user_threads = [
        {"id": thread_id, "user": thread["user"]}
        for thread_id, thread in threads.items()
        if thread["user"] == current_user["username"]
    ]
    return {"threads": user_threads}


@router.post("/chat")
async def chat(request: ChatRequest, current_user: dict = Depends(get_current_user)):
    if (
        request.thread_id not in threads
        or threads[request.thread_id]["user"] != current_user["username"]
    ):
        raise HTTPException(status_code=404, detail="Thread not found")

    thread = threads[request.thread_id]
    researcher = thread["researcher"]
    response = await researcher.research(request.prompt)
    return {"response": response}


@router.post("/clear_thread")
async def clear_thread(thread_id: str, current_user: dict = Depends(get_current_user)):
    if (
        thread_id not in threads
        or threads[thread_id]["user"] != current_user["username"]
    ):
        raise HTTPException(status_code=404, detail="Thread not found")

    threads[thread_id]["researcher"].memory.clear()
    return {"message": "Thread history cleared"}


@router.get("/check_auth")
async def check_auth(_: dict = Depends(get_current_user)):
    """
    Function to check if the user is authenticated
    """
    return {"authenticated": True}


@router.get("/get_messages_by_thread_id/{thread_id}")
async def get_messages_by_thread_id(
    thread_id: str, current_user: dict = Depends(get_current_user)
):
    """
    Endpoint to get messages by a thread id
    """
    if (
        thread_id not in threads
        or threads[thread_id]["user"] != current_user["username"]
    ):
        raise HTTPException(status_code=404, detail="Thread not found")

    thread = threads[thread_id]
    messages = await thread["researcher"].get_memory().abuffer_as_messages()
    return {"messages": messages}
