from typing import Text
from sqlalchemy import Column, ForeignKey, Integer, Float, String, Text
from sqlalchemy.orm import relationship

from entities.base import Base


class AICourse(Base):
    __tablename__ = "ai_course"

    id = Column(Integer, primary_key=True, autoincrement=True)
    tour_list = Column(Text, nullable=False)  # JSON 문자열로 저장
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)

    user_relation = relationship("User", back_populates="courses")  # User와의 관계 설정

    def __repr__(self):
        return f"AICourse: {self.id}, {self.tour_list}"
