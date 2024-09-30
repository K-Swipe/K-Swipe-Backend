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
    gungu: str
    lat: float
    lng: float
    title: str
    subtitle: str
    addr1: str
    homepage_u: str
    trfc_info: str
    usage_day: str
    hidy_info: str
    usage_time: str
    usage_amou: str
    middle_siz: str
    main_img_n: str
    main_img_t: str
    itemcntnts: str
    kakao_rating: int

    class Config:
        orm_mode = True


class SpotListSchema(BaseModel):
    spots: List[SpotSchema]

    class Config:
        orm_mode = True


class SpotReponse(BaseModel):
    id: int | None
    placeImages: str | None
    placeName: str | None
    amountLiked: int | None
    placeTitle: str | None
    placeSubtitle: str | None
    placeDescription: str | None
    kakaoMapRating: float | None
    placewebsite: str | None
    closedDays: str | None
    disabilitySupport: str | None
    openratingHours: str | None
    transportationInfo: str | None

    class Config:
        orm_mode = True


class SpotListResponse(BaseModel):
    spots: List[SpotReponse]

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


class ShortListResponse(BaseModel):
    shorts: List[ShortResponse]

    class Config:
        orm_mode = True


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
    spots: List[PhotoResponse]

    class Config:
        orm_mode = True


class TumbsupResponse(BaseModel):
    spot_id: int
    user_id: int

    class Config:
        orm_mode = True
