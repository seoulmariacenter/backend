from django.urls import path

from . import apis

app_name = 'flight'

urlpatterns = [
    path('iata/', apis.IATACodeList.as_view(), name='iata'),
    path('transport/', apis.TransportCreate.as_view(), name='transport_create'),
    path('transport/<int:pk>/', apis.TransportRetrieve.as_view(), name='transport_get'),
]
