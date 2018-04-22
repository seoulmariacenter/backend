import json

from django.http import HttpResponse
from rest_framework import permissions, status
from rest_framework.views import APIView

from .models import ReservationHost


class MakeReservation(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        name = request.data.get('username', '')
        phone_number = request.data.get('phone_number', '')
        gender = request.data.get('gender', True)

        user, reservation_num_list = ReservationHost.objects.create_user(
            name=name,
            phone_number=phone_number,
            gender=gender
        )

        data = {
            'username': user.username,
            'phone_number': user.phone_number,
            'gender': user.gender,
            'reservation_num': f'{reservation_num_list[0]}-'
                               f'{reservation_num_list[1]}-'
                               f'{reservation_num_list[2]}-'
                               f'{reservation_num_list[-1]}'
        }

        return HttpResponse(json.dumps(data),
                            content_type='application/json; charset=utf-8',
                            status=status.HTTP_201_CREATED)


class CheckReservation(APIView):
    def post(self, request, *args, **kwargs):
        pass
