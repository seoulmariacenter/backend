from rest_framework import serializers
from rest_framework.settings import api_settings

from .models import Product, Date, Schedule


class ProductSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=100)
    start_time = serializers.DateField(format=api_settings.DATE_FORMAT)
    end_time = serializers.DateField()
    price = serializers.CharField(max_length=10)
    publish = serializers.BooleanField(default=False)
    image = serializers.ImageField(allow_empty_file=True, allow_null=True)

    class Meta:
        model = Product
        fields = (
            'pk',
            'title',
            'start_time',
            'end_time',
            'price',
            'publish',
            'description',
            'image'
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


class DateField(serializers.RelatedField):
    queryset = Date.objects.all()

    def to_internal_value(self, data):
        return self.queryset.filter(product_id=data[0]).get(date_num=data[1])

    def to_representation(self, value):
        return value.date_num


class ScheduleSerializer(serializers.ModelSerializer):
    place = serializers.CharField(max_length=30, allow_blank=True)
    description = serializers.CharField()
    date = DateField()
    transport = serializers.CharField(max_length=10, allow_blank=True)
    time = serializers.CharField(max_length=10, allow_blank=True)

    class Meta:
        model = Schedule
        fields = (
            'pk',
            'place',
            'description',
            'date',
            'transport',
            'time',
        )
