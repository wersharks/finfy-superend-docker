from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from bank.models import DepositType, InvestmentType

User = get_user_model()
class ChoiceField(serializers.ChoiceField):
    def to_representation(self, obj):
        if obj == '' and self.allow_blank:
            return obj
        return self._choices[obj]

    def to_internal_value(self, data):
        # To support inserts with the value
        if data == '' and self.allow_blank:
            return ''

        for key, val in self._choices.items():
            if val == data:
                return key
        self.fail('invalid_choice', input=data)

class DepositSerializer(serializers.Serializer):
    amount = serializers.IntegerField()
    inves_type = ChoiceField(choices=[(tag, tag.value) for tag in InvestmentType])
    # inves_type = serializers.CharField()

    class Meta:
        fields = (
            "amount",
            "inves_type",
        )


class IDSerializer(serializers.Serializer):
    id = serializers.IntegerField()

class RegisterSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password','password1',  'user_type',)

    def validate(self, attr):
        validate_password(attr['password'])
        return attr

    def create(self, validated_data):
            user = User.objects.create(
                username=validated_data['email'],
                user_type=validated_data['user_type'],
                email=validated_data['email'],
                first_name=validated_data['first_name'],
                last_name=validated_data['last_name'],

                )
            user.set_password(validated_data['password'])
            user.save()

            return user