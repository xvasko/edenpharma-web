from rest_framework import serializers

from core.models import Customer


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['name', 'city', 'phone_number', 'street', 'zip']



