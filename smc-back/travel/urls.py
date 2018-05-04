from django.urls import path

from . import apis

app_name = 'travel'

urlpatterns = [
    # 순례 상품 URL
    path('product/', apis.ProductListCreate.as_view(), name='product_view'),
    path('product/publish/', apis.PublishedProductList.as_view(), name='published_product_view'),
    path('product/publish/<int:pk>/', apis.PublishedProductRetrieve.as_view(), name='published_product_detail'),
    path('product/<int:pk>/', apis.ProductRetrieveUpdateDestroy.as_view(), name='product_detail'),
    path('product/<int:pk>/image/', apis.ProductImageUpdate.as_view(), name='product_image'),
    # 하루 일정 URL
    path('product/<int:pk>/date/', apis.DateListCreate.as_view(), name='date_view'),
    path('product/<int:pk>/date/<int:date_num>/', apis.DateRetrieveUpdateDestroy.as_view(), name='date_detail'),
    # 스케줄 URL
    path('product/<int:pk>/date/<int:date_num>/schedule/', apis.ScheduleListCreate.as_view(), name='schedule_view'),
    path('product/<int:pk>/date/<int:date_num>/schedule/<int:schedule_pk>/', apis.ScheduleRetrieveUpdateDestroy.as_view(), name='schedule_detail')
]
