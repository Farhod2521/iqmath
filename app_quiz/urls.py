from django.urls import path
from .views import (
    ScienceListView, QuizListView, ResultCreateAPIView,
    ScienceCreateAPIView, ScienceUpdateAPIView, ScienceDestroyAPIView,
    QuizCreateAPIView, Result_Telegram_Bot_CreateVIEW, Result_Telegram_Bot_ListView, 
    Get_Student_Result_By_TelegramID, ResultListView, Results_ALL_View, Results_EXAM_View,
    Pass_Exam_UpdateResultStatusAPIView, Results_Add_View,UpdatePassExamStudentAPIView

)

urlpatterns = [


    #################################     RESULT      ####################
    path('result_all/', Results_ALL_View.as_view(), name='result_all'),
    path('result_pass_exam/', Results_EXAM_View.as_view(), name='result_pass_exam'),
    path('result_pass_exam_status/', Pass_Exam_UpdateResultStatusAPIView.as_view(), name='result_pass_exam'),
    path('result_add_student/', Results_Add_View.as_view(), name='result_pass_exam'),
    path('result_filter_student_count/<int:pk>/', UpdatePassExamStudentAPIView.as_view(), name='result_pass_exam'),

    #################################     TELEGRAM     ####################
    path('telegram_user/create/', Result_Telegram_Bot_CreateVIEW.as_view(), name='telegram_user'),
    path('telegram_user/list/check/', Result_Telegram_Bot_ListView.as_view(), name='telegram_user'),
    path('telegram_user/result/', Get_Student_Result_By_TelegramID.as_view(), name='telegram_user'),


    ############################ Science   #################################
    path('science/create/', ScienceCreateAPIView.as_view(), name='science-create'),
    path('science/update/<int:pk>/', ScienceUpdateAPIView.as_view(), name='science-update'),
    path('science/delete/<int:pk>/', ScienceDestroyAPIView.as_view(), name='science-delete'),

    ############################ APP MAIN #################################
    path('sciences/list/', ScienceListView.as_view(), name='science-list'),
    path('quizzes/<int:science_id>/', QuizListView.as_view(), name='quiz-list'),
    path('submit-quiz-result/', ResultCreateAPIView.as_view(), name='submit-quiz-result'),
    path('quiz/add/', QuizCreateAPIView.as_view(), name='submit-quiz-result'),
    path('result/list/', ResultListView.as_view(), name='submit-quiz-result'),
    path('result/list/', ResultListView.as_view(), name='submit-quiz-result'),
]
