from django.urls import path


from .views import (
student_dashboard, olimpiada, student_profile, 
login, sms_code, teachers_dashboard, quiz_student
)

urlpatterns = [
    path("student_dashboard/", student_dashboard, name="student_dashboard"),
    path("olimpiada/", olimpiada, name="olimpiada"),
    path("student_profile/", student_profile, name="student_profile"),
    path("login/", login, name="login"),
    path("sms_code/", sms_code, name="sms_code"),
    path("quiz_student/", quiz_student, name="quiz_student"),










    ###################################  TEACHERS ##########################################
    path("teachers_dashboard/", teachers_dashboard, name="teachers_dashboard"),

]