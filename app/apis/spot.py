from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse

from entities.popularity import Popularity
from repository.spotRepository import SpotRepository
from schema.request import TumbsupRequest
from schema.response import SpotListResponse, SpotListSchema, SpotReponse, SpotSchema, TumbsupResponse
from entities.spot import Spot
from services.spotSerivce import SpotService


router = APIRouter(prefix="/spots", tags=["spot"])


@router.get("/list", description="spot 리스트 조회", status_code=200, response_model=SpotListResponse)
def get_spot_list(spot_service: SpotService = Depends()) -> SpotListResponse:
    spot_list: SpotListSchema = spot_service.get_spot_list()

    response = SpotListResponse(
        spots=[
            SpotReponse(
                id=spot.id,
                placeImages=spot.main_img_n,
                placeName=spot.name,
                amountLiked=spot.total_likes,
                placeTitle=spot.title,
                placeSubtitle=spot.subtitle,
                placeDescription=spot.itemcntnts,
                kakaoMapRating=spot.kakao_rating,
                placewebsite=spot.homepage_u,
                closedDays=spot.hldy_info,
                disabilitySupport=spot.middle_siz,
                openratingHours=spot.usage_time,
                transportationInfo=spot.trfc_info,
            )
            for spot in spot_list.spots
        ]
    )

    response_body = {
        "spotList": response,
    }

    # try:

    # except Exception as e:
    #     raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/{spot_id}", description="spot_id로 spot 정보 조회", status_code=200, response_model=SpotReponse)
def get_spot_detail(spot_id: int, spot_service: SpotService = Depends()) -> SpotReponse:
    spot: SpotSchema | None = spot_service.get_spot(spot_id)

    if not spot:
        raise HTTPException(status_code=404, detail="spot not found")

    response = SpotReponse(
        id=spot.id,
        placeImages=spot.main_img_n,
        placeName=spot.name,
        amountLiked=spot.total_likes,
        placeTitle=spot.title,
        placeSubtitle=spot.subtitle,
        placeDescription=spot.itemcntnts,
        kakaoMapRating=spot.kakao_rating,
        placewebsite=spot.homepage_u,
        closedDays=spot.hldy_info,
        disabilitySupport=spot.middle_siz,
        openratingHours=spot.usage_time,
        transportationInfo=spot.trfc_info,
    )

    try:
        return response

    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.post("/thumbsup", description="호출 시, 좋아요를 업데이트 ", status_code=200)
def thumbs_up_spot(
    thumsupRequest: TumbsupRequest, spot_service: SpotService = Depends(), spot_repo: SpotRepository = Depends()
) -> JSONResponse:

    popularity: str = spot_repo.update_popularity(thumsupRequest)

    # popularity: TumbsupResponse = TumbsupResponse.from_orm(popularity)

    if not popularity:
        raise HTTPException(status_code=404, detail="spot not found")

    print(popularity)

    if popularity == "deleted":
        response_body = {
            "message": "thumbs up delete successful",
        }

    else:
        response_body = {
            "message": "thumbs up successful",
        }

    return response_body

    try:
        return JSONResponse(status_code=200, content=response_body)

    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")
