import json
from fastapi import Depends
import joblib
import pandas as pd
from utils.exceptions import NotFoundException
from entities.aiCourse import AICourse
from entities.tour import BusanTourInfo
from database.connection import get_db
from services.convert_value import cvt_reason, cvt_style, cvt_thema, cvt_traffic
from repository.spotRepository import SpotRepository
from schema.request import AICouserResponse, GenerateCourseRequest, RecommendationRequest, TourItem
from schema.response import SpotListSchema
from sqlalchemy import func, select, delete
from sqlalchemy.orm import Session

from model.recommend import prediction
from model.Recommended.config import cfg


class AIService:
    def __init__(self, session: Session = Depends(get_db)):
        self.model = self._load_model(cfg.model_path)
        self.info = pd.read_csv(cfg.information_path)
        self.busan_spot_info = pd.read_csv(cfg.spot_info)
        self.recommneded_place = None
        self.thema = cvt_thema()
        self.reason_dict = cvt_reason()
        self.style_dict = cvt_style()
        self.traffic = cvt_traffic()
        self.session = session

    def get_recommendation(self, request) -> list:
        place = request.travelPlan.place
        howmany = self.is_blank_array(request.travelPlan.howmany, "TRAVEL_NUM")
        style = self.is_blank_array(request.travelPlan.style, "TRAVEL_STYL")
        reasone = self.is_blank_array(request.travelPlan.reason, "TRAVEL_MOTIVE_1")
        thema = self.is_blank_array(request.travelPlan.thema, "TRAVEL_MISSION_PRIORITY")
        age = self.is_blank_array(request.travelProfile.age, "AGE_GRP")
        gender = self.is_blank_array(request.travelProfile.gender, "GENDER")
        people = self.is_blank_array(request.travelProfile.people, "TRAVEL_COMPANIONS_NUM")
        traffic = self.is_blank_array(request.travelProfile.traffic, "MVMN_NM")

        # Convert thema, reason, style to numeric values
        if thema in self.thema:
            thema = self.thema[thema]

        if reasone in self.reason_dict:
            reasone = self.reason_dict[reasone]

        if style in self.style_dict:
            style = self.style_dict[style]

        if traffic in self.traffic:
            traffic = self.traffic[traffic]

        input_df = pd.DataFrame.from_dict(
            {
                "TRAVEL_MISSION_PRIORITY": thema,
                "MVMN_NM": traffic,
                "GENDER": gender,
                "AGE_GRP": age,
                "TRAVEL_STYL": style,
                "TRAVEL_MOTIVE_1": reasone,
                "TRAVEL_NUM": howmany,
                "TRAVEL_COMPANIONS_NUM": people,
                "sido_gungu_list": place,
            }
        )
        recommneded_place = prediction(self.info, input_df, self.model)

        request_body = []

        for spot in recommneded_place:
            print(spot)
            target = self.session.scalars(select(BusanTourInfo).where(BusanTourInfo.name.like(f"%{spot}%"))).first()
            id = target.id
            lng = target.lng
            lat = target.lat
            request_body.append({"name": spot, "id": id, "lng": lng, "lat": lat})

        return request_body

    def add_course_by_user(self, generate_course: GenerateCourseRequest):
        """AI 추천 코스 저장"""

        # tourList를 JSON 문자열로 변환(ensure_ascii=False: 한글이 유니코드로 출력되지 않도록 설정)
        tour_list_json = json.dumps([item.dict() for item in generate_course.tourList], ensure_ascii=False)

        user = self.session.scalars(select(AICourse).where(AICourse.user_id == generate_course.userId)).first()
        if not user:
            raise NotFoundException("User does not exist")

        ai_course = AICourse(tour_list=tour_list_json, user_id=generate_course.userId)

        self.session.add(ai_course)
        self.session.commit()
        self.session.refresh(ai_course)

        return ai_course

    def get_course(self, course_id: int) -> GenerateCourseRequest:
        """AI 추천 코스 단일 조회"""

        ai_course = self.session.scalars(select(AICourse).where(AICourse.id == course_id)).first()

        if ai_course is None:
            raise NotFoundException("AI Course not found")

        # JSON 문자열을 파싱하여 tourList 생성
        tour_list = json.loads(ai_course.tour_list)

        # GenerateCourseRequest 객체 생성
        generate_course_request = GenerateCourseRequest(
            userId=ai_course.user_id,
            tourList=[TourItem(**item) for item in tour_list],  # TourItem은 tourList의 각 항목을 나타내는 클래스
        )

        return generate_course_request

    def get_course_list_by_user(self, user_id: int) -> list:
        """AI 추천 코스 리스트 조회"""

        ai_course_list = self.session.scalars(select(AICourse).where(AICourse.user_id == user_id)).all()

        # GenerateCourseRequest 객체 리스트 생성
        generate_course_request_list = []
        for ai_course in ai_course_list:
            # JSON 문자열을 파싱하여 tourList 생성
            tour_list = json.loads(ai_course.tour_list)

            generate_course_request = AICouserResponse(
                # userId=ai_course.user_id,
                tourId=ai_course.id,
                tourList=[TourItem(**item) for item in tour_list],  # TourItem은 tourList의 각 항목을 나타내는 클래스
            )

            generate_course_request_list.append(generate_course_request)

        return generate_course_request_list

    def is_blank_array(self, value, column_name):
        if value == "":
            mode_value = self.busan_spot_info[column_name].mode()[0]
            return mode_value
        else:
            return value

    @staticmethod
    def _load_model(model_path):
        model = joblib.load(model_path)
        return model


if __name__ == "__main__":
    app = AIService()
    request = RecommendationRequest(
        userId=1,
        travelPlan={
            "place": ["부산+기장군", "부산+중구"],
            "howmany": "",
            "style": "city",
            "reason": "요즘 너무 바빠 몸과 마음의 재충전이 필요해요",
            "thema": "힐링과 휴식",
        },
        travelProfile={"age": "", "gender": "", "people": "", "traffic": ""},
    )
    # print(request.travelPlan['howmany'])
    app.get_recommendation(request)
