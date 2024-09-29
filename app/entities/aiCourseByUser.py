from sqlalchemy import Column, ForeignKey, Integer, Boolean
from sqlalchemy.orm import relationship

from entities.base import Base


class AICourseByUser(Base):
    __tablename__ = "ai_course_by_user"

    id = Column(Integer, primary_key=True, index=True)  # 고유 ID
    course_id = Column(Integer, ForeignKey("course.id"), primary_key=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), primary_key=True)

    def __repr__(self):
        return f"AICourse: {self.course_id}, User: {self.user_id}"
