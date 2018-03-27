from django.urls import reverse, resolve
from rest_framework.test import APILiveServerTestCase

from flight.management.commands import migrate_iata
from .models import IATACode
from .apis import IATACodeList


class IATATest(APILiveServerTestCase):
    def setUp(self):
        """
        환경 변수 설정
        """
        self.URL_API_IATA_NAME = 'flight:iata'
        self.URL_API_IATA = '/flight/iata/'
        self.IATA_VIEW_CLASS = IATACodeList

    def test_iata_url_name_reverse(self):
        """
        테스트 1. url name과 실제 url이 일치하는가
        """
        url = reverse(self.URL_API_IATA_NAME)
        self.assertEqual(url, self.URL_API_IATA)

    def test_iata_url_resolve_view_class(self):
        """
        테스트 2. url를 리졸브한 결과가 url name, view와 일치하는가
        """
        resolver_match = resolve(self.URL_API_IATA)
        self.assertEqual(resolver_match.view_name,
                         self.URL_API_IATA_NAME)
        self.assertEqual(resolver_match.func.view_class,
                         self.IATA_VIEW_CLASS)

    def test_iata_get_list(self):
        """
        테스트 3. iata 리스트를 받아온다
        """
        # iata 데이터를 담는 커맨드를 실행한다
        migrate_iata.Command().handle()
        # 쿼리셋과 response를 불러온다
        queryset = IATACode.objects.all()
        response = self.client.get(self.URL_API_IATA, format='json')

        # 응답코드가 정상인가?
        self.assertEqual(response.status_code, 200)
        # response에 담긴 데이터 갯수와 queryset의 데이터 갯수가 같은가?
        self.assertEqual(len(response.data), queryset.count())
