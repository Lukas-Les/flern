import os

import psycopg

from psycopg import AsyncConnection

DATABASE_URL = os.environ["DATABASE_URL"]

# TODO: implement a connection pool
_connection: AsyncConnection | None = None


async def _create_connection() -> psycopg.AsyncConnection:
    """Create a new async database connection."""
    return await psycopg.AsyncConnection.connect(DATABASE_URL, autocommit=True)


async def create_or_return_connection() -> psycopg.AsyncConnection:
    global _connection
    if _connection is None or _connection.closed:
        _connection = await _create_connection()
    return _connection
