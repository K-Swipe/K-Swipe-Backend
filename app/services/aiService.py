from repository.spotRepository import SpotRepository
from schema.response import SpotListSchema
from schema.request import RecommendationRequest

import joblib
import pandas as pd


class AIService:
    def __init__(self):
        self.rm_model = load_recommendation_model()

    def get_recommendation(self, request: RecommendationRequest):
        # 데이터 전처리

        place = request.travelPlan["place"]
        howmany = request.travelPlan["howmany"]
        style = request.travelPlan["style"]
        reasone = request.travelPlan["reason"]
        thema = request.travelPlan["thema"]
        age = request.travelProfile["age"]
        people = request.travelProfile["people"]
        # price = request.travelProfile["price"]
        traffic = request.travelProfile["traffic"]

        input_df = pd.DataFrame.from_dict(place, howmany, style, reasone, thema, age, people, traffic)

        recommend_course = self.rm_model.predict(input_df)

        return recommend_course


def load_recommendation_model():

    rm_model = joblib.load("./model/catboost_model_B.pkl")

    return rm_model
