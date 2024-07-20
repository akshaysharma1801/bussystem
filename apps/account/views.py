from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.contrib.auth.models import User
from .serializer import (
    RegisterSerializer, LoginSerializer,
    LoginUserDetailSerializer
)
from rest_framework import status
from django.contrib.auth import authenticate, login, logout

class LoginView(APIView):

    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(
                username=serializer.data.get('email').lower(),
                password=serializer.data.get('password'),
            )
            if user is not None:
                login(request, user)
                serializer = LoginUserDetailSerializer(user)
                return Response({
                    'success':True,
                    'data':serializer.data,
                    'message':'Login Successfully'
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'success':False,
                    'detail': "Invalid Username or password."
                },status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors)
    
class RegisterView(APIView):

    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)