from sqlalchemy import Column, Integer, String, Float

from entities.base import Base


class BusanTourInfo(Base):
    __tablename__ = "busan_tour_info"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=True)
    gungu = Column(String(50), nullable=True)
    lat = Column(Float, nullable=True)
    lng = Column(Float, nullable=True)
    title = Column(String(50), nullable=True)
    subtitle = Column(String(50), nullable=True)
    addr1 = Column(String(50), nullable=True)
    homepage_u = Column(String(64), nullable=True)
    trfc_info = Column(String(256), nullable=True)
    usage_day = Column(String(50), nullable=True)
    hidy_info = Column(String(128), nullable=True)
    usage_time = Column(String(256), nullable=True)
    usage_amou = Column(String(64), nullable=True)
    middle_siz = Column(String(128), nullable=True)
    main_img_n = Column(String(128), nullable=True)
    main_img_t = Column(String(128), nullable=True)
    itemcntnts = Column(String(1024), nullable=True)
    kakao_rating = Column(Float, nullable=True)

    def __reqr__(self):
        return f"BusanTourInfo: {self.id}, {self.name}, {self.gungu}, {self.lat}, {self.lng}, {self.title}, {self.subtitle}, {self.addr1}, {self.homepage_u}, {self.trfc_info}, {self.usage_day}, {self.hidy_info}, {self.usage_time}, {self.usage_amou}, {self.middle_siz}, {self.main_img_n}, {self.main_img_t}, {self.itemcntnts}, {self.kakao_rating}"
