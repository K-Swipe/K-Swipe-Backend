from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi import status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from schema.oauth.social_schma import PROVIDER_ENUM
from schema.request import SocialLogin

from services.userService import UserService
from repository.userRepository import UserRepository

router = APIRouter(
    prefix="/oauth",
    tags=["users"],
)


@router.post(path="/{social}", description="소셜 로그인 / 회원가입")
async def social_auth(
    social: str,
    reqeust: SocialLogin,
    user_service: UserService = Depends(),
    user_repo: UserRepository = Depends(),
):
    print(f"GET /oauth/{social}")
    print(social)

    # social에 따라 분기처리
    social = PROVIDER_ENUM.from_str(social.lower())
    if not social:
        raise HTTPException(status_code=404)

    try:
        if social == PROVIDER_ENUM.GOOGLE:
            user_data = user_service.auth_google(reqeust.code)
        elif social == PROVIDER_ENUM.KAKAO:
            user_data = user_service.auth_kakao(reqeust.code)

        print(user_data)

        user = user_repo.get_user(user_data.email, social=user_data.social)
        print(user)

        # 존재하는 회원시 로그인처리
        if user:
            print("로그인처리")
            access_token: str = user_service.create_jwt(username=user.username)

            response_body = {
                "message": "oauth login successful",
                "name": user_data.username,
                "email": user_data.email,
                "social": user_data.social,
                "access_token": access_token,
            }
            print(response_body)
            return JSONResponse(status_code=status.HTTP_200_OK, content=response_body)
        else:
            print("회원가입처리")
            # 존재하지 않는 회원시 회원가입처리
            user_repo.save_user(user_data)
            response_body = {
                "message": "oauth register successful",
                "username": user_data.username,
                "email": user_data.email,
                "social": user_data.social,
            }
            print(response_body)
            return JSONResponse(status_code=status.HTTP_200_OK, content=response_body)

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
