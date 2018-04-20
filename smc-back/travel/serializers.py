from rest_framework import serializers
from rest_framework.settings import api_settings

from flight.models import Transport
from .models import Product, Date, Schedule


class Base64ImageField(serializers.ImageField):

    def to_internal_value(self, data):
        from django.core.files.base import ContentFile
        import base64
        import six
        import uuid

        if isinstance(data, six.string_types):
            if 'data:' in data and ';base64,' in data:
                header, data = data.split(';base64,')

            try:
                decoded_file = base64.b64decode(data)
            except TypeError:
                self.fail('invalid_image')

            file_name = str(uuid.uuid4())[:12]
            file_extension = self.get_file_extension(file_name, decoded_file, )

            complete_file_name = f'{file_name}.{file_extension}'

            data = ContentFile(decoded_file, name=complete_file_name)

        return super(Base64ImageField, self).to_internal_value(data)

    def get_file_extension(self, file_name, decoded_file):
        import imghdr

        extension = imghdr.what(file_name, decoded_file)
        extension = "jpg" if extension == "jpeg" else extension

        return extension


class ProductSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=100)
    start_time = serializers.DateField(format=api_settings.DATE_FORMAT)
    end_time = serializers.DateField()
    price = serializers.CharField(max_length=10)
    publish = serializers.BooleanField(default=False)
    image = Base64ImageField(allow_empty_file=True, allow_null=True)

    class Meta:
        model = Product
        fields = (
            'pk',
            'title',
            'start_time',
            'end_time',
            'price',
            'publish',
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


class TransportField(serializers.RelatedField):
    queryset = Transport.objects.all()

    def to_internal_value(self, data):
        return self.queryset.get(pk=data)

    def to_representation(self, value):
        return value.flight_code


class ScheduleSerializer(serializers.ModelSerializer):
    place = serializers.CharField(max_length=30, allow_blank=True)
    description = serializers.CharField(allow_blank=True)
    date = DateField()
    transport = TransportField()

    class Meta:
        model = Schedule
        fields = (
            'pk',
            'place',
            'description',
            'date',
            'transport',
        )
