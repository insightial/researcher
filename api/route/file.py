"""Module for file operations."""

from fastapi import APIRouter, HTTPException
from researcher.utils.database import get_db_connection
from pydantic import BaseModel

router = APIRouter()

class FileMetadata(BaseModel):
    user_id: str
    file_name: str
    s3_location: str

@router.on_event("startup")
async def create_tables():
    """
    Create necessary tables in the database.
    """
    async with get_db_connection() as conn:
        async with conn.cursor() as cursor:
            # Create user_files table if it doesn't exist
            await cursor.execute("""
                CREATE TABLE IF NOT EXISTS user_files (
                    id SERIAL PRIMARY KEY,
                    user_id VARCHAR(255) NOT NULL,
                    file_name VARCHAR(255) NOT NULL,
                    s3_location VARCHAR(255) NOT NULL,
                    deleted BOOLEAN DEFAULT FALSE
                )
            """)

@router.post("/add-file")
async def add_file(file_metadata: FileMetadata):
    """
    Insert file metadata into the database.
    """
    async with get_db_connection() as conn:
        async with conn.cursor() as cursor:
            await cursor.execute(
                "INSERT INTO user_files (user_id, file_name, s3_location) VALUES (%s, %s, %s)",
                (file_metadata.user_id, file_metadata.file_name, file_metadata.s3_location)
            )
    return {"message": "File metadata added successfully"}

@router.delete("/delete-file/{file_id}")
async def delete_file(file_id: int):
    """
    Mark a file as deleted in the database.
    """
    async with get_db_connection() as conn:
        async with conn.cursor() as cursor:
            await cursor.execute(
                "UPDATE user_files SET deleted = TRUE WHERE id = %s",
                (file_id,)
            )
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="File not found")
    return {"message": "File marked as deleted successfully"}
