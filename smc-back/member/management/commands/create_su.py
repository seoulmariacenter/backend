from django.conf import settings
from django.contrib.auth.models import User
from django.core.management import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        user = User.objects.get(
            username=settings.SUPERUSER_USERNAME,
        )

        if not user:
            new_user = User.objects.create_superuser(
                username=settings.SUPERUSER_USERNAME,
                password=settings.SUPERUSER_PASSWORD,
            )
            print(f'관리자 아이디 "{new_user}"가 생성되었습니다')

        else:
            print(f'관리자 아이디 "{user}"가 이미 존재합니다')
