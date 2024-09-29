from pydantic import BaseModel


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
    place: List[str]  # 사용자가 선택한 구역 목록
    howmany: int | str  # 방문 경험 정도(0~4)
    style: str  # 선호하는 여행 스타일 (city or nature)
    reason: int | str  # 여행의 목적 (0~4)
    thema: str  # 선호하는 여행 테마 목록


class TravelProfile(BaseModel):
    age: int | str  # 사용자 연령대 (10, 20, 30, 40)
    gender: str  # 사용자 성별
    people: int | str  # 동행 인원(1~5)
    # price: List[int] | str # 예상 지출 비용 범위 - 입력만 받음
    traffic: str  # 선호하는 교통 수단 (car or bus)


class RecommendationRequest(BaseModel):
    userId: int
    travelPlan: TravelPlan
    travelProfile: TravelProfile
