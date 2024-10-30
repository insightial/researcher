"""Description: This file contains the backend code for handling S3 operations."""

from io import BytesIO

import tempfile
import os
from fastapi import APIRouter, UploadFile, HTTPException, Request, Depends
import boto3

from researcher.embeddings.embeddings import Embeddings
from .file import add_file, FileMetadata, Depends
from .auth import get_current_user
from researcher.document.document import DocumentLoader
from researcher.store.vectorstore import Store
from langchain_community.vectorstores import PGEmbedding

router = APIRouter()

# Initialize S3 client
s3_client = boto3.client("s3", region_name=os.environ.get("COGNITO_REGION"))
S3_BUCKET = os.environ.get("S3_BUCKET")


@router.post("/upload")
async def upload_file(
    file: UploadFile, request: Request, current_user: dict = Depends(get_current_user)
):
    """
    Function to upload a file to S3 and index it in PGEmbedding.
    """
    user_id = current_user["username"]
    file_path = f"files/{user_id}/{file.filename}"
    s3_location = f"s3://{S3_BUCKET}/{file_path}"
    file_extension = file.filename.split(".")[-1].lower()

    try:
        # Step 1: Upload file to S3
        file_content = await file.read()
        s3_client.upload_fileobj(BytesIO(file_content), S3_BUCKET, file_path)

        # Step 2: Add file metadata to the database
        file_metadata = FileMetadata(
            user_id=user_id,
            file_name=file.filename,
            s3_location=s3_location,
        )
        await add_file(file_metadata)

        # Step 3: Write file temporarily to disk
        with tempfile.NamedTemporaryFile(
            delete=False, suffix=f".{file_extension}"
        ) as tmp_file:
            tmp_file.write(file_content)
            tmp_file_path = tmp_file.name

        # Step 4: Load document content for indexing
        loader = DocumentLoader(path=tmp_file_path, source=s3_location)
        documents = await loader.load()

        # Step 4: Get Store from app state
        store = request.state.store

        # Step 5: Index the document content in PGEmbedding
        store.load(documents)

        return {
            "message": "File uploaded and indexed successfully",
            "file_name": file.filename,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
