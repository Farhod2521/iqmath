from  django.shortcuts import render
from app_quiz.models import Science


def student_dashboard(request):
    return render(request, "student_dashboard.html")


def olimpiada(request):
    # Retrieve all Science objects from the database
    science_objects = Science.objects.all()

    # Pass the science objects to the template
    return render(request, "olimpiada.html", {"science_objects": science_objects})


def student_profile(request):
    return render(request, "student_profile.html")



def login(request):
    return render(request, "login.html")


def sms_code(request):
    return render(request, "sms_code.html")

def quiz_student(request, id):
    print(id)
    return render(request, "quiz_student.html")

def result_student(request):
    return render(request, "result_student.html")





################################   TEACHERS #########################################
def  teachers_dashboard(request):
    return render(request, "teacher_dashoard.html")


def  students_ball_teacher(request):
    return render(request, "student_ball.html")