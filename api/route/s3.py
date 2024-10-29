"""Description: This file contains the backend code for handling S3 operations."""

import os
from fastapi import APIRouter, UploadFile, File, HTTPException
import boto3
from .file import add_file, FileMetadata, Depends
from .auth import get_current_user

router = APIRouter()

# Initialize S3 client
s3_client = boto3.client("s3", region_name=os.environ.get("COGNITO_REGION"))
S3_BUCKET = os.environ.get("S3_BUCKET")


@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...), current_user: dict = Depends(get_current_user)
):
    """
    Function to upload a file to S3.
    """
    user_id = current_user["username"]
    try:
        # Upload file to S3
        s3_client.upload_fileobj(
            file.file, S3_BUCKET, f"files/{user_id}/{file.filename}"
        )

        # Prepare metadata for the database
        file_metadata = FileMetadata(
            user_id=user_id,
            file_name=file.filename,
            s3_location=f"s3://{S3_BUCKET}/files/{user_id}/{file.filename}",
        )

        try:
            await add_file(file_metadata)  # Pass the FileMetadata instance
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e)) from e

        return {"message": "File uploaded successfully", "file_name": file.filename}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
