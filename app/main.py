from fastapi import FastAPI
from app.api.routes import router as api_router


app = FastAPI(
    title="AI Quant Analyst",
    description="Backend service for AI-powered quant analysis",
    version="0.1.0",
)

app.include_router(api_router, tags=["chat"])


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
