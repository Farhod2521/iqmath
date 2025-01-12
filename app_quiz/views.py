from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Science, Quiz, Result
from .serializers import ScienceSerializer, QuizSerializer, ResultSerializer
from app_customer.models import Student
from rest_framework.permissions import IsAuthenticated
import jwt
from rest_framework.exceptions import AuthenticationFailed
import random

from rest_framework.generics import CreateAPIView, UpdateAPIView, DestroyAPIView








class ScienceCreateAPIView(CreateAPIView):
    queryset = Science.objects.all()
    serializer_class = ScienceSerializer


class ScienceUpdateAPIView(UpdateAPIView):
    queryset = Science.objects.all()
    serializer_class = ScienceSerializer
    lookup_field = 'pk'  


class ScienceDestroyAPIView(DestroyAPIView):
    queryset = Science.objects.all()
    serializer_class = ScienceSerializer
    lookup_field = 'pk' 








##########################                               ScienceListView                  ####################################################################
class ScienceListView(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request):
        sciences = Science.objects.all()
        serializer = ScienceSerializer(sciences, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class QuizListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, science_id):
        # Get quizzes based on the science_id
        score_1_quizzes = Quiz.objects.filter(science_id=science_id, score=2.1)
        score_2_quizzes = Quiz.objects.filter(science_id=science_id, score=3.1)
        score_3_quizzes = Quiz.objects.filter(science_id=science_id, score=5.1)

        # Randomly select quizzes based on the number required
        selected_score_1 = random.sample(list(score_1_quizzes), min(10, len(score_1_quizzes)))
        selected_score_2 = random.sample(list(score_2_quizzes), min(10, len(score_2_quizzes)))
        selected_score_3 = random.sample(list(score_3_quizzes), min(10, len(score_3_quizzes)))

        # Combine all selected quizzes
        selected_quizzes = selected_score_1 + selected_score_2 + selected_score_3

        # Serialize the selected quizzes
        serializer = QuizSerializer(selected_quizzes, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)



class SubmitQuizResultView(APIView):
    def post(self, request):
        token_header = request.headers.get('Authorization', '')
        if not token_header or not token_header.startswith('Bearer '):
            return Response({"error": "Authorization token missing or invalid"}, status=401)

        token = token_header.split(' ')[1]  # 'Bearer' ni olib tashlab, faqat tokenni olish

        try:
            # Imzoni tekshirmasdan faqat payloadni olish
            decoded_token = jwt.decode(token, options={"verify_signature": False})
            print("Decoded payload:", decoded_token)
        except jwt.DecodeError:
            return Response({"error": "Failed to decode token"}, status=401)

        student_id = decoded_token.get('student_id')
        if not student_id:
            raise AuthenticationFailed("No student ID found in token")

        try:
            student = Student.objects.get(id=student_id)
        except Student.DoesNotExist:
            return Response({"error": "Student not found"}, status=404)

        # Continue with quiz result processing
        quiz_id = request.data.get('quiz_id')
        answers = request.data.get('answers')
        end_time = request.data.get('end_time')

        if not quiz_id or not answers or not end_time:
            return Response({"error": "Missing required fields"}, status=400)

        try:
            quiz = Quiz.objects.get(id=quiz_id)
        except Quiz.DoesNotExist:
            return Response({"error": "Quiz not found"}, status=404)

        score = 0
        correct_answers = 0
        total_questions = len(answers)

        for answer_data in answers:
            quiz_answer = quiz.answer
            if answer_data['answer'] == quiz_answer:
                score += quiz.score
                correct_answers += 1

        result_data = {
            'student': student.id,
            'quiz': quiz.id,
            'science': quiz.science.id if quiz.science else None,
            'score': score,
            'total_questions': total_questions,
            'correct_answers': correct_answers,
            'end_time': end_time
        }

        result_serializer = ResultSerializer(data=result_data)

        if result_serializer.is_valid():
            result_serializer.save()
            return Response(result_serializer.data, status=201)

        return Response(result_serializer.errors, status=400)