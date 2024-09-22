from typing import List
from pydantic import ConfigDict, BaseModel


class UserSchema(BaseModel):
    user_id: int
    username: str
    email: str

    class Config:
        orm_mode = True


class JWTResponse(BaseModel):
    access_token: str


class SpotSchema(BaseModel):
    id: int
    name: str
    gugun: str
    lat: float
    lng: float
    trav_nm: str
    title: str
    subtitle: str
    addr1: str
    homepage_u: str
    trfc_info: str
    usage_day: str
    hldy_info: str
    usage_time: str
    usage_amou: str
    middle_siz: str
    main_img_n: str
    main_img_t: str
    itemcntnts: str
    kakao_rating: int
    total_likes: int

    class Config:
        orm_mode = True


class SpotListSchema(BaseModel):
    spots: list[SpotSchema]

    class Config:
        orm_mode = True


class SpotReponse(BaseModel):
    id: int
    placeImages: str
    placeName: str
    amountLiked: int
    placeTitle: str
    placeSubtitle: str
    placeDescription: str
    kakaoMapRating: float
    placewebsite: str
    closedDays: str
    disabilitySupport: str
    openratingHours: str
    transportationInfo: str

    class Config:
        orm_mode = True


class SpotListResponse(BaseModel):
    spots: list[SpotReponse]

    class Config:
        orm_mode = True


class RecommendationResponse(BaseModel):
    ai_course: List[object]

    class Config:
        orm_mode = True


class ShortResponse(BaseModel):
    videoUrl: str
    title: str
    description: str
    channelTitle: str


class PhotoResponse(BaseModel):
    id: int
    main_img_n: str
    name: str
    title: str
    subtitle: str
    addr1: str
    kakao_rating: float

    class Config:
        orm_mode = True


class PhotoListResponse(BaseModel):
    spots: list[PhotoResponse]

    class Config:
        orm_mode = True
