from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI
from routes import base,data,vercel


app=FastAPI()
app.include_router(base.base_router)
app.include_router(data.data_router)
app.include_router(vercel.vercel_router)





