from sqlalchemy import Column, Integer, BigInteger, String, Numeric
from sqlalchemy.ext.declarative import declarative_base
from geoalchemy2.types import Geometry
from sqlalchemy.orm import relationship

Base = declarative_base()


class Spot(Base):
    __tablename__ = "busan_gis"

    id = Column(Integer, primary_key=True, index=True)
    geom = Column(Geometry(geometry_type="POINT", srid=4326), nullable=True)
    uc_seq = Column(BigInteger, nullable=True)
    name = Column(String(254), nullable=True)
    gugun = Column(String(254), nullable=True)
    lat = Column(Numeric, nullable=True)
    lng = Column(Numeric, nullable=True)
    trav_nm = Column(String(254), nullable=True)
    title = Column(String(254), nullable=True)
    subtitle = Column(String(254), nullable=True)
    addr1 = Column(String(254), nullable=True)
    homepage_u = Column(String(254), nullable=True)
    trfc_info = Column(String(254), nullable=True)
    usage_day = Column(String(254), nullable=True)
    hldy_info = Column(String(254), nullable=True)
    usage_time = Column(String(254), nullable=True)
    usage_amou = Column(String(254), nullable=True)
    middle_siz = Column(String(254), nullable=True)
    main_img_n = Column(String(254), nullable=True)
    main_img_t = Column(String(254), nullable=True)
    itemcntnts = Column(String(254), nullable=True)
    kakao_rating = Column(Integer, nullable=True)
    total_likes = Column(Integer, nullable=True)

    def __repr__(self):
        return f"Spot: {self.id}, {self.name}, {self.gugun}, {self.lat}, {self.lng}, {self.trav_nm}, {self.title}, {self.subtitle}, {self.addr1}, {self.homepage_u}, {self.trfc_info}, {self.usage_day}, {self.hldy_info}, {self.usage_time}, {self.usage_amou}, {self.middle_siz}, {self.main_img_n}, {self.main_img_t}, {self.itemcntnts}, {self.kakao_rating}, {self.total_likes}"
