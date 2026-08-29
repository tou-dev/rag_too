import os
from urllib.parse import quote
import httpx
from fastapi import APIRouter, Depends, UploadFile, status, HTTPException
from fastapi.responses import JSONResponse

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
        # 1. Read binary content into memory
        file_bytes = await file.read()

        # 2. Extract and sanitize base URL (strips /rest/v1 and trailing slashes)
        supabase_base_url = app_settings.SUPABASE_URL.split("/rest")[0].rstrip("/")
        
        bucket_name = app_settings.SUPABASE_BUCKET_NAME
        raw_path = f"{project_id}/{file.filename}"
        safe_path = quote(raw_path)
        
        endpoint = f"{supabase_base_url}/storage/v1/object/{bucket_name}/{safe_path}"

        headers = {
            "Authorization": f"Bearer {app_settings.SUPABASE_SERVICE_ROLE_KEY}",
            "apiKey": app_settings.SUPABASE_SERVICE_ROLE_KEY,
            "Content-Type": file.content_type or "application/octet-stream",
            "x-upsert": "true"
        }

        # 3. Direct HTTP POST request to Supabase Storage API
        async with httpx.AsyncClient() as client:
            response = await client.post(endpoint, content=file_bytes, headers=headers)

        # 4. Handle response errors
        if response.status_code not in (200, 201):
            try:
                error_detail = response.json()
            except Exception:
                error_detail = response.text

            raise HTTPException(
                status_code=response.status_code,
                detail=f"Supabase Storage Error ({response.status_code}): {error_detail}"
            )

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "signal": ResponseSignal.FILE_UPLOAD_SUCCESS.value,
                "file_path": raw_path
            }
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Upload Error: {str(e)}"
        )