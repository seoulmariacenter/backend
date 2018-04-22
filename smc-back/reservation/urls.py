from django.urls import path

from . import apis

app_name = 'reservation'

urlpatterns = [
    path('check', apis.CheckReservation.as_view(), name='check_reservation')
]
