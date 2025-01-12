from django.urls import path
from .views import (
    ScienceListView, QuizListView, SubmitQuizResultView,
    ScienceCreateAPIView, ScienceUpdateAPIView, ScienceDestroyAPIView
)

urlpatterns = [






    ############################ Science   #################################
    path('science/create/', ScienceCreateAPIView.as_view(), name='science-create'),
    path('science/update/<int:pk>/', ScienceUpdateAPIView.as_view(), name='science-update'),
    path('science/delete/<int:pk>/', ScienceDestroyAPIView.as_view(), name='science-delete'),

    ############################ APP MAIN #################################
    path('sciences/list/', ScienceListView.as_view(), name='science-list'),
    path('quizzes/<int:science_id>/', QuizListView.as_view(), name='quiz-list'),
    path('submit-quiz-result/', SubmitQuizResultView.as_view(), name='submit-quiz-result'),
]
