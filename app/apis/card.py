from fastapi import APIRouter, HTTPException
import requests

from utils.config import SEARCH_URL, YOUTUBE_API_KEY


router = APIRouter(
    prefix="/card",
    tags=["card"],
)


@router.get("/shorts", response_model=list)
def get_shorts_videos(keyword: str = "부산 관광지"):

    params = {
        "part": "snippet",
        "q": keyword,
        "type": "video",
        "videoDuration": "short",  # Short 비디오만 필터링
        "key": YOUTUBE_API_KEY,
        "maxResults": 10,  # 최대 결과 수
    }

    response = requests.get(SEARCH_URL, params=params)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Error fetching data from YouTube API")

    data = response.json()
    video_urls = []

    for item in data.get("items", []):
        video_id = item["id"]["videoId"]
        video_description = item["snippet"]["description"]
        video_title = item["snippet"]["title"]
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        video_urls.append(video_url)

    return video_urls
