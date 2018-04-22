from django.urls import path

from . import apis

app_name = 'reservation'

urlpatterns = [
    path('make/', apis.MakeReservation.as_view(), name='make_reservation'),
    path('check/', apis.CheckReservation.as_view(), name='check_reservation')
]
