from contextlib import asynccontextmanager

from langgraph.checkpoint.memory import MemorySaver
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
from psycopg_pool import AsyncConnectionPool


class BaseCheckpointManager:
    def __init__(self, checkpoint_type: str = None, **kwargs):
        """
        Initialize the BaseCheckpointerManager with the necessary parameters.

        :param checkpoint_type: Type of Checkpoint (default is "MemorySaver").
                            Supported types are:
                                - "postgres": PostgreSQL-backed checkpoint.
        """
        self.checkpoint_type = checkpoint_type
        self.conn_string = kwargs.get("conn_string")

    @asynccontextmanager
    async def get_checkpointer(self):
        """
        Asynchronously yield a checkpointer (memory saver) instance.

        This method creates a new instance of the memory saver each time it's called,
        ensuring a fresh connection to the database.

        Yields:
            An instance of AsyncPostgresSaver or MemorySaver.
        """
        if self.checkpoint_type == "postgres":
            async with AsyncConnectionPool(
                conninfo=self.conn_string,
                max_size=20,
            ) as pool, pool.connection() as conn:
                checkpointer = AsyncPostgresSaver(conn)
                yield checkpointer
        else:
            # For MemorySaver, use it directly as a synchronous context manager
            with MemorySaver() as checkpointer:
                yield checkpointer
