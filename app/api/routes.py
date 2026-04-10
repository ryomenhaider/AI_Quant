import httpx
from fastapi import APIRouter, HTTPException, Depends
from app.models.schemas import ChatRequest, ChatResponse, ErrorResponse
from app.services.llm import LLMService


router = APIRouter()


def get_llm_service() -> LLMService:
    return LLMService()


@router.post(
    "/chat",
    response_model=ChatResponse,
    responses={
        500: {"model": ErrorResponse},
        502: {"model": ErrorResponse},
    },
)
async def chat(
    request: ChatRequest, llm_service: LLMService = Depends(get_llm_service)
):
    try:
        response = await llm_service.chat(request.message)
        return ChatResponse(response=response)
    except httpx.TimeoutException:
        raise HTTPException(status_code=504, detail="Request to LLM timed out")
    except httpx.HTTPStatusError as e:
        raise HTTPException(
            status_code=502, detail=f"LLM API error: {e.response.status_code}"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
