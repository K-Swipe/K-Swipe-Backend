import os

from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_SECRET_KEY = os.getenv("GOOGLE_SECRET_KEY")
GOOGLE_CALLBACK_URI = "https://balpyo.site/google/callback"

KAKAO_CLIENT_ID = os.getenv("KAKAO_CLIENT_ID")
KAKAO_SECRET_KEY = os.getenv("KAKAO_SECRET_KEY")
KAKAO_CALLBACK_URI = "https://balpyo.site/kakao/callback"

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
SEARCH_URL = "https://www.googleapis.com/youtube/v3/search"
