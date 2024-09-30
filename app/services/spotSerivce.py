from fastapi import Depends
from entities.popularity import Popularity
from entities.tour import BusanTourInfo
from entities.popularity import Popularity
from schema.request import TumbsupRequest
from schema.response import PhotoListResponse, PhotoResponse, SpotListSchema, SpotSchema, TumbsupResponse
from entities.spot import Spot
from repository.spotRepository import SpotRepository


class SpotService:

    def __init__(self, spotRepository: SpotRepository = Depends()):
        self.spotRepository = spotRepository

    def get_spot(self, spot_id: int) -> Spot:
        spot: BusanTourInfo | None = self.spotRepository.get_spot_one(spot_id)

        return SpotSchema.from_orm(spot)

    def get_spot_list(self) -> SpotListSchema:
        spot_list: list[BusanTourInfo] = self.spotRepository.get_spot_list()

        return SpotListSchema(spots=[SpotSchema.from_orm(spot) for spot in spot_list])

    def update_popularity(self, thumsupRequest: TumbsupRequest) -> TumbsupResponse:

        popularity: Popularity = self.spotRepository.update_popularity(thumsupRequest)

        return TumbsupResponse.from_orm(popularity)

    def get_total_likes(self, spot_id: int) -> int:
        total_likes: int = self.spotRepository.get_total_likes(spot_id)
        return total_likes
