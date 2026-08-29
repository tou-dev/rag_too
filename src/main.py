import os
from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.responses import FileResponse
from routes import base, data, vercel

app = FastAPI()

FAVICON_PATH = os.path.join(os.path.dirname(__file__), "assets", "favicon.ico")

@app.get('/favicon.ico', include_in_schema=False)
async def favicon():
    return FileResponse(FAVICON_PATH)

app.include_router(base.base_router)
app.include_router(data.data_router)
app.include_router(vercel.vercel_router)