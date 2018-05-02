import json

from django.contrib.auth import authenticate
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.utils import timezone
from rest_framework import permissions, status, generics
from rest_framework.response import Response
from rest_framework.views import APIView

from travel.models import Product
from travel.paginations import StandardPagination
from .models import ReservationHost
from .serializers import ReservationSerializer, ReservationMemberSerializer


class MakeReservation(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        name = request.data.get('username', '')
        christian_name = request.data.get('christian_name', '')
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
            christian_name=christian_name,
            phone_number=phone_number,
            gender=gender,
            product=product_object,
        )

        if user:
            data = {
                'product': user.product.title,
                'username': user.username,
                'christian_name': user.christian_name,
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
                'pk': user.pk,
                'product': user.reservationhost.product.title,
                'product_pk': user.reservationhost.product.pk,
                'username': user.username,
                'christian_name': user.reservationhost.christian_name,
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


class CancelReservation(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        name = request.data.get('name', '')
        password = request.data.get('password', '')

        user = authenticate(
            username=name,
            password=password,
        )
        if user:
            user.date_canceled = timezone.localtime()
            user.save()
            user.is_active = False
            user.save()
            return Response(status.HTTP_200_OK)

        else:
            data = {
                'message': '입력 정보가 잘못되었습니다. 다시 입력해주세요!'
            }

            return HttpResponse(json.dumps(data),
                                content_type='application/json; charset=utf-8',
                                status=status.HTTP_400_BAD_REQUEST)


class UpdateReservation(APIView):
    permission_classes = (permissions.AllowAny,)

    def patch(self, request, *args, **kwargs):
        pass


class DestroyReservation(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def delete(self, request, *args, **kwargs):
        pk = request.data.get('pk', '')

        user = ReservationHost.objects.get(pk=pk)

        if user:
            user.delete()
            return Response(status.HTTP_204_NO_CONTENT)

        else:
            data = {
                'message': '입력 정보가 잘못되었습니다. 다시 입력해주세요!'
            }

            return HttpResponse(json.dumps(data),
                                content_type='application/json; charset=utf-8',
                                status=status.HTTP_400_BAD_REQUEST)


class AllReservationList(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    pagination_class = StandardPagination
    serializer_class = ReservationSerializer

    def get_queryset(self):
        product = Product.objects.all()
        select = product.get(pk=self.kwargs['product_pk'])
        return select.reservationhost_set.all()


class ActiveReservationList(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    pagination_class = StandardPagination
    serializer_class = ReservationSerializer

    def get_queryset(self):
        product = Product.objects.all()
        select = product.get(pk=self.kwargs['product_pk'])
        return select.reservationhost_set.filter(is_active=True)


class ReservationHostRetrieveDestroy(generics.RetrieveDestroyAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ReservationSerializer
    lookup_url_kwarg = 'host_pk'

    def get_queryset(self):
        product = Product.objects.all()
        select = product.get(pk=self.kwargs['product_pk'])
        return select.reservationhost_set.all()


class ReservationMemberListCreate(generics.ListCreateAPIView):
    permission_classes = (permissions.AllowAny,)
    pagination_class = StandardPagination
    serializer_class = ReservationMemberSerializer

    def get_queryset(self):
        host = ReservationHost.objects.all()
        select = host.get(pk=self.kwargs['host_pk'])
        return select.reservationmember_set.all()


class ReservationMemberRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = ReservationMemberSerializer
    lookup_url_kwarg = 'member_pk'

    def get_queryset(self):
        host = ReservationHost.objects.all()
        select = host.get(pk=self.kwargs['host_pk'])
        return select.reservationmember_set.all()
