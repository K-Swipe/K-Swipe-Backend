from sqlalchemy import Column, ForeignKey, Integer, Boolean
from sqlalchemy.orm import relationship

from entities.base import Base


class Popularity(Base):
    __tablename__ = "popularity"

    id = Column(Integer, primary_key=True, index=True)  # 고유 ID
    spot_id = Column(Integer, ForeignKey("busan_tour_info.id"), primary_key=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), primary_key=True)

    def __init__(self, spot_id: int, user_id: int):
        self.spot_id = spot_id
        self.user_id = user_id

    def __repr__(self):
        return f"Popularity: {self.spot_id}, User: {self.user_id}"
