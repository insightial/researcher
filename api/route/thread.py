import uuid

from fastapi import APIRouter, Depends, HTTPException

from researcher.utils.thread import (
    delete_thread_from_db,
    get_threads_for_user_from_db,
    save_thread_to_db,
    update_thread_name_in_db,
)

from .auth import get_current_user

router = APIRouter()


@router.post("/thread")
async def create_thread(current_user: dict = Depends(get_current_user)):
    thread_id = str(uuid.uuid4())
    thread_name = "New Chat"
    # Save the thread to the database
    await save_thread_to_db(thread_id, current_user["username"], thread_name)
    return {"thread_id": thread_id}


@router.put("/thread")
async def update_thread_name(
    thread_id: str, name: str, current_user: dict = Depends(get_current_user)
):
    # Check if the thread belongs to the current user
    threads = await get_threads_for_user_from_db(current_user["username"])
    if not any(thread["id"] == thread_id for thread in threads):
        raise HTTPException(status_code=404, detail="Thread not found")

    # Update thread name in the database
    update_thread_name_in_db(thread_id, name)
    return {"message": "Thread name updated"}


@router.get("/threads")
async def get_threads(current_user: dict = Depends(get_current_user)):
    # Fetch the threads from the database
    user_threads = await get_threads_for_user_from_db(current_user["username"])
    return {"threads": user_threads}


@router.delete("/thread")
async def clear_thread(thread_id: str, current_user: dict = Depends(get_current_user)):
    # Check if the thread belongs to the current user
    threads = await get_threads_for_user_from_db(current_user["username"])
    if not any(thread["id"] == thread_id for thread in threads):
        raise HTTPException(status_code=404, detail="Thread not found")

    # Delete the thread from the database
    await delete_thread_from_db(thread_id)
    return {"message": "Thread history cleared"}
