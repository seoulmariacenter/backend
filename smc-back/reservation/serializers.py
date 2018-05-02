from rest_framework import serializers

from .models import ReservationHost, ReservationMember


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReservationHost
        fields = (
            'pk',
            'product',
            'username',
            'christian_name',
            'phone_number',
            'gender',
            'is_active',
            'date_joined',
            'date_canceled',
        )


class ReservationMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReservationMember
        fields = (
            'pk',
            'host',
            'name',
            'christian_name',
            'phone_number',
            'gender',
            'is_adult'
        )
