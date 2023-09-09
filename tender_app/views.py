from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .functions import *


class EmailCheckApiView(APIView):
    permission_classes = []

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

