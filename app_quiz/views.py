from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Science, Quiz, Result, Result_Telegram_Bot
from .serializers import ScienceSerializer, QuizSerializer, ResultSerializer,Result_Telegram_Bot_Serializers, Quiz_Add_Serializers
from app_customer.models import Student
from rest_framework.permissions import IsAuthenticated
import jwt
from rest_framework.exceptions import AuthenticationFailed
import random

from rest_framework.generics import CreateAPIView, UpdateAPIView, DestroyAPIView





class Result_Telegram_Bot_CreateVIEW(CreateAPIView):
    queryset = Result_Telegram_Bot.objects.all()
    serializer_class  =  Result_Telegram_Bot_Serializers

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





class QuizCreateAPIView(CreateAPIView):
    queryset = Quiz.objects.all()
    serializer_class = Quiz_Add_Serializers


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

from datetime import datetime

class ResultCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        token_header = request.headers.get('Authorization', '')
        if not token_header or not token_header.startswith('Bearer '):
            return Response({"error": "Authorization token missing or invalid"}, status=401)

        token = token_header.split(' ')[1]  # 'Bearer' so'zini olib tashlab, faqat tokenni olish

        try:
            # Imzoni tekshirmasdan faqat payloadni olish
            decoded_token = jwt.decode(token, options={"verify_signature": False})
        except jwt.DecodeError:
            return Response({"error": "Failed to decode token"}, status=401)

        student_id = decoded_token.get('student_id')
        if not student_id:
            raise AuthenticationFailed("No student ID found in token")

        try:
            student = Student.objects.get(id=student_id)
        except Student.DoesNotExist:
            return Response({"error": "Student not found"}, status=404)

        data = request.data
        answers = data.get("answers", [])
        end_time_str = data.get("end_time")

        # Savollar bo'yicha natijani hisoblash
        total_questions = len(answers)
        correct_answers = 0
        total_score = 0
        science_set = set()

        for answer in answers:
            quiz_id = answer.get("quiz_id")
            user_answer = answer.get("answer")

            try:
                quiz = Quiz.objects.get(id=quiz_id)
                science_set.add(quiz.science)
                if quiz.answer == user_answer:
                    correct_answers += 1
                    total_score += quiz.score
            except Quiz.DoesNotExist:
                return Response({"error": f"Quiz with id {quiz_id} not found"}, status=status.HTTP_404_NOT_FOUND)

        # Science ni aniqlash (bitta fandan test bo'lishi kerak)
        if len(science_set) != 1:
            return Response({"error": "All questions must belong to the same science"}, status=status.HTTP_400_BAD_REQUEST)
        science = science_set.pop()

        # Urinishlar sonini aniqlash
        attempt_number = Result.objects.filter(student=student, science=science).count() + 1

        # End time ni datetime formatga o'zgartirish
        try:
            end_time = datetime.fromisoformat(end_time_str)
        except ValueError:
            return Response({"error": "Invalid end_time format. Use ISO format"}, status=status.HTTP_400_BAD_REQUEST)

        # Result obyektini yaratish
        result = Result.objects.create(
            student=student,
            quiz=quiz,  # Oxirgi ishlangan testni saqlaymiz
            science=science,
            score=total_score,
            total_questions=total_questions,
            correct_answers=correct_answers,
            attempt_number=attempt_number,
            end_time=end_time
        )
        result.calculate_status()
        result.calculate_test_time()

        # Natijani qaytarish
        response_data = {
            "student": student.id,
            "science": science.id,
            "score": total_score,
            "total_questions": total_questions,
            "correct_answers": correct_answers,
            "attempt_number": attempt_number,
            "test_time": result.test_time,
        }
        return Response(response_data, status=status.HTTP_201_CREATED)