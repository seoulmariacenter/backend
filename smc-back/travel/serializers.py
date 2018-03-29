from rest_framework import serializers
from rest_framework.settings import api_settings

from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=100)
    start_time = serializers.DateField(format=api_settings.DATE_FORMAT)
    end_time = serializers.DateField()
    price = serializers.CharField(max_length=10)

    class Meta:
        model = Product
        fields = (
            'pk',
            'title',
            'start_time',
            'end_time',
            'price',
        )
