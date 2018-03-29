from rest_framework import generics, permissions

from .paginations import StandardPagination
from .serializers import ProductSerializer, DateSerializer
from .models import Product, Date


class ProductListCreate(generics.ListCreateAPIView):
    """
    순례 상품을 생성하고 리스트를 반환하는 뷰
    상품 생성은 authenticated 유저만 가능
    pagination을 이용하는 게 효과적이라 판단해 generic view와 serializer 사용
    """
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = StandardPagination


class ProductRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    """
    순례 상품의 디테일, 수정, 삭제를 담당하는 뷰
    상품 수정, 삭제는 authenticated 유저만 가능
    """
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class DateListCreate(generics.ListCreateAPIView):
    """
    하루 일정을 생성하고 리스트를 반환하는 뷰
    """
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = DateSerializer
    pagination_class = StandardPagination

    def get_queryset(self):
        product = self.kwargs['pk']
        return Date.objects.select_related('product').filter(product_id=product)


class DateRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    """
    하루 일정의 디테일, 수정, 삭제를 담당하는 뷰
    """
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = DateSerializer
    lookup_field = 'date_num'
    lookup_url_kwarg = 'date_num'

    def get_queryset(self):
        product = self.kwargs['pk']
        return Date.objects.select_related('product').filter(product_id=product)
