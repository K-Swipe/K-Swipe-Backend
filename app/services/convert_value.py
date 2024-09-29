def cvt_thema():
    thema = {
        "쇼핑하기": 1,
        "테마파크 놀러가기": 2,
        "역사 유적지 구경": 3,
        "야외 활동 즐기기": 4,
        "지역 문화공연 관람": 6,
        "힐링과 휴식": 21,
        "지역 축제 참여": 9,
        "다양한 체험 프로그램": 11,
        "촬영지 방문하기": 12,
        "웰니스 여행 즐기기": 21,
        "SNS 인생샷 남기기": 22,
        "호캉스 즐기기": 23,
        "새로운 여행지": 24,
        "인플루언서 추천코스": 26,
        "친환경 여행": 21,
    }
    return thema


def cvt_reason():
    reason = {
        0: 1,
        1: 2,
        2: 7,
        3: 3,
        4: 9,
    }
    return reason


def cvt_style():
    style = {"city": 2, "nature": 0}
    return style


def cvt_traffic():
    traffic = {"car": "자가용", "bus": "대중교통 등"}
    return traffic
