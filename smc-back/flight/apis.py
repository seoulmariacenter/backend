from rest_framework import status
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


class TransportCreateRetrieve(APIView):
    """
    Transport 객체를 만들고 디테일을 불러오는 뷰
    """
    queryset = Transport.objects.all()

    def get(self, request, *arge, **kwargs):
        # 매개변수 값 pk를 불러온다
        pk = kwargs['pk']
        # queryset에서 transport와 foreign key로 연결된 iata 객체도 한꺼번에 불러온다
        instance = self.queryset.select_related('start_IATA__korean_name',
                                                'end_IATA__korean_name').get(pk=pk)

        data = {
            'flight': str(instance.flight_code),
            'start_IATA': str(instance.start_IATA),
            'end_IATA': str(instance.end_IATA),
            'start_time': str(instance.start_time),
            'end_time': str(instance.end_time)
        }

        return Response(data=data, status=status.HTTP_200_OK)
