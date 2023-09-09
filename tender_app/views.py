from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import *
from django.contrib.auth import authenticate, login, logout
from .models import *
from .functions import *


class EmailCheckApiView(APIView):
    permission_classes = [AllowAny, ]

    def get(self, request):
        email = request.GET.get('email')
        if email is None:
            return Response({'message': 'Email is required!'}, status=status.HTTP_400_BAD_REQUEST)
        import random
        code = str(random.randint(10**5, 10**6))
        EmailCode(email=email, code=code).save()
        sendEmail(email, code)
        return Response({'message': 'Email sent!'}, status=status.HTTP_200_OK)

    def post(self, request):
        if 'email' not in request.data.keys():
            return Response({'message': 'Email is required!'}, status=status.HTTP_400_BAD_REQUEST)
        if 'code' not in request.data.keys():
            return Response({'message': 'Code is required!'}, status=status.HTTP_400_BAD_REQUEST)
        email_code = EmailCode.objects.filter(email=request.data['email']).latest('id')
        if email_code.code == str(request.data['code']):
            email_code.delete()
            return Response({'message': 'Email is confirmed!'}, status=status.HTTP_200_OK)
        return Response({'message': 'Code is not valid!'}, status=status.HTTP_400_BAD_REQUEST)


class LogInApiView(APIView):
    permission_classes = [AllowAny, ]

    def post(self, request):
        if 'email' not in request.data.keys():
            return Response({'message': 'Email is required!'}, status=status.HTTP_400_BAD_REQUEST)
        if 'password' not in request.data.keys():
            return Response({'message': 'Password is required!'}, status=status.HTTP_400_BAD_REQUEST)
        user = authenticate(username=request.data['email'], password=request.data['password'])
        if not user:
            return Response({'message': 'Login and/or password is not valid'}, status=status.HTTP_403_FORBIDDEN)
        login(request, user)
        return Response({'message': 'User is logged in!'}, status=status.HTTP_202_ACCEPTED)


class LogOutApiView(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        logout(request)
        return Response({'message': 'User is logged out!'}, status=status.HTTP_200_OK   )
