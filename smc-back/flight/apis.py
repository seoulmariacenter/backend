import json

from django.http import HttpResponse
from rest_framework import status
from rest_framework.views import APIView

from .models import IATACode


class IATACodeCreateRetrieve(APIView):
    """
    IATA 코드 목록을 불러오는 뷰
    """
    queryset = IATACode.objects.all()

    def get(self, request, *args, **kwargs):
        data = dict()

        # IATA 쿼리셋을 순회하며 모든 아이템을 딕셔너리에 매핑한다
        for item in self.queryset.all():
            data[str(item.korean_name)] = str(item.code_name)

        # 퍼포먼스 향상을 위해 serializer, Response 함수는 쓰지 않고
        # data를 json으로 직접 변환해 순수 HttpResponse에 파싱한다
        return HttpResponse(json.dumps(data),
                            content_type='application/json; charset=utf-8',
                            status=status.HTTP_200_OK)