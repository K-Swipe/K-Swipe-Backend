from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse

from schema.request import GenerateCourseRequest, RecommendationRequest
from schema.response import RecommendationResponse
from services.aiService import AIService

router = APIRouter(prefix="/aiCourse", tags=["aiCourse"])


@router.post("/generate", description="AI 추천 코스 생성", status_code=200)
def generate_ai_course(request: RecommendationRequest, ai_service: AIService = Depends()):

    generate_course: RecommendationResponse = ai_service.get_recommendation(request)

    request_body = {
        "aiCourse": generate_course,
    }

    try:
        return request_body

    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.post("/create", description="AI 추천 코스를 생성합니다.", status_code=201)
def update_ai_course_by_user(generate_course: GenerateCourseRequest, ai_service: AIService = Depends()):

    ai_course = ai_service.add_course_by_user(generate_course)

    if not ai_course:
        raise HTTPException(status_code=404, detail="AI Course not found")

    created_ai_course = {"course_id": ai_course.id, "tour_list": generate_course}

    response = {
        "status": "save ai course",
        "aiCourse": created_ai_course,
    }

    return response


@router.get("/{course_id}", description="AI 추천 코스 조회", status_code=200)
def get_ai_course(course_id: int, ai_service: AIService = Depends()):

    ai_course: RecommendationResponse = ai_service.get_course(course_id)

    if not ai_course:
        raise HTTPException(status_code=404, detail="AI Course not found")

    response = {
        "aiCourse": ai_course,
    }

    return response


@router.get("/list/{user_id}", description="AI 추천 코스 리스트 조회", status_code=200)
def get_ai_course_list_by_user(user_id: int, ai_service: AIService = Depends()):

    ai_course_list = ai_service.get_course_list_by_user(user_id)

    if not ai_course_list:
        raise HTTPException(status_code=404, detail="AI Course not found")

    response = {
        "userId": user_id,
        "aiCourseList": ai_course_list,
    }

    return response
