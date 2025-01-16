from django.urls import path
from .views import (
    ScienceListView, QuizListView, ResultCreateAPIView,
    ScienceCreateAPIView, ScienceUpdateAPIView, ScienceDestroyAPIView,
    QuizCreateAPIView, Result_Telegram_Bot_CreateVIEW
)

urlpatterns = [



    path('telegram_user/create/', Result_Telegram_Bot_CreateVIEW.as_view(), name='telegram_user'),


    ############################ Science   #################################
    path('science/create/', ScienceCreateAPIView.as_view(), name='science-create'),
    path('science/update/<int:pk>/', ScienceUpdateAPIView.as_view(), name='science-update'),
    path('science/delete/<int:pk>/', ScienceDestroyAPIView.as_view(), name='science-delete'),

    ############################ APP MAIN #################################
    path('sciences/list/', ScienceListView.as_view(), name='science-list'),
    path('quizzes/<int:science_id>/', QuizListView.as_view(), name='quiz-list'),
    path('submit-quiz-result/', ResultCreateAPIView.as_view(), name='submit-quiz-result'),
    path('quiz/add/', QuizCreateAPIView.as_view(), name='submit-quiz-result'),
]
