from pydantic import BaseModel, Field


class SignUpRequest(BaseModel):
    username: str
    password: str
    email: str


class LoginRequest(BaseModel):
    username: str
    password: str


class SocialLogin(BaseModel):
    code: str


class SpotRequest(BaseModel):
    spot_id: int


from typing import List, Dict


class TravelPlan(BaseModel):
    place: List[str] = Field(None, description="여행지", example=["부산+기장군", "부산+중구"])
    howmany: int | str = Field(None, description="여행 일수", example=2)
    style: str = Field(None, description="여행 스타일", example="city")
    reason: int | str = Field(None, description="여행 목적", example=3)
    thema: str = Field(None, description="여행 테마", example="쇼핑하기")


class TravelProfile(BaseModel):
    age: int | str = Field(None, description="나이", example=30)
    gender: str = Field(None, description="성별", example="남")
    people: int | str = Field(None, description="동행 인원", example=4)
    price: List[int] | str = Field(None, description="예산", example=[10000, 20000])
    traffic: str = Field(None, description="이동수단", example="car")


class RecommendationRequest(BaseModel):
    userId: int = Field(..., description="사용자 ID", example=15)
    travelPlan: TravelPlan = Field(None, description="여행 계획")
    travelProfile: TravelProfile = Field(None, description="여행 프로필")


class TumbsupRequest(BaseModel):
    spot_id: int = Field(..., description="관광지 ID", example=1)
    user_id: int = Field(..., description="사용자 ID", example=15)


class TourItem(BaseModel):
    name: str = Field(..., description="관광지 이름", example="스카이라인루지 부산")
    id: int = Field(..., description="관광지 ID", example=47)
    lng: float = Field(..., description="경도", example=129.21884)
    lat: float = Field(..., description="위도", example=35.19473)


class GenerateCourseRequest(BaseModel):
    userId: int = Field(..., description="사용자 ID", example=15)
    tourList: List[TourItem] = Field(
        ...,
        description="관광지 리스트",
        example=[{"name": "스카이라인루지 부산", "id": 47, "lng": 129.21884, "lat": 35.19473}],
    )


class AICouserResponse(BaseModel):
    # userId: int
    tourId: int
    tourList: List[TourItem]
