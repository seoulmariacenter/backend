from django.urls import path

from . import apis

app_name = 'flight'

urlpatterns = [
    path('iata/', apis.IATACodeCreateRetrieve.as_view(), name='iata'),
]
