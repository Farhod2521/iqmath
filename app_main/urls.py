from django.urls import path


from .views import (
student_dashboard, olimpiada, student_profile, 
login, sms_code, teachers_dashboard, quiz_student, result_student, students_ball_teacher, teacher_login, teacher_quiz_add,
question_teacher,
)

urlpatterns = [
    path("student_dashboard/", student_dashboard, name="student_dashboard"),
    path("olimpiada/", olimpiada, name="olimpiada"),
    path("student_profile/", student_profile, name="student_profile"),
    path("login/", login, name="login"),
    path("sms_code/", sms_code, name="sms_code"),
    path("quiz_student/<int:id>/", quiz_student, name="quiz_student"),
    path("result_student/", result_student, name="result_student"),










    ###################################  TEACHERS ##########################################
    path("teachers_dashboard/", teachers_dashboard, name="teachers_dashboard"),
    path("students_balls/", students_ball_teacher, name="students_ball_teacher"),
    path("teacher_login/", teacher_login, name="teacher_login"),
    path("teacher_quiz_add/", teacher_quiz_add, name="teacher_quiz_add"),
    path("question_teacher/", question_teacher, name="question_teacher"),

]