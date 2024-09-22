from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from entities.base import Base


class Popularity(Base):
    __tablename__ = "popularity"

    id = Column(Integer, primary_key=True, index=True)  # 고유 ID
    spot_id = Column(Integer, ForeignKey("busan_gis.id"), nullable=False)
    user_id = Column(Integer, nullable=False)

    def __init__(self, spot_id: int, user_id: int, popularity: int):
        self.spot_id = spot_id
        self.user_id = user_id
        self.popularity = popularity

    def __repr__(self):
        return f"Popularity: {self.spot_id}, User: {self.user_id}, {self.popularity}"
