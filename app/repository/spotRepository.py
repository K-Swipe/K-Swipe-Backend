from typing import List

from fastapi import Depends
from sqlalchemy import func, select, delete
from sqlalchemy.orm import Session

from entities.popularity import Popularity
from entities.spot import Spot
from database.connection import get_db


class SpotRepository:
    def __init__(self, session: Session = Depends(get_db)):
        self.session = session

    def get_spot_list(self) -> List[Spot]:
        result = self.session.scalars(select(Spot).limit(20)).all()
        return result

    def get_spot_one(self, spot_id: int) -> Spot:
        return self.session.scalars(select(Spot).where(Spot.id == spot_id)).first()

    # 검색어가 포함된 spot_name을 가진 spot을 반환
    def getSpotBySpotName(self, spot_name):
        return self.session.scalars(select(Spot).where(Spot.spot_name.like(f"%{spot_name}%"))).all()

    # 가장 인기 있는 spot을 반환
    def getPopularSpot(self):
        return self.session.scalars(select(Spot).order_by(Spot.popularity.popularity.desc())).first()

    def update_total_likes(self):
        # 서브쿼리를 사용하여 각 spot_id에 대한 좋아요 수를 계산
        subquery = (
            self.session.query(Popularity.spot_id, func.count(Popularity.id).label("like_count"))
            .group_by(Popularity.spot_id)
            .subquery()
        )

        # spot 테이블의 total_likes 업데이트
        self.session.query(Spot).join(subquery, Spot.id == subquery.c.spot_id).update(
            {Spot.total_likes: subquery.c.like_count}, synchronize_session="fetch"  # 세션 동기화
        )
        self.session.commit()
