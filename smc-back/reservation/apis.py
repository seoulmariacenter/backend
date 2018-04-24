import json

from django.contrib.auth import authenticate
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from rest_framework import permissions, status
from rest_framework.views import APIView

from travel.models import Product
from .models import ReservationHost


class MakeReservation(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        name = request.data.get('username', '')
        phone_number = request.data.get('phone_number', '')
        gender = request.data.get('gender', True)
        product = request.data.get('product', '')

        try:
            product_object = Product.objects.get(pk=product)

        except ObjectDoesNotExist:
            data = {
                'message': '순례 상품을 반드시 선택해 주세요!'
            }
            return HttpResponse(json.dumps(data),
                                content_type='application/json; charset=utf-8',
                                status=status.HTTP_400_BAD_REQUEST)

        user, reservation_num_list = ReservationHost.objects.create_user(
            name=name,
            phone_number=phone_number,
            gender=gender,
            product=product_object,
        )

        if user:
            data = {
                'product': user.product.title,
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

        else:
            data = {
                'message': '입력 정보가 잘못되었습니다. 다시 입력해주세요!'
            }

            return HttpResponse(json.dumps(data),
                                content_type='application/json; charset=utf-8',
                                status=status.HTTP_400_BAD_REQUEST)


class CheckReservation(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        name = request.data.get('name', '')
        password = request.data.get('password', '')

        user = authenticate(
            username=name,
            password=password,
        )

        if user:
            data = {
                'product': user.reservationhost.product.title,
                'username': user.username,
                'phone_number': user.reservationhost.phone_number,
                'gender': user.reservationhost.gender,
            }

            return HttpResponse(json.dumps(data),
                                content_type='application/json; charset=utf-8',
                                status=status.HTTP_200_OK)

        else:
            data = {
                'message': '입력 정보가 잘못되었습니다. 다시 입력해주세요!'
            }

            return HttpResponse(json.dumps(data),
                                content_type='application/json; charset=utf-8',
                                status=status.HTTP_400_BAD_REQUEST)
