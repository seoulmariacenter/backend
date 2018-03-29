from django.urls import path

from . import apis

app_name = 'travel'

urlpatterns = [
    path('product/', apis.ProductListCreate.as_view(), name='product_view'),
    path('product/<int:pk>/', apis.ProductRetrieveUpdateDestroy.as_view(), name='product_detail')
]
