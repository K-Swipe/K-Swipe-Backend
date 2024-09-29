from fastapi import Depends
import joblib
import pandas as pd
from entities.tour import BusanTourInfo
from database.connection import get_db
from services.convert_value import cvt_reason, cvt_style, cvt_thema, cvt_traffic
from repository.spotRepository import SpotRepository
from schema.request import RecommendationRequest
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
