import random

from django.contrib.auth.models import UserManager, User
from django.db import models


class ReservationHostManager(UserManager):
    def create_user(self, name, password=None, **extra_fields):
        # 기존 UserManager class의 create_user 메서드 상속
        user = super().create_user(username=name, password=password, **extra_fields)
        # list comprehension으로 예매번호 리스트 생성 (예: ['1111', '2222', '3333', '4444']
        # 클라이언트에게는 4개의 4자리 비밀번호를 입력하도록 할 예정 (예: ____-____-____-____ )
        reservation_num_list = [str(random.randint(1000, 9999)) for _ in range(4)]
        # 예매번호를 하나의 문자열로 합침
        reservation_num = ''.join(reservation_num_list)
        # 하나로 합친 예매번호를 패스워드로 설정 후 저장
        user.set_password(reservation_num)
        user.save(using=self._db)
        return user, reservation_num_list

    def create_superuser(self, username, password, email=None, **extra_fields):
        return super().create_superuser(username, email, password, **extra_fields)


class ReservationHost(User):
    name = models.CharField(max_length=10, unique=False)
    phone_number = models.CharField(max_length=30, unique=False)
    gender = models.BooleanField(default=True)
    is_active = True

    objects = ReservationHostManager()
