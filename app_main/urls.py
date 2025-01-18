from django.urls import path


from .views import student_dashboard, olimpiada, student_profile, login, sms_code


urlpatterns = [
    path("", student_dashboard, name="student_dashboard"),
    path("olimpiada/", olimpiada, name="olimpiada"),
    path("student_profile/", student_profile, name="student_profile"),
    path("login/", login, name="login"),
    path("sms_code/", sms_code, name="sms_code"),
]