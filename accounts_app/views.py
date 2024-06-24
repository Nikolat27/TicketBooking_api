from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from . import serializers
from .models import User


# Create your views here.

class UserRegisterView(APIView):
    def post(self, request):
        if request.user.is_authenticated:
            username = request.data.get("username")
            email = request.data.get("email")
            pass1 = request.data.get("pass1")
            pass2 = request.data.get("pass2")

            if not username or email or pass1 and pass2:
                return Response(
                    {"response": "Please Provide all the required fields", "status": status.HTTP_400_BAD_REQUEST})

            if pass1 != pass2:
                return Response({"response": "Your passwords are not matched", "status": status.HTTP_400_BAD_REQUEST})

            if User.objects.filter(username=username).exists():
                return Response({"response": "This username exists", "status": status.HTTP_400_BAD_REQUEST})

            if User.objects.filter(email=email).exists():
                return Response({"response": "This email exists", "status": status.HTTP_400_BAD_REQUEST})

            User.objects.create_user(username=username, email=email, password=pass1)
            return Response({"response": "User created successfully", "status": status.HTTP_200_OK})


class UserLogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh_token")
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
