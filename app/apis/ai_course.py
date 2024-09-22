from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse

from schema.request import RecommendationRequest
from schema.response import RecommendationResponse
from services.aiService import AIService

router = APIRouter(prefix="/ai", tags=["ai"])


@router.post("/course", description="AI 추천 코스 생성", status_code=200)
def generate_ai_course(request: RecommendationRequest, ai_service: AIService = Depends()):

    generate_course: RecommendationResponse = ai_service.get_recommendation(request)

    try:
        return generate_course

    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")
