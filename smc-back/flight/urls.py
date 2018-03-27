from django.urls import path

from . import apis

app_name = 'flight'

urlpatterns = [
    path('iata/', apis.IATACodeList.as_view(), name='iata'),
]
