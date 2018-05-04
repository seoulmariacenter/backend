from django.conf import settings
from django.contrib.auth import get_user_model

from django.core.management import BaseCommand

User = get_user_model()


class Command(BaseCommand):
    def handle(self, *args, **options):
        new_user = User.objects.create_superuser(
            username=settings.SUPERUSER_USERNAME,
            email='',
            password=settings.SUPERUSER_PASSWORD,
        )
        print(f'관리자 아이디 "{new_user}"가 생성되었습니다')
