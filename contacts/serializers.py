from rest_framework import serializers
from .models import Contact


class MetaPagesSerializer(serializers.Serializer):
    page = serializers.IntegerField(required=True)
    page_size = serializers.IntegerField(required=True)
    total = serializers.IntegerField(required=True)
    page_count = serializers.IntegerField(required=True)


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['first_name', 'last_name', 'phone', 'email']

    def validate_phone(self, value):
        if not value.startswith('+7'):
            raise serializers.ValidationError("Номер телефона должен начинаться с +7")
        return value
