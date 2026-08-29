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
    # 1. Clean URL formatting
    supabase_url = app_settings.SUPABASE_URL.rstrip("/")
    
    # 2. Initialize Supabase Client
    supabase: Client = create_client(
        supabase_url,
        app_settings.SUPABASE_SERVICE_ROLE_KEY
    )

    bucket_name = app_settings.SUPABASE_BUCKET_NAME

    try:
        # 3. Read file bytes into memory
        file_bytes = await file.read()
        storage_path = f"{project_id}/{file.filename}"

        # 4. Upload to Supabase Storage
        res = supabase.storage.from_(bucket_name).upload(
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
        # Fallback to inspect dictionary-based SDK exceptions
        error_msg = str(e)
        if hasattr(e, "args") and e.args:
            error_msg = str(e.args[0])

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Storage Exception on bucket '{bucket_name}': {error_msg}"
        )