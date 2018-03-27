import json

from datetime import datetime
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import IATACode, Transport


class IATACodeList(APIView):
    """
    IATA 코드 목록을 불러오는 뷰
    """
    queryset = IATACode.objects.all()

    def get(self, request, *args, **kwargs):
        data = dict()

        # IATA 쿼리셋을 순회하며 모든 아이템을 딕셔너리에 매핑한다
        for item in self.queryset.all():
            data[str(item.korean_name)] = str(item.code_name)

        # 퍼포먼스 향상을 위해 serializer는 쓰지 않는다
        return Response(data=data, status=status.HTTP_200_OK)


class TransportCreate(APIView):
    """
    Transport 객체를 생성하는 뷰
    """
    queryset_transport = Transport.objects.all()
    queryset_iata = IATACode.objects.select_related('korean_name__korean_name').all()
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def post(self, request, *args, **kwargs):
        # frontend에서 날아온 bytecode를 utf-8로 디코딩
        body_unicode = request.body.decode('utf-8')
        # 문자열을 json으로 불러옴
        payload = json.loads(body_unicode)

        flight_code = payload['flight_code']

        start_iata = self.queryset_iata.get(code_name=payload['start_iata'])
        end_iata = self.queryset_iata.get(code_name=payload['end_iata'])

        start_year, start_month, start_day = payload['start_day'].split('-')
        end_year, end_month, end_day = payload['end_day'].split('-')

        start_hour, start_minute = payload['start_time'].split(':')
        end_hour, end_minute = payload['end_time'].split(':')

        start_time_instance = datetime(
            int(start_year), int(start_month), int(start_day),
            int(start_hour), int(start_minute)
        )

        end_time_instance = datetime(
            int(end_year), int(end_month), int(end_day),
            int(end_hour), int(end_minute)
        )

        instance = Transport.objects.create(
            flight_code=flight_code,
            start_IATA=start_iata,
            end_IATA=end_iata,
            start_time=start_time_instance,
            end_time=end_time_instance,
        )

        data = {
            'flight_code': str(instance.flight_code),
            'start_IATA': str(instance.start_IATA),
            'end_IATA': str(instance.end_IATA),
            'start_time': str(instance.start_time),
            'end_time': str(instance.end_time)
        }

        return Response(data=data, status=status.HTTP_201_CREATED)


class TransportRetrieve(APIView):
    """
    Transport 객체의 디테일을 불러오는 뷰
    """
    queryset = Transport.objects.all()

    def get(self, request, *arge, **kwargs):
        # 매개변수 값 pk를 불러온다
        pk = kwargs['pk']
        # queryset에서 transport와 foreign key로 연결된 iata 객체도 한꺼번에 불러온다
        instance = self.queryset.select_related('start_IATA__korean_name',
                                                'end_IATA__korean_name').get(pk=pk)

        data = {
            'flight_code': str(instance.flight_code),
            'start_IATA': str(instance.start_IATA),
            'end_IATA': str(instance.end_IATA),
            'start_time': str(instance.start_time),
            'end_time': str(instance.end_time)
        }

        return Response(data=data, status=status.HTTP_200_OK)
