from django.urls import path
from .views import RegisterStudentAPIView, VerifySmsCodeAPIView, LoginAPIView, StudentProfileAPIView

urlpatterns = [
    path('register/', RegisterStudentAPIView.as_view(), name='register_student'),
    path('verify-sms/', VerifySmsCodeAPIView.as_view(), name='verify_sms'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('profile/', StudentProfileAPIView.as_view(), name='profile'),
]



