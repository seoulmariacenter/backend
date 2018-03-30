from django.urls import reverse, resolve
from rest_framework.test import APILiveServerTestCase

from flight.tests import DummyUser
from .apis import ProductListCreate, \
    ProductRetrieveUpdateDestroy, \
    DateListCreate, DateRetrieveUpdateDestroy


class DummyData:
    def __init__(self):
        """
        자주 쓰는 데이터를 미리 정의해 둔다
        """
        self.product_data = {
            'title': 'dummy_title',
            'start_time': '2018-04-01',
            'end_time': '2018-04-06',
            'price': '4,000,000'
        }
        self.date_data = {
            'date_num': '1',
            'date_time': '2018-04-01',
            'product': ''
        }


class ProductTest(APILiveServerTestCase):
    def setUp(self):
        """
        환경 변수 설정
        """
        self.URL_API_PRODUCT_LC_NAME = 'travel:product_view'
        self.URL_API_PRODUCT_RUD_NAME = 'travel:product_detail'
        self.URL_API_PRODUCT = '/travel/product/'
        self.PRODUCT_LC_VIEW_CLASS = ProductListCreate
        self.PRODUCT_RUD_VIEW_CLASS = ProductRetrieveUpdateDestroy
        self.dummy_user = DummyUser()
        self.dummy_data = DummyData()

    def test_product_lc_url_name_reverse(self):
        """
        테스트 1. url name과 실제 url이 일치하는가
        """
        url = reverse(self.URL_API_PRODUCT_LC_NAME)
        self.assertEqual(url, self.URL_API_PRODUCT)

    def test_product_lc_url_resolve_view_class(self):
        """
        테스트 2. url을 리졸브한 결과가 url name, view와 일치하는가
        :return:
        """
        resolver_match = resolve(self.URL_API_PRODUCT)
        self.assertEqual(resolver_match.view_name,
                         self.URL_API_PRODUCT_LC_NAME)
        self.assertEqual(resolver_match.func.view_class,
                         self.PRODUCT_LC_VIEW_CLASS)

    def test_product_rud_url_name_reverse(self):
        """
        테스트 3. url name과 실제 url이 일치하는가
        """
        url = reverse(self.URL_API_PRODUCT_RUD_NAME, args='1')
        self.assertEqual(url, self.URL_API_PRODUCT + '1/')

    def test_product_rud_url_resolve_view_class(self):
        """
        테스트 4. url을 리졸브한 결과가 url name, view와 일치하는가
        :return:
        """
        resolver_match = resolve(self.URL_API_PRODUCT + '1/')
        self.assertEqual(resolver_match.view_name,
                         self.URL_API_PRODUCT_RUD_NAME)
        self.assertEqual(resolver_match.func.view_class,
                         self.PRODUCT_RUD_VIEW_CLASS)

    def test_product_create(self):
        """
        테스트 5. product 객체를 생성한다
        """
        dummy_user = self.dummy_user
        dummy_user.create_user()
        login = self.client.login(**dummy_user.user_info)
        self.assertTrue(login)

        response = self.client.post(self.URL_API_PRODUCT, data=self.dummy_data.product_data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['title'], self.dummy_data.product_data['title'])

    def test_product_list(self):
        """
        테스트 6. product 객체의 리스트를 확인한다
        """
        dummy_user = self.dummy_user
        dummy_user.create_user()
        login = self.client.login(**dummy_user.user_info)
        self.assertTrue(login)

        # product 객체를 5개 생성한다
        for _ in range(1, 6):
            self.client.post(self.URL_API_PRODUCT, data=self.dummy_data.product_data)

        response = self.client.get(self.URL_API_PRODUCT)
        # 응답 코드 및 생성된 객체 갯수를 확인한다
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 5)

    def test_product_retrieve(self):
        """
        테스트 7. product 객체의 retrieve 테스트
        """
        dummy_user = self.dummy_user
        dummy_user.create_user()
        login = self.client.login(**dummy_user.user_info)
        self.assertTrue(login)

        response_create = self.client.post(self.URL_API_PRODUCT, data=self.dummy_data.product_data)
        self.assertEqual(response_create.status_code, 201)

        primary_key = str(response_create.data['pk']) + '/'
        response_retrieve = self.client.get(self.URL_API_PRODUCT + primary_key)
        self.assertEqual(response_retrieve.status_code, 200)

    def test_product_update(self):
        """
        테스트 8. product 객체의 update 테스트
        """
        dummy_user = self.dummy_user
        dummy_user.create_user()
        login = self.client.login(**dummy_user.user_info)
        self.assertTrue(login)

        response_create = self.client.post(self.URL_API_PRODUCT, data=self.dummy_data.product_data)
        self.assertEqual(response_create.status_code, 201)

        primary_key = str(response_create.data['pk']) + '/'
        response_update = self.client.patch(self.URL_API_PRODUCT + primary_key, data={'title': 'vietnam'})
        self.assertEqual(response_update.status_code, 200)
        self.assertEqual(response_update.data['title'], 'vietnam')

    def test_product_destroy(self):
        """
        테스트 9. product 객체의 destroy 테스트
        """
        dummy_user = self.dummy_user
        dummy_user.create_user()
        login = self.client.login(**dummy_user.user_info)
        self.assertTrue(login)

        response_create = self.client.post(self.URL_API_PRODUCT, data=self.dummy_data.product_data)
        self.assertEqual(response_create.status_code, 201)

        primary_key = str(response_create.data['pk']) + '/'
        response_destroy = self.client.delete(self.URL_API_PRODUCT + primary_key)
        self.assertEqual(response_destroy.status_code, 204)


class DateTest(APILiveServerTestCase):
    def setUp(self):
        """
        환경 변수 설정
        """
        self.URL_API_DATE_LC_NAME = 'travel:date_view'
        self.URL_API_DATE_RUD_NAME = 'travel:date_detail'
        self.PRODUCT_PK = '1'
        self.URL_API_DATE = '/travel/product/' + self.product_pk + '/date/'
        self.URL_API_PRODUCT = '/travel/product/'
        self.DATE_LC_VIEW_CLASS = DateListCreate
        self.DATE_RUD_VIEW_CLASS = DateRetrieveUpdateDestroy
        self.dummy_user = DummyUser()
        self.dummy_data = DummyData()

    """
    product_pk와 url_api_date를 동적으로 구성하기 위한 getter/setter 구성
    """

    @property
    def product_pk(self):
        return self.PRODUCT_PK

    @product_pk.setter
    def product_pk(self, input_value):
        self.PRODUCT_PK = input_value

    @property
    def url_api_date(self):
        return self.URL_API_DATE

    @url_api_date.setter
    def url_api_date(self, input_pk):
        blank_1, travel, product, pk, date, blank_2 = self.URL_API_DATE.split('/')
        new_pk = str(input_pk)
        self.URL_API_DATE = '/' + '/'.join((travel, product, new_pk, date)) + '/'

    def test_date_lc_url_name_reverse(self):
        """
        테스트 1. url name과 실제 url이 일치하는가
        """
        url = reverse(self.URL_API_DATE_LC_NAME, args='1')
        self.assertEqual(url, self.URL_API_DATE)

    def test_date_lc_url_resolve_view_class(self):
        """
        테스트 2. url을 리졸브한 결과가 url name, view와 일치하는가
        :return:
        """
        resolver_match = resolve(self.URL_API_DATE)
        self.assertEqual(resolver_match.view_name,
                         self.URL_API_DATE_LC_NAME)
        self.assertEqual(resolver_match.func.view_class,
                         self.DATE_LC_VIEW_CLASS)

    def test_date_rud_url_name_reverse(self):
        """
        테스트 3. url name과 실제 url이 일치하는가
        """
        url = reverse(self.URL_API_DATE_RUD_NAME, args=('1', '1',))
        self.assertEqual(url, self.URL_API_DATE + '1/')

    def test_date_rud_url_resolve_view_class(self):
        """
        테스트 4. url을 리졸브한 결과가 url name, view와 일치하는가
        :return:
        """
        resolver_match = resolve(self.URL_API_DATE + '1/')
        self.assertEqual(resolver_match.view_name,
                         self.URL_API_DATE_RUD_NAME)
        self.assertEqual(resolver_match.func.view_class,
                         self.DATE_RUD_VIEW_CLASS)

    def test_date_create(self):
        """
        테스트 5. date 객체를 생성한다
        """
        # 로그인
        dummy_user = self.dummy_user
        dummy_user.create_user()
        login = self.client.login(**dummy_user.user_info)
        self.assertTrue(login)

        # product 객체 생성
        response_product = self.client.post(self.URL_API_PRODUCT, data=self.dummy_data.product_data)
        self.dummy_data.date_data['product'] = response_product.data['pk']

        # product pk에 따라 date api url 변경
        self.product_pk = response_product.data['pk']
        self.url_api_date = self.product_pk

        # product 객체를 foreign key로 하는 date 객체 생성
        response_date = self.client.post(self.URL_API_DATE, data=self.dummy_data.date_data)
        self.assertEqual(response_date.status_code, 201)
        self.assertEqual(response_date.data['date_time'], self.dummy_data.date_data['date_time'])

    def test_date_list(self):
        """
        테스트 6. date list를 생성한다
        """
        # 로그인
        dummy_user = self.dummy_user
        dummy_user.create_user()
        login = self.client.login(**dummy_user.user_info)
        self.assertTrue(login)

        # product 객체 생성
        response_product = self.client.post(self.URL_API_PRODUCT, data=self.dummy_data.product_data)
        self.dummy_data.date_data['product'] = response_product.data['pk']

        # product pk에 따라 date api url 변경
        self.product_pk = response_product.data['pk']
        self.url_api_date = self.product_pk

        # product 객체를 foreign key로 하는 date 객체 5회 생성
        # date 날짜에 따라 객체 index 동적 구성
        for i in range(1, 6):
            self.client.post(self.url_api_date,
                             data={'date_num': str(i),
                                   'date_time': f'2018-04-0{i}',
                                   'price': '4,000,000',
                                   'product': self.product_pk}
                             )

        # date 객체의 갯수 파악
        response_date = self.client.get(self.url_api_date)
        self.assertEqual(response_date.status_code, 200)
        self.assertEqual(response_date.data['count'], 5)

    def test_date_retrieve(self):
        """
        테스트 7. date 객체의 retrieve 테스트
        """
        # 로그인
        dummy_user = self.dummy_user
        dummy_user.create_user()
        login = self.client.login(**dummy_user.user_info)
        self.assertTrue(login)

        # date 객체 생성
        response_product = self.client.post(self.URL_API_PRODUCT, data=self.dummy_data.product_data)
        self.dummy_data.date_data['product'] = response_product.data['pk']

        # product pk에 따라 date api url 변경
        self.product_pk = response_product.data['pk']
        self.url_api_date = self.product_pk

        # product 객체를 foreign key로 하는 date 객체 생성
        response_date = self.client.post(self.url_api_date, data=self.dummy_data.date_data)
        self.assertEqual(response_date.status_code, 201)

        # date 객체 retrieve
        response_retrieve = self.client.get(self.url_api_date + '1/')
        self.assertEqual(response_retrieve.status_code, 200)
        self.assertEqual(response_retrieve.data['date_time'], self.dummy_data.date_data['date_time'])

    def test_date_update(self):
        """
        테스트 8. date 객체의 update 테스트
        """
        # 로그인
        dummy_user = self.dummy_user
        dummy_user.create_user()
        login = self.client.login(**dummy_user.user_info)
        self.assertTrue(login)

        # date 객체 생성
        response_product = self.client.post(self.URL_API_PRODUCT, data=self.dummy_data.product_data)
        self.dummy_data.date_data['product'] = response_product.data['pk']

        # product pk에 따라 date api url 변경
        self.product_pk = response_product.data['pk']
        self.url_api_date = self.product_pk

        # product 객체를 foreign key로 하는 date 객체 생성
        response_date = self.client.post(self.url_api_date, data=self.dummy_data.date_data)
        self.assertEqual(response_date.status_code, 201)

        # date 객체 update
        response_update = self.client.patch(self.url_api_date + str(response_date.data['date_num']) + '/',
                                            data={
                                                'date_time': '2018-04-10'
                                            })
        self.assertEqual(response_update.status_code, 200)
        self.assertEqual(response_update.data['date_time'], '2018-04-10')

    def test_date_destroy(self):
        """
        테스트 9. date 객체 destroy 테스트
        """
        # 로그인
        dummy_user = self.dummy_user
        dummy_user.create_user()
        login = self.client.login(**dummy_user.user_info)
        self.assertTrue(login)

        # date 객체 생성
        response_product = self.client.post(self.URL_API_PRODUCT, data=self.dummy_data.product_data)
        self.dummy_data.date_data['product'] = response_product.data['pk']

        # product pk에 따라 date api url 변경
        self.product_pk = response_product.data['pk']
        self.url_api_date = self.product_pk

        # product 객체를 foreign key로 하는 date 객체 생성
        response_date = self.client.post(self.url_api_date, data=self.dummy_data.date_data)
        self.assertEqual(response_date.status_code, 201)

        # date 객체 destroy
        response_destroy = self.client.delete(self.url_api_date + str(response_date.data['date_num']) +'/')
        self.assertEqual(response_destroy.status_code, 204)
