from django.urls import path
from .views import *

urlpatterns = [
    path('email_check', EmailCheckApiView.as_view(), name='email_check_url'),
    path('log_in', LogInApiView.as_view(), name='log_in_url'),
    path('log_out', LogOutApiView.as_view(), name='log_out_url'),
]
