from django.urls import path
from .views import *

urlpatterns = [
    path('basic_registration', BasicRegistrationApiView.as_view(), name='basic_registration_url'),
    path('email_check', EmailCheckApiView.as_view(), name='email_check_url'),
    path('log_in', LogInApiView.as_view(), name='log_in_url'),
    path('log_out', LogOutApiView.as_view(), name='log_out_url'),
]
