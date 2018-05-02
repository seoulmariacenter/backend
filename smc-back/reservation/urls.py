from django.urls import path

from . import apis

app_name = 'reservation'

urlpatterns = [
    path('make/', apis.MakeReservation.as_view(), name='make_reservation'),
    path('check/', apis.CheckReservation.as_view(), name='check_reservation'),
    path('cancel/', apis.CancelReservation.as_view(), name='cancel_reservation'),
    path('destroy/', apis.DestroyReservation.as_view(), name='destroy_reservation'),
]

urlpatterns += [
    path('list/<int:pk>/', apis.AllReservationList.as_view(), name='reservation_list'),
    path('list/<int:pk>/active/', apis.ActiveReservationList.as_view(), name='reservation_list'),
]

urlpatterns += [
    path('member/<int:pk>/', apis.ReservationMemberListCreate.as_view(), name='reservation_member'),
    path('member/<int:pk>/detail/<int:member_pk>/', apis.ReservationMemberUpdateDestroy.as_view(), name='member_detail')
]
