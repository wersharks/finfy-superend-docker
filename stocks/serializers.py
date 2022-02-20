from django.forms import CharField
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password


class StockActionSerializer(serializers.Serializer):
    amount = serializers.IntegerField()
    stock_symbol = serializers.CharField()

    class Meta:
        fields = (
            "amount",
            "stock_symbol",
        )