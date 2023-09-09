from django.urls import path
from .views import *

urlpatterns = [
    path('email_check', EmailCheckApiView.as_view(), name='email_check_url'),
]
