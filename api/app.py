import uuid

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from route.auth import router as auth_router
from route.message import router as message_router
from route.research import router as research_router
from route.thread import router as thread_router
from route.s3 import router as s3_router
from route.file import router as file_router

from researcher.checkpoint import BaseCheckpointManager
from researcher.graph.researcher import Researcher
from researcher.utils.database import close_db_pool, get_db_connection_str, init_db_pool

load_dotenv()

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import TypedDict

from langgraph.graph import StateGraph


class State(TypedDict):
    graph: StateGraph


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[State]:
    """
    Lifespan for the FastAPI app.
    """

    # Initialize the database connection pool
    await init_db_pool()

    # Initialize a Researcher instance
    checkpoint_manager = BaseCheckpointManager(
        checkpoint_type="postgres", conn_string=get_db_connection_str()
    )
    researcher = await Researcher.create_researcher(
        checkpoint_manager=checkpoint_manager,
    )

    # Compile the graph with the checkpointer
    async with researcher.checkpointer.get_checkpointer() as checkpointer:
        graph = researcher.graph.compile(checkpointer=checkpointer)

        # Generate a visualization of the graph
        graph.get_graph().draw_mermaid_png(output_file_path="docs/researcher_graph.png")
        yield {"graph": graph}

    # Close the database connection pool on shutdown
    await close_db_pool()


app = FastAPI(lifespan=lifespan)

# Set up CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000", "https://researcher.insightial.com"],
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

app.include_router(research_router)
app.include_router(auth_router)
app.include_router(message_router)
app.include_router(thread_router)
app.include_router(s3_router)
app.include_router(file_router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
