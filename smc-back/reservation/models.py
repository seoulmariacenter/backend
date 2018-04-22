from django.contrib.auth.models import AnonymousUser, UserManager
from django.db import models


class ReservationHostManager(UserManager):
    def create_user(self, username, password=None, **extra_fields):
        return super().create_user(username=username, password=password, **extra_fields)


class ReservationHost(AnonymousUser, models.Model):
    username = models.CharField(max_length=10)
    password = models.PositiveSmallIntegerField()
    phone_number = models.CharField(max_length=30)
    gender = models.BooleanField(default=True)
    is_active = True

    objects = ReservationHostManager()

    def set_password(self, raw_password):
        pass

    def check_password(self, raw_password):
        pass

    def save(self):
        pass

    def delete(self):
        pass
