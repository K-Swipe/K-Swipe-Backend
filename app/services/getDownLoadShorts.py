import os
from googleapiclient.discovery import build
from pytube import YouTube


def download_short(short_id, api_key):
    # Authenticate with YouTube Data API using API key
    youtube = build("youtube", "v3", developerKey=api_key)

    # Construct the video URL from the short ID
    video_url = f"https://www.youtube.com/shorts/{short_id}"

    try:
        # Download the video
        print(f"Downloading {short_id}")
        yt = YouTube(video_url)
        yt.streams.filter(adaptive=True, file_extension="mp4").first().download()
        print(f"Successfully downloaded {short_id}")
    except Exception as e:
        print(f"Error downloading {short_id}: {e}")


if __name__ == "__main__":
    short_id = "F9nuCjA-cxU"  # 여기에 YouTube Shorts ID를 입력하세요
    api_key = "AIzaSyDkHc0pGs-LTt6KTrrQToL1wGbAPsx-77U"  # 여기에 생성한 API 키를 입력하세요
    download_short(short_id, api_key)
