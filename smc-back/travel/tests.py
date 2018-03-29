from django.urls import reverse, resolve
from rest_framework.test import APILiveServerTestCase

from flight.tests import DummyUser
from .apis import ProductListCreate, ProductRetrieveUpdateDestroy


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


class ProductTest(APILiveServerTestCase):
    def setUp(self):
        """
        환경 변수 설정
        """
        self.URL_API_PRODUCT_NAME = 'travel:product_view'
        self.URL_API_PRODUCT = '/travel/product/'
        self.PRODUCT_LC_VIEW_CLASS = ProductListCreate
        self.PRODUCT_RUD_VIEW_CLASS = ProductRetrieveUpdateDestroy
        self.dummy_user = DummyUser()
        self.dummy_data = DummyData()

    def test_product_url_name_reverse(self):
        """
        테스트 1. url name과 실제 url이 일치하는가
        """
        url = reverse(self.URL_API_PRODUCT_NAME)
        self.assertEqual(url, self.URL_API_PRODUCT)

    def test_product_url_resolve_view_class(self):
        """
        테스트 2. url을 리졸브한 결과가 url name, view와 일치하는가
        :return:
        """
        resolver_match = resolve(self.URL_API_PRODUCT)
        self.assertEqual(resolver_match.view_name,
                         self.URL_API_PRODUCT_NAME)
        self.assertEqual(resolver_match.func.view_class,
                         self.PRODUCT_LC_VIEW_CLASS)

    def test_product_create(self):
        """
        테스트 3. product 객체를 생성한다
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
        테스트 4. product 객체의 리스트를 확인한다
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
        테스트 5. product 객체의 retrieve 테스트
        """
        dummy_user = self.dummy_user
        dummy_user.create_user()
        login = self.client.login(**dummy_user.user_info)
        self.assertTrue(login)

        response_create = self.client.post(self.URL_API_PRODUCT, data=self.dummy_data.product_data)
        self.assertEqual(response_create.status_code, 201)

        primary_key = str(response_create.data['pk']) + '/'
        response_retrieve = self.client.get(self.URL_API_PRODUCT+primary_key)
        self.assertEqual(response_retrieve.status_code, 200)

    def test_product_update(self):
        """
        테스트 5. product 객체의 update 테스트
        """
        dummy_user = self.dummy_user
        dummy_user.create_user()
        login = self.client.login(**dummy_user.user_info)
        self.assertTrue(login)

        response_create = self.client.post(self.URL_API_PRODUCT, data=self.dummy_data.product_data)
        self.assertEqual(response_create.status_code, 201)

        primary_key = str(response_create.data['pk']) + '/'
        response_update = self.client.patch(self.URL_API_PRODUCT+primary_key, data={'title': 'vietnam'})
        self.assertEqual(response_update.status_code, 200)
        self.assertEqual(response_update.data['title'], 'vietnam')

    def test_product_delete(self):
        """
        테스트 6. product 객체의 delete 테스트
        """
        dummy_user = self.dummy_user
        dummy_user.create_user()
        login = self.client.login(**dummy_user.user_info)
        self.assertTrue(login)

        response_create = self.client.post(self.URL_API_PRODUCT, data=self.dummy_data.product_data)
        self.assertEqual(response_create.status_code, 201)

        primary_key = str(response_create.data['pk']) + '/'
        response_delete = self.client.delete(self.URL_API_PRODUCT+primary_key)
        self.assertEqual(response_delete.status_code, 204)
