from  django.shortcuts import render



def student_dashboard(request):
    return render(request, "student_dashboard.html")


def olimpiada(request):
    return render(request, "olimpiada.html")


def student_profile(request):
    return render(request, "student_profile.html")