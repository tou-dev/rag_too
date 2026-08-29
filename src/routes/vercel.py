from fastapi import FastAPI,APIRouter

vercel_router=APIRouter()

@vercel_router.get("/health")
async def vercel_health():
    return {
        "running_on_vercel":True,

    }
