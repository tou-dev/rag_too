import os
from fastapi import APIRouter, Depends, UploadFile, status, HTTPException
from fastapi.responses import JSONResponse
from supabase import create_client, Client

from models import ResponseSignal
from helpers.config import get_settings, Settings

data_router = APIRouter(
    prefix="/api/v1/data",
    tags=["api_v1", "data"],
)

@data_router.post("/upload/{project_id}")
async def upload_data(
    project_id: str,
    file: UploadFile,
    app_settings: Settings = Depends(get_settings)
):
    try:
        # 1. Read file bytes into memory
        file_bytes = await file.read()

        # 2. Initialize Supabase Client
        supabase: Client = create_client(
            app_settings.SUPABASE_URL,
            app_settings.SUPABASE_SERVICE_ROLE_KEY
        )

        # 3. Create scoped path in bucket: <project_id>/<filename>
        storage_path = f"{project_id}/{file.filename}"

        # 4. Upload in-memory bytes to Supabase Storage
        supabase.storage.from_(app_settings.SUPABASE_BUCKET_NAME).upload(
            path=storage_path,
            file=file_bytes,
            file_options={
                "content-type": file.content_type or "application/octet-stream",
                "upsert": "true"
            }
        )

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "signal": ResponseSignal.FILE_UPLOAD_SUCCESS.value,
                "file_path": storage_path
            }
        )
    except Exception as e:
        # Extract meaningful message from dictionary or exception objects
        if isinstance(e, dict):
            error_detail = e.get("message") or e.get("error") or str(e)
        elif hasattr(e, "message"):
            error_detail = e.message
        else:
            error_detail = str(e)

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Supabase Upload Failed: {error_detail}"
        )