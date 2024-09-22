from fastapi import Depends
from schema.response import PhotoListResponse, PhotoResponse, SpotListSchema, SpotSchema
from entities.spot import Spot
from repository.spotRepository import SpotRepository


class SpotService:

    def __init__(self, spotRepository: SpotRepository = Depends()):
        self.spotRepository = spotRepository

    def get_spot(self, spot_id: int) -> Spot:
        spot: Spot | None = self.spotRepository.get_spot_one(spot_id)

        return SpotSchema.from_orm(spot)

    def get_spot_list(self) -> SpotListSchema:
        spot_list: list[Spot] = self.spotRepository.get_spot_list()

        return SpotListSchema(spots=[SpotSchema.from_orm(spot) for spot in spot_list])

    def get_spot_photo_list(self) -> PhotoListResponse:
        spot_list: list[Spot] = self.spotRepository.get_spot_list()

        return PhotoListResponse(spots=[PhotoResponse.from_orm(spot) for spot in spot_list])
