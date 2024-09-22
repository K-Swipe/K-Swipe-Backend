from typing import List
from fastapi import APIRouter, Depends, HTTPException
import requests

from services.spotSerivce import SpotService
from schema.response import PhotoResponse, ShortResponse
from utils.config import SEARCH_URL, YOUTUBE_API_KEY


router = APIRouter(
    prefix="/card",
    tags=["card"],
)


@router.get("/shorts", status_code=200)
def get_shorts_videos_handler() -> list[ShortResponse]:

    params = {
        "part": "snippet",
        "q": "shorts 부산관광지 #shorts #부산관광지",  # 검색어
        "type": "video",
        "videoDuration": "short",  # Short 비디오만 필터링
        "key": YOUTUBE_API_KEY,
        "maxResults": 10,  # 최대 결과 수
    }

    response = requests.get(SEARCH_URL, params=params)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Error fetching data from YouTube API")

    data = response.json()

    shortsList = []

    video_id = data.get("items", [])[0]["id"]["videoId"]

    for item in data.get("items", []):
        response: ShortResponse = ShortResponse(
            videoUrl=f"https://www.youtube.com/watch?v={video_id}",
            title=item["snippet"]["title"],
            description=item["snippet"]["description"],
            channelTitle=item["snippet"]["channelTitle"],
        )

        shortsList.append(response)

    return shortsList


@router.get("/photos", response_model=list)
def get_photo_card_handler(spot_service: SpotService = Depends()) -> List[PhotoResponse]:

    spot_photo_list = spot_service.get_spot_photo_list()

    try:

        response: List[PhotoResponse] = [
            PhotoResponse(
                spotId=spot.id,
                spotImage=spot.main_img_n,
                spotName=spot.name,
                spotTitle=spot.title,
                spotSubtitle=spot.subtitle,
                address=spot.addr1,
                kakaoMapRating=spot.kakao_rating,
            )
            for spot in spot_photo_list
        ]

        print(response)

        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")
