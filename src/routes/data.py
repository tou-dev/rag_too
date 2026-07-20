from fastapi import FastAPI,APIRouter,Depends,UploadFile,status
from fastapi.responses import JSONResponse
from models import ResponseSignal
from helpers.config import get_settings,Settings
from controllers import DataController,ProjectController
import os, aiofiles
data_router=APIRouter(
    prefix="/api/v1/data",
    tags=["api_v1","data"],

)

@data_router.post("/upload/{project_id}")
async def upload_data(
        project_id:str,file:UploadFile,
        app_settings:Settings=Depends(get_settings)):

    
        project_dir_path=ProjectController().get_project_path(project_id=project_id)
        file_path=os.path.join(project_dir_path,file.filename)
        
        async with aiofiles.open(file_path,"wb") as f:
            while chunk:= await file.read(app_settings.FILE_PARTIE_SIZE):
                await f.write(chunk)

        return JSONResponse(
             status_code=status.HTTP_200_OK,
             content= {
                "signal":ResponseSignal.FILE_UPLOAD_SUCCESS.value
            })  
        