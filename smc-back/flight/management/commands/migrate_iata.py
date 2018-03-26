from django.core.management import BaseCommand

from ...models import IATAKorean, IATACode
from ...utils import make_iata_pair


class Command(BaseCommand):
    """
    IATA 데이터를 자동으로 매핑한다
    """

    def handle(self, *args, **options):
        # 쿼리셋 호출
        queryset = IATACode.objects.all()
        # iata 제너레이터 컴프리헨션 호출
        iata_pair = make_iata_pair()
        # 추가된 아이템 카운트를 잴 변수
        appended_item_count = 0

        # iata_pair를 순회하며 DB에 없는 아이템을 추가한다
        for pair in iata_pair:
            if not queryset.filter(code_name=pair.code_name).exists():
                korean_instance = IATAKorean.objects.create(
                    korean_name=pair.korean_name
                )
                IATACode.objects.create(
                    korean_name=korean_instance,
                    code_name=pair.code_name,
                )

                appended_item_count += 1

        print(f'총 {appended_item_count}개의 아이템이 추가되었습니다.')
