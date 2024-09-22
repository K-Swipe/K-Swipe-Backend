from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, func
from sqlalchemy.orm import relationship


from entities.base import Base


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String(256), nullable=True)
    password = Column(String(256), nullable=True)
    email = Column(String(256), nullable=False, unique=True)  # 중복방지
    social = Column(String(256), nullable=True)
    is_deleted = Column(Boolean, default=False)
    registered_at = Column(DateTime, default=func.now())  # 사용자가 생성될 때 현재 시간으로 설정
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())  # 수정 시 현재 시간으로 업데이트

    def __repr__(self):
        return f"User: {self.user_id}, {self.username}, {self.password} , {self.email}, {self.social}"

    @classmethod
    def create(cls, username: str, hashed_password: str, email: str) -> "User":
        return cls(username=username, password=hashed_password, email=email)
