from django.contrib.auth.models import User
from django.urls import reverse, resolve
from rest_framework.test import APILiveServerTestCase

from .utils import iata_list
from .management.commands import migrate_iata, migrate_transport
from .models import IATACode, Transport
from .apis import IATACodeList, TransportCreate


class DummyUser:
    def __init__(self):
        """
        자주 쓰는 데이터를 미리 정의해 둔다
        """
        self.data_succeed = {
            'flight_code': 'KE001',
            'start_iata': 'ICN',
            'end_iata': 'FCO',
            'start_day': '2018-04-01',
            'end_day': '2018-04-02',
            'start_time': '12:00',
            'end_time': '21:00'
        }
        self.data_failure = {
            'flight_code': 'KE001',
            'start_iata': 'ABC',
            'end_iata': 'EFG',
            'start_day': '2018-04-01',
            'end_day': '2018-04-02',
            'start_time': '12:00',
            'end_time': '21:00'
        }
        self.user_info = {
            'username': 'dummy',
            'password': 'password'
        }

    def create_user(self):
        user = User.objects.create_user(
            username=self.user_info['username'],
            password=self.user_info['password'],
        )
        user.save()
        return user


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

    def test_default_iata_list_create(self):
        """
        테스트 4. default iata 객체 리스트 생성 커맨드를 테스트한다
        """
        # iata 데이터를 담는 커맨드를 실행한다
        migrate_iata.Command().handle()
        # 쿼리셋을 호출하고 갯수를 센다
        queryset = IATACode.objects.all()
        count = queryset.count()
        # utils에 마련된 코드 네임 갯수와 실제로 DB에 매핑된 코드 네임 갯수가 같은가?
        self.assertEqual(len(iata_list.iata_code_name), count)

    def test_iata_get_list(self):
        """
        테스트 4. iata 리스트를 받아온다
        """
        # iata 데이터를 담는 커맨드를 실행한다
        migrate_iata.Command().handle()
        # 쿼리셋과 response를 불러온다
        queryset = IATACode.objects.all()
        response = self.client.get(self.URL_API_IATA, format='json')

        # 응답 코드가 정상인가?
        self.assertEqual(response.status_code, 200)
        # response에 담긴 데이터 갯수와 queryset의 데이터 갯수가 같은가?
        self.assertEqual(len(response.data), queryset.count())


class TransportTest(APILiveServerTestCase):
    def setUp(self):
        """
        환경 변수 설정
        """
        self.URL_API_TRANSPORT_NAME = 'flight:transport_create'
        self.URL_API_TRANSPORT = '/flight/transport/'
        self.TRANSPORT_VIEW_CLASS = TransportCreate

    def test_transport_url_name_reverse(self):
        """
        테스트 1. url name과 실제 url이 일치하는가
        """
        url = reverse(self.URL_API_TRANSPORT_NAME)
        self.assertEqual(url, self.URL_API_TRANSPORT)

    def test_transport_url_resolve_view_class(self):
        """
        테스트 2. url를 리졸브한 결과가 url name, view와 일치하는가
        """
        resolver_match = resolve(self.URL_API_TRANSPORT)
        self.assertEqual(resolver_match.view_name,
                         self.URL_API_TRANSPORT_NAME)
        self.assertEqual(resolver_match.func.view_class,
                         self.TRANSPORT_VIEW_CLASS)

    def test_default_transport_create(self):
        """
        테스트 3. default transport 객체 생성 커맨드를 테스트한다
        """
        migrate_transport.Command().handle()
        queryset = Transport.objects.all()
        count = queryset.count()
        instance = queryset.get(pk=1)
        self.assertEqual(1, count)
        self.assertEqual('전용 버스', instance.flight_code)

    def test_transport_create(self):
        """
        테스트 4. transport 객체를 생성한다
        """
        # iata 데이터를 담는 커맨드를 실행한다
        migrate_iata.Command().handle()

        # dummy user를 생성하고 로그인한다
        dummy = DummyUser()
        dummy.create_user()
        login = self.client.login(**dummy.user_info)
        # 제대로 로그인 되었는가?
        self.assertTrue(login)

        # dummy user와 data를 이용해 tranport 객체를 생성해 본다
        response = self.client.post(self.URL_API_TRANSPORT, data=dummy.data_succeed)
        # 응답 코드가 정상인가?
        self.assertEqual(response.status_code, 201)
        # response에 담긴 데이터와 dummy data가 같은가?
        self.assertEqual(response.data['flight_code'], dummy.data_succeed['flight_code'])

    def test_transport_create_failure(self):
        """
        테스트 5. transport 객체 생성 실패 케이스를 테스트한다
        """
        # iata 데이터를 담는 커맨드를 실행한다
        migrate_iata.Command().handle()

        # dummy user를 생성하고 로그인한다
        dummy = DummyUser()
        dummy.create_user()
        login = self.client.login(**dummy.user_info)
        # 제대로 로그인 되었는가?
        self.assertTrue(login)

        # dummy user와 data를 이용해 tranport 객체를 생성해 본다
        response = self.client.post(self.URL_API_TRANSPORT, data=dummy.data_failure)
        # 응답 코드가 정상인가?
        self.assertEqual(response.status_code, 400)
        # 실패 메시지가 원하는 대로 출력되는가?
        self.assertEqual(response.data['msg'], 'IATACode matching query does not exist.')
