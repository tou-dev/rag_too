from .BaseController import BaseController
from fastapi import UploadFile
from models import ResponseSignal

class DataController(BaseController):
    def __init__(self):
        super().__init__()
        self.size_scale=1048576
    
    def validate_uploaded_file(self,file:UploadFile):
        if file.content_type not in self.app_settings.FILE_ALLOWED_TYPES:
            return {
                ResponseSignal.FILE_TYPE_NOT_SUPPORTED.value,
                ResponseSignal.FILE_UPLOAD_FAILED.value
            }
        if file.size > self.app_settings.FILE_MAX_SIZE * self.size_scale:
            return {
                ResponseSignal.FILE_SIZE_EXCEEDED.value,
                ResponseSignal.FILE_UPLOAD_FAILED.value
            }
        
        return ResponseSignal.FILE_UPLOAD_SUCCESS.value
        
        