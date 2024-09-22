from datetime import datetime, timedelta
import random
import time
import bcrypt
from jose import jwt
from schema.oauth.social_schma import SocialMember, PROVIDER_ENUM
import os

import requests

from utils.config import (
    GOOGLE_CLIENT_ID,
    GOOGLE_SECRET_KEY,
    GOOGLE_CALLBACK_URI,
    KAKAO_CLIENT_ID,
    KAKAO_SECRET_KEY,
    KAKAO_CALLBACK_URI,
)


class UserService:
    encoding: str = "utf-8"
    secret_key: str = "3afa21d53830f04a26f81f54b8c06b135042971ff4278d3e1250893a0fada6c6"
    jwt_algorithm: str = "HS256"

    def hash_password(self, plain_password: str) -> str:
        hashed_password: bytes = bcrypt.hashpw(plain_password.encode(self.encoding), salt=bcrypt.gensalt())
        return hashed_password.decode(self.encoding)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        # 추후 디테일한 try-except를 사용하여 예외처리를 추가해야함
        return bcrypt.checkpw(plain_password.encode(self.encoding), hashed_password.encode(self.encoding))

    # openssl rand -hex 32 명령어로 비밀키 생성하는 것을 선행
    def create_jwt(
        self,
        username: str,
    ) -> str:
        return jwt.encode(  # sub: subject, exp: expiration
            {"sub": username, "exp": datetime.now() + timedelta(days=1)},  # username은 추후 고유한 값으로 변경해야함
            self.secret_key,
            algorithm=self.jwt_algorithm,
        )

    def decode_jwt(self, access_token: str) -> str:
        payload: dict = jwt.decode(access_token, self.secret_key, algorithms=self.jwt_algorithm)

        # expire time을 확인하여, 만료된 토큰인지 확인하는 로직 추가 필요
        return payload["sub"]  # username

    def auth_google(self, code: str):
        print("auth_google")
        try:
            # google에 access token 요청
            token_url = f"https://oauth2.googleapis.com/token?client_id={GOOGLE_CLIENT_ID}&client_secret={GOOGLE_SECRET_KEY}&code={code}&grant_type=authorization_code&redirect_uri={GOOGLE_CALLBACK_URI}"
            token_response = requests.post(token_url)
            if token_response.status_code != 200:
                raise Exception

            # google에 회원 정보 요청
            access_token = token_response.json()["access_token"]
            user_info = f"https://www.googleapis.com/oauth2/v1/userinfo?access_token={access_token}"
            user_response = requests.get(user_info)
            if user_response.status_code != 200:
                raise Exception
        except:
            raise Exception("google oauth error")

        info = user_response.json()
        return SocialMember(username=info.get("name"), email=info.get("email"), social=PROVIDER_ENUM.GOOGLE.name)

    def auth_kakao(self, code: str):
        print("auth_kakao")
        try:
            # kakao에 access token 요청
            token_url = f"https://kauth.kakao.com/oauth/token?client_id={KAKAO_CLIENT_ID}&client_secret={KAKAO_SECRET_KEY}&code={code}&grant_type=authorization_code&redirect_uri={KAKAO_CALLBACK_URI}"
            headers = {"Content-type": "application/x-www-form-urlencoded;charset=utf-8"}
            token_response = requests.post(token_url, headers=headers)
            if token_response.status_code != 200:
                raise Exception

            # kakao에 회원 정보 요청
            access_token = token_response.json()["access_token"]
            user_info = f"https://kapi.kakao.com/v2/user/me"
            headers = {
                "Authorization": "Bearer " + access_token,
                "Content-type": "application/x-www-form-urlencoded;charset=utf-8",
            }
            user_response = requests.post(user_info, headers=headers)
            if user_response.status_code != 200:
                raise Exception
        except:
            raise Exception("kakao oauth error")

        info = user_response.json()["kakao_account"]
        name = info.get("name") if info.get("name") else info.get("profile").get("nickname")
        return SocialMember(username=name, email=info.get("email"), social=PROVIDER_ENUM.KAKAO.name)

    @staticmethod  # instance method에 접근할 필요가 없기 때문에, @staticmethod를 사용하여 정적 메소드로 선언(self )
    def create_otp() -> int:
        return random.randint(1000, 9990)  # 1000 ~ 9990 사이의 랜덤한 4자리 숫자 생성

    @staticmethod
    def send_email_to_user(
        email: str,
    ) -> None:

        time.sleep(10)  # 1초 대기
        print(f"Sending email to {email}")  # 이메일 전송 로직
