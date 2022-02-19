from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

User = get_user_model()

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