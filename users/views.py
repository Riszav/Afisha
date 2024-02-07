from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from .serializers import UserCreateSerializer, UserAuthSerializer
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from django.shortcuts import redirect
from .models import ConfirmCode
from django.conf import settings
from django.core.mail import send_mail
from rest_framework.views import APIView


class RegistrationCreateApiView(APIView):
    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data='We send code on your email, go to link in message and enter code. '
                             'If the message didn`t arrive, check if you wrote your email correctly',
                        status=status.HTTP_201_CREATED)


class ConfirmCreateApiView(APIView):
    def post(self, request):
        code = request.data.get('code')
        try:
            confirm_code = ConfirmCode.objects.get(code=code)
            if confirm_code.is_expired():
                return Response(data={"error": "Confirmation code has expired. Please register again."}, status=400)
            user = confirm_code.user
            user.is_active = True
            user.save()
            return Response(data={"message": "User successfully confirmed."}, status=200)
        except ConfirmCode.DoesNotExist:
            return Response(data={"error": "Invalid confirmation code."}, status=400)


class AuthorizationCreateApiView(APIView):
    def post(self, request):
        serializer = UserAuthSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(**serializer.validated_data)
        if user:
            # 1-Вариант---------------------------
            # try:
            #     token = Token.objects.get(user=user)
            # except:
            #     token = Token.objects.create(user=user)
            # 2-Вариант---------------------------
            token, _ = Token.objects.get_or_create(user=user)
            return Response(data={'key': token.key})
        return Response(status=status.HTTP_401_UNAUTHORIZED)



@api_view(['POST'])
def registration_api_view(request):
    serializer = UserCreateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    username = serializer.validated_data.get('username')
    email = serializer.validated_data.get('email')
    password = serializer.validated_data.get('password')

    user = User.objects.create_user(username=username, email=email, password=password, is_active=False)
    confirm_code = ConfirmCode.objects.create(user=user)
    confirm_code.generate()
    confirm_code.save()
    # user.confirm_code = confirm_code.code
    send_mail('Code for confirm of user', f'Use this code ({confirm_code.code}). Input this in this url: http://127.0.0.1:8000/api/v1/users/confirm/', settings.EMAIL_HOST_USER, [email])
    return Response(data='We send code on your email, go to link in message and enter code. '
                         'If the message didn`t arrive, check if you wrote your email correctly', status=status.HTTP_201_CREATED)


@api_view(['POST'])
def confirm_api_view(request):
    code = request.data.get('code')
    try:
        confirm_code = ConfirmCode.objects.get(code=code)
        if confirm_code.is_expired():
            return Response(data={"error": "Confirmation code has expired. Please register again."}, status=400)
        user = confirm_code.user
        user.is_active = True
        user.save()
        return Response(data={"message": "User successfully confirmed."}, status=200)
    except ConfirmCode.DoesNotExist:
        return Response(data={"error": "Invalid confirmation code."}, status=400)

@api_view(['POST'])
def authorization_api_view(request):
    serializer = UserAuthSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    user = authenticate(**serializer.validated_data)
    if user:
        # 1-Вариант---------------------------
        # try:
        #     token = Token.objects.get(user=user)
        # except:
        #     token = Token.objects.create(user=user)
        # 2-Вариант---------------------------
        token, _ = Token.objects.get_or_create(user=user)
        return Response(data={'key': token.key})
    return Response(status=status.HTTP_401_UNAUTHORIZED)