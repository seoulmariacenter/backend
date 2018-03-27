from django.core.management import BaseCommand

from ...models import Transport


class Command(BaseCommand):
    """
    기본 운송수단 (전용버스)를 자동으로 매핑한다
    """

    def handle(self, *args, **options):
        queryset = Transport.objects.all()
        if not queryset.filter(flight_code='전용 버스').exists():
            Transport.objects.create(
                flight_code='전용 버스'
            )
            print(f'기본 운송 수단 {Transport.objects.get(flight_code="전용 버스")} 아이템이 추가되었습니다.')

        else:
            print(f'기본 운송 수단 {Transport.objects.get(flight_code="전용 버스")} 아이템이 이미 존재합니다.')
