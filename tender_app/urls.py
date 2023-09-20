from django.urls import path
from .views import *

urlpatterns = [
    path('basic_registration', BasicRegistrationApiView.as_view(), name='basic_registration_url'),
    path('bundles', BundleListApiView.as_view(), name='bundles_url'),
    path('cities', CityListApiView.as_view(), name='cities_url'),
    path('email_check', EmailCheckApiView.as_view(), name='email_check_url'),
    path('get_info', GetInfoApiView.as_view(), name='get_info_url'),
    path('is_registered', IsRegisteredApiView.as_view(), name='is_registered_url'),
    path('log_in', LogInApiView.as_view(), name='log_in_url'),
    path('log_out', LogOutApiView.as_view(), name='log_out_url'),
    path('sections', SectionListApiView.as_view(), name='sections_url'),
    path('subsections', SubSectionListApiView.as_view(), name='subsections_url'),
    path('worker_feedbacks', WorkerFeedbacksApiView.as_view(), name='worker_feedbacks_url'),
]
