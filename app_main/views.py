from  django.shortcuts import render



def student_dashboard(request):
    return render(request, "student_dashboard.html")


def olimpiada(request):
    return render(request, "olimpiada.html")


def student_profile(request):
    return render(request, "student_profile.html")



def login(request):
    return render(request, "login.html")


def sms_code(request):
    return render(request, "sms_code.html")

def quiz_student(request):
    return render(request, "quiz_student.html")






################################   TEACHERS #########################################
def  teachers_dashboard(request):
    return render(request, "teacher_dashoard.html")