from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse

from utils.exceptions import NotFoundException
from utils.apiReponse import ApiResponse
from schema.request import GenerateCourseRequest, RecommendationRequest
from schema.response import RecommendationResponse
from services.aiService import AIService

router = APIRouter(prefix="/aiCourse", tags=["aiCourse"])


@router.post("/generate", description="AI 추천 코스 생성", status_code=200)
def generate_ai_course(
    request: RecommendationRequest, ai_service: AIService = Depends()
) -> ApiResponse[RecommendationResponse]:

    generate_course: RecommendationResponse = ai_service.get_recommendation(request)

    response = {
        "generateCourse": generate_course,
    }

    try:
        return ApiResponse(success=True, message="Request was successful.", data=response)

    except Exception as e:
        return ApiResponse(success=False, message=str(e), data=None)


@router.post("/create", description="AI 추천 코스를 생성합니다.", status_code=201)
def update_ai_course_by_user(
    generate_course: GenerateCourseRequest, ai_service: AIService = Depends()
) -> ApiResponse[RecommendationResponse]:

    ai_course: RecommendationResponse = ai_service.add_course_by_user(generate_course)

    response = {"createdAIcourse": {"course_id": ai_course.id, "tour_list": generate_course}}

    try:
        return ApiResponse(success=True, message="Request was successful.", data=response)
    except Exception as e:
        return ApiResponse(success=False, message=str(e), data=None)


@router.get("/", description="AI 추천 코스 상세 조회", status_code=200)
def get_ai_course(course_id: int = 7, ai_service: AIService = Depends()) -> ApiResponse[RecommendationResponse]:

    ai_course: RecommendationResponse = ai_service.get_course(course_id)

    response = {
        "aiCourse": ai_course,
    }

    try:
        return ApiResponse(success=True, message="Request was successful.", data=response)
    except Exception as e:
        return ApiResponse(success=False, message=str(e), data=None)


@router.get("/list/", description="AI 추천 코스 리스트 조회", status_code=200)
def get_ai_course_list_by_user(
    user_id: int = 16, ai_service: AIService = Depends()
) -> ApiResponse[RecommendationResponse]:

    ai_course_list = ai_service.get_course_list_by_user(user_id)

    if not ai_course_list:
        raise HTTPException(status_code=404, detail="AI Course not found")

    response = {
        "userId": user_id,
        "aiCourseList": ai_course_list,
    }

    try:
        return ApiResponse(success=True, message="Request was successful.", data=response)
    except Exception as e:
        return ApiResponse(success=False, message=str(e), data=None)
