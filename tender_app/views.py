from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import *
from django.contrib.auth import authenticate, login, logout
from .serializers import *
from .models import *
from .functions import *


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
        user = CustomUser(email=request.data['email'], type=request.data['type'])
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


class CompanyCreateApiView(APIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = CompanySerializer

    def post(self, request):
        company = Company(user=request.user, name=request.data['name'], bin=request.data['bin'],
                          address=request.data['address'], face=request.data['face'],
                          face_phone=request.data['face_phone'], favourites=request.data['favourites'],
                          requisites=request.data['requisites'], license=request.data['license'],
                          gos_reg=request.data['gos_reg'])
        company.save()


class CompanyDetailAPIView(APIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = CompanySerializer

    def get(self, request):
        query = Company.objects.get(id=request.GET.get('id'))
        return Response(data=CompanySerializer(query).data, status=status.HTTP_200_OK)

    def post(self, request):
        company = Company.objects.get(id=request.GET.get('id'))
        query = Tender.objects.filter(author=company)
        return Response(data=TenderFilterSerializer(query, many=True).data, status=status.HTTP_200_OK)


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

    def post(self, request):
        logout(request)
        return Response({'message': 'User is logged out!'}, status=status.HTTP_200_OK)


class SectionListApiView(APIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = SectionSerializer

    def get(self, request):
        query = Section.objects.all()
        return Response(data=SectionSerializer(query, many=True).data, status=status.HTTP_200_OK)


class SubSectionListApiView(APIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = SubSectionSerializer

    def get(self, request):
        query = Subsection.objects.all()
        return Response(data=SubSectionSerializer(query, many=True).data, status=status.HTTP_200_OK)


class TenderListApiView(APIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = TenderFilterSerializer
    filterset_fields = ['city', 'types_of_work', 'budget', 'author']

    def get(self, request):
        query = Tender.objects.filter(is_active=True)
        return Response(data=TenderFilterSerializer(query, many=True).data, status=status.HTTP_200_OK)

    def post(self, request):
        author = Company.objects.get(user=request.user)
        tender = Tender(author=author, city=request.data['city'], types_of_work =request.data['types_of_work '],
                        expired_date=request.data['expired_date'], budget=request.data['budget'],
                        description=request.data['description'], docs=request.data['docs'])
        tender.save()
        return Response(data='Tender create', status=status.HTTP_201_CREATED)


class WorkerDetailApiView(APIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = WorkerDetailSerializer

    def get(self, request):
        query = Worker.objects.get(id=request.GET.get('id'))
        return Response(data=WorkerDetailSerializer(query).data, status=status.HTTP_200_OK)


class WorkerCreateApiView(APIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = WorkerSerializer

    def post(self, request):
        worker = Worker(user=request.user, name=request.data['name'], bin=request.data['bin'],
                        description=request.data['description'], director=request.data['director'],
                        phone=request.data['phone'], rating=request.data['rating'], cities=request.data['cities'],
                        types_of_work=request.data['types_of_work'], docs=request.data['docs'])
        worker.save()
