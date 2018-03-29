from rest_framework import serializers
from rest_framework.settings import api_settings

from .models import Product, Date


class ProductSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=100)
    start_time = serializers.DateField(format=api_settings.DATE_FORMAT)
    end_time = serializers.DateField()
    price = serializers.CharField(max_length=10)
    dates = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Product
        fields = (
            'pk',
            'title',
            'start_time',
            'end_time',
            'price',
            'dates',
        )


class ProductField(serializers.RelatedField):
    queryset = Product.objects.all()

    def to_internal_value(self, data):
        return self.queryset.get(pk=data)

    def to_representation(self, value):
        return value.title


class DateSerializer(serializers.ModelSerializer):
    date_num = serializers.IntegerField()
    date_time = serializers.DateField(format=api_settings.DATE_FORMAT)
    product = ProductField()

    class Meta:
        model = Date
        fields = (
            'date_num',
            'date_time',
            'product',
        )
