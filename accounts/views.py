from django.contrib.auth import authenticate
from .serializers import SignUpSerializer, UserSerializer
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema


class SignUpView(generics.GenericAPIView):
    serializer_class = SignUpSerializer

    @swagger_auto_schema(request_body=SignUpSerializer, tags=['Signup/Login'])
    def post(self, request: Request):
        data = request.data

        serializer = self.serializer_class(data=data)

        if serializer.is_valid():
            serializer.save()

            response = {
                "message": "User Created Successfully",
                "data": serializer.data
            }

            return Response(data=response, status=status.HTTP_201_CREATED)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):

    @swagger_auto_schema(request_body=UserSerializer, tags=['Signup/Login'])
    def post(self, request: Request):
        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(email=email, password=password)

        if user:
            response = {
                "message": "Login Successful",
                "token": user.auth_token.key
            }
            return Response(data=response, status=status.HTTP_200_OK)
        else:
            return Response(data={"message": "Invalid username or password"},
                            status=status.HTTP_401_UNAUTHORIZED)

    @swagger_auto_schema(tags=['Signup/Login'])
    def get(self, request: Request):
        content = {
            "user": str(request.user),
            "auth": str(request.auth)
        }

        return Response(data=content, status=status.HTTP_200_OK)
