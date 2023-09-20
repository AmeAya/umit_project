from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import *
from django.contrib.auth import authenticate, login, logout
from .serializers import *
from .models import *
from .functions import *
import requests


class BasicRegistrationApiView(APIView):
    permission_classes = [AllowAny, ]

    def post(self, request):
        required_fields = ['email', 'password1', 'password2', 'type']
        for field in required_fields:
            if field not in request.data.keys():
                return Response({'message': field.capitalize() + ' is required!'}, status=status.HTTP_400_BAD_REQUEST)
        if request.data['type'] not in ['company', 'worker']:
            return Response({'message': 'Type must be "company" or "worker"!'}, status=status.HTTP_400_BAD_REQUEST)
        if request.data['password1'] != request.data['password2']:
            return Response({'message': 'Passwords didn`t match!'}, status=status.HTTP_400_BAD_REQUEST)
        user = CustomUser(email=request.data['email'].lower(), type=request.data['type'])
        user.set_password(request.data['password1'])
        user.save()
        return Response({'message': 'User is created!', 'email': user.email}, status=status.HTTP_201_CREATED)


class BundleListApiView(APIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = BundleSerializer

    def get(self, request):
        query = Bundle.objects.all()
        return Response(data=BundleSerializer(query, many=True).data, status=status.HTTP_200_OK)


class CityListApiView(APIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = CitySerializer

    def get(self, request):
        query = City.objects.all()
        return Response(data=CitySerializer(query, many=True).data, status=status.HTTP_200_OK)


class EmailCheckApiView(APIView):
    permission_classes = [AllowAny, ]

    def get(self, request):
        email = request.GET.get('email').lower()
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
        email_code = EmailCode.objects.filter(email=request.data['email'].lower()).latest('id')
        if email_code.code == str(request.data['code']):
            email_code.delete()
            return Response({'message': 'Email is confirmed!'}, status=status.HTTP_200_OK)
        return Response({'message': 'Code is not valid!'}, status=status.HTTP_400_BAD_REQUEST)


class GetInfoApiView(APIView):
    permission_classes = [AllowAny, ]

    def get(self, request):
        if 'bin' not in request.GET.keys():
            return Response({'message': 'BIN/IIN is required!'}, status=status.HTTP_400_BAD_REQUEST)
        if 'type' not in request.GET.keys():
            return Response({'message': 'Type is required!'}, status=status.HTTP_400_BAD_REQUEST)
        if request.GET.get('type') not in ['worker', 'company']:
            return Response({'message': 'Type must be "company" or "worker"'}, status=status.HTTP_400_BAD_REQUEST)
        url = 'https://old.stat.gov.kz/api/juridical/counter/api/'
        params = {
            'bin': request.GET.get('bin'),
            'lang': 'ru'
        }
        response = requests.get(url, params).json()
        if response['success']:
            data = {
                'message': 'Data received!',
                'info': getInfoSerializer(response['obj'], request.GET.get('type')),
                'flag': True,
            }
        else:
            data = {
                'message': 'Data is not received!',
                'flag': False,
            }
        return Response(data=data, status=status.HTTP_200_OK)


class IsRegisteredApiView(APIView):
    permission_classes = [AllowAny, ]

    def get(self, request):
        email = request.GET.get('email').lower()
        if email is None:
            return Response({'message': 'Email is required!'}, status=status.HTTP_400_BAD_REQUEST)
        if CustomUser.objects.filter(email=email):
            return Response({'message': 'This email already exists!', 'flag': True}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'This email doesn`t exists!', 'flag': False}, status=status.HTTP_200_OK)


class LogInApiView(APIView):
    permission_classes = [AllowAny, ]

    def post(self, request):
        if 'email' not in request.data.keys():
            return Response({'message': 'Email is required!'}, status=status.HTTP_400_BAD_REQUEST)
        if 'password' not in request.data.keys():
            return Response({'message': 'Password is required!'}, status=status.HTTP_400_BAD_REQUEST)
        user = authenticate(username=request.data['email'].lower(), password=request.data['password'])
        if not user:
            return Response({'message': 'Login and/or password is not valid'}, status=status.HTTP_403_FORBIDDEN)
        login(request, user)
        return Response({'message': 'User is logged in!'}, status=status.HTTP_202_ACCEPTED)


class LogOutApiView(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request):
        logout(request)
        return Response({'message': 'User is logged out!'}, status=status.HTTP_200_OK)


class SectionListApiView(APIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = SectionSerializer

    def get(self, request):
        query = Section.objects.all()
        return Response(data=SectionSerializer(query, many=True).data, status=status.HTTP_200_OK)

    def post(self, request):
        pass


class SubSectionListApiView(APIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = SubSectionSerializer

    def get(self, request):
        query = Section.objects.all()
        return Response(data=SubSectionSerializer(query, many=True).data, status=status.HTTP_200_OK)


class WorkerFeedbacksApiView(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        if 'id' not in request.GET.keys():
            return Response({'message': 'Id is required!'}, status=status.HTTP_400_BAD_REQUEST)
        query = Worker.objects.get(id=request.GET.get('id'))
        return Response(data=FeedbackSerializer(query.feedbacks.all(), many=True).data, status=status.HTTP_200_OK)
