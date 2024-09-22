import joblib
import pandas as pd
from repository.spotRepository import SpotRepository
from schema.request import RecommendationRequest
from schema.response import SpotListSchema

from model.recommend import prediction
from model.Recommended.config import cfg


class AIService:
    def __init__(self):
        self.model = self._load_model(cfg.model_path)
        self.info = pd.read_csv(cfg.information_path)
        self.busan_spot_info = pd.read_csv(cfg.spot_info)
        self.recommneded_place = None

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
        self.recommneded_place = recommneded_place
        print(self.recommneded_place)

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
        travelPlan={"place": ["부산+기장군", "부산+중구"], "howmany": "", "style": "", "reason": "", "thema": ""},
        travelProfile={"age": "", "gender": "", "people": "", "traffic": ""},
    )
    # print(request.travelPlan['howmany'])
    app.get_recommendation(request)
