from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router as api_router


app = FastAPI(
    title="AI Quant Analyst",
    description="Backend service for AI-powered quant analysis",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api", tags=["chat"])


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
