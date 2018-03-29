from django.urls import path

from . import apis

app_name = 'travel'

urlpatterns = [
    # 순례 상품 URL
    path('product/', apis.ProductListCreate.as_view(), name='product_view'),
    path('product/<int:pk>/', apis.ProductRetrieveUpdateDestroy.as_view(), name='product_detail'),
    # 하루 일정 URL
    path('product/<int:pk>/date/', apis.DateListCreate.as_view(), name='date_view'),
    path('product/<int:pk>/date/<int:date_num>/', apis.DateRetrieveUpdateDestroy.as_view(), name='date_detail'),
]
