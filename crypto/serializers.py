from django.forms import CharField
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from bank.models import DepositType, InvestmentType


class BuyCryptoSerializer(serializers.Serializer):
    amount = serializers.IntegerField()
    crypto_symbol = CharField()
    # inves_type = serializers.CharField()

    class Meta:
        fields = (
            "amount",
            "crypto_symbol",
        )