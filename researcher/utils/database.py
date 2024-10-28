"""
Database utilities for the Researcher app.
"""

import logging
import os
from contextlib import asynccontextmanager

from psycopg_pool import AsyncConnectionPool

# Set up a simple logger for console output during development
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Fetch the environment variables for database connection
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")


# Connection pool variable
connection_pool = None


# Get the connection string for the database
def get_db_connection_str():
    """
    Return a connection string for the database.

    The connection string is in the format:
        postgresql://<username>:<password>@<host>:<port>/<database_name>

    Returns:
        str: The connection string.
    """
    conn_string = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    return conn_string


# Initialize the connection pool
async def init_db_pool():
    """
    Initialize the connection pool for the database.

    This function should only be called once at application startup.
    Subsequent calls will have no effect.

    The connection pool is stored in the `connection_pool` global variable.
    """
    global connection_pool
    if connection_pool is None:
        connection_pool = AsyncConnectionPool(conninfo=get_db_connection_str())


# Close the connection pool
async def close_db_pool():
    """
    Close the connection pool.

    This function should be called once at application shutdown to cleanly close
    all connections in the pool.

    The connection pool is stored in the `connection_pool` global variable.
    """
    global connection_pool
    if connection_pool is not None:
        await connection_pool.close()
        connection_pool = None


# Set up a connection to the PostgreSQL database
# Use an async context manager to fetch connections from the pool
@asynccontextmanager
async def get_db_connection():
    """
    Asynchronously yield a connection to the PostgreSQL database.

    This function is an async context manager which yields a connection to the
    database. The connection is fetched from the connection pool and will be
    returned to the pool when the context manager is exited.

    Yields:
        An instance of `AsyncConnectionPool.Connection`.
    """
    async with connection_pool.connection() as connection:
        yield connection
