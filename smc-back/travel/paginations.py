from rest_framework.pagination import PageNumberPagination


class StandardPagination(PageNumberPagination):
    page_size = 6
    page_query_param = 'page'
    max_page_size = 100
