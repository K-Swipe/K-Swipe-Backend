from sqlalchemy import Column, Integer, String, Float

from entities.base import Base


class BusanTourInfo(Base):
    __tablename__ = "busan_tour_info"

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    gungu = Column(String(50))
    lat = Column(Float)
    lng = Column(Float)
    title = Column(String(50))
    subtitle = Column(String(50))
    addr1 = Column(String(50))
    homepage_u = Column(String(64))
    trfc_info = Column(String(256))
    usage_day = Column(String(50))
    hidy_info = Column(String(128))
    usage_time = Column(String(256))
    usage_amou = Column(String(64))
    middle_siz = Column(String(128))
    main_img_n = Column(String(128))
    main_img_t = Column(String(128))
    itemcntnts = Column(String(1024))
    kakao_rating = Column(Float)

    def __reqr__(self):
        return f"BusanTourInfo: {self.id}, {self.name}, {self.gungu}, {self.lat}, {self.lng}, {self.title}, {self.subtitle}, {self.addr1}, {self.homepage_u}, {self.trfc_info}, {self.usage_day}, {self.hidy_info}, {self.usage_time}, {self.usage_amou}, {self.middle_siz}, {self.main_img_n}, {self.main_img_t}, {self.itemcntnts}, {self.kakao_rating}"
