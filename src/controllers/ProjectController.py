from .BaseController import BaseController
import os
class ProjectController(BaseController):
    def __init__(self):
        super().__init__()
        
    

    def get_project_path(self,project_id:str): 
        project_dirs=os.join(self.files_dir,project_id)

        if not os.path.exists(project_dirs):
            os.makedirs(project_dirs)
        
        return project_dirs