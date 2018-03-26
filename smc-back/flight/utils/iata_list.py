from typing import NamedTuple

# iata 한글 이름 튜플
iata_korean_name = (
    '인천',
    '김포',
    '텔아비브',
    '하노이',
    '후에',
    '다낭',
    '마드리드',
    '바르셀로나',
    '두브로브니크',
    '스플리트',
    '로마, 피우미치노',
    '로마, 참피노',
    '도쿄, 나리타',
    '도쿄, 하네다',
)

# iata 공항 코드 튜플
iata_code_name = (
    'ICN',
    'GMP',
    'TLV',
    'HAN',
    'HUI',
    'DAD',
    'MAD',
    'BCN',
    'DBV',
    'SPU',
    'FCO',
    'CIA',
    'NRT',
    'HND',
)


# 두 자료를 엮을 네임드튜플 자료구조 정의
class IATAPair(NamedTuple):
    korean_name: str
    code_name: str


# 두 자료를 제너레이터 컴프리헨션으로 묶는 함수
def make_iata_pair():
    return (IATAPair(korean_name=korean,
                     code_name=code)
            for korean, code
            in zip(iata_korean_name,
                   iata_code_name)
            )
