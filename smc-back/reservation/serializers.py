from rest_framework import serializers

from .models import ReservationHost


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReservationHost
        fields = (
            'pk',
            'product',
            'username',
            'phone_number',
            'gender',
            'is_active'
        )
