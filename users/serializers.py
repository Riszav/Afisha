from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError
from users.models import ConfirmCode
from django.conf import settings
from django.core.mail import send_mail

class UserAuthSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class UserCreateSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField()


    def validate_username(self, username):
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise ValidationError('User already exists! Choose other username.')


    def create(self, validated_data):
        user = User.objects.create_user(**validated_data, is_active=False)  # username=username, email=email, password=password
        confirm_code = ConfirmCode.objects.create(user=user)
        confirm_code.generate()
        confirm_code.save()
        try:
            send_mail('Code for confirm of user',
                      f'Use this code ({confirm_code.code}). Input this in this url: http://127.0.0.1:8000/api/v1/users/confirm/',
                      settings.EMAIL_HOST_USER, [user.email])
        except:
            User.objects.get(username=user.username).delete()
            raise ValidationError('Код не отправлен! Не удалось создать пользователя')
        return user

