from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Science, Quiz, Result, Result_Telegram_Bot, Pass_Exam_Student
from .serializers import (
    ScienceSerializer, QuizSerializer, ResultSerializer,Result_Telegram_Bot_Serializers, 
    Quiz_Add_Serializers, Result_Telegram_Serializers, Pass_Exam_ResultSerializer )
from app_customer.models import Student, User
from rest_framework.permissions import IsAuthenticated
import jwt
from rest_framework.exceptions import AuthenticationFailed
import random

from rest_framework.generics import CreateAPIView, UpdateAPIView, DestroyAPIView, ListAPIView

from datetime import datetime
import requests
from django.shortcuts import get_object_or_404



def format_test_time(test_time_str):
    try:
        # timedelta formatidagi vaqtni o'qish
        time_parts = test_time_str.split(":")
        hours, minutes, seconds = map(int, time_parts)
        total_seconds = hours * 3600 + minutes * 60 + seconds
        # Faqat MM:SS ko'rinishda formatlash
        minutes, seconds = divmod(total_seconds, 60)
        return f"{minutes:02}:{seconds:02}"
    except ValueError:
        raise ValueError("test_time must be in 'H:MM:SS' format.")









class QuizCreateAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = QuizSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Quiz muvaffaqiyatli yaratildi!", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class Get_Student_Result_By_TelegramID(APIView):
    def post(self, request, *args, **kwargs):
        telegram_id = request.data.get('telegram_id')
        
        if not telegram_id:
            return Response({"detail": "telegram_id is required"}, status=status.HTTP_400_BAD_REQUEST)
 
        try:
            result_bot = Result_Telegram_Bot.objects.get(telegram_id=telegram_id)
            phone = result_bot.phone
        except Result_Telegram_Bot.DoesNotExist:
            return Response("No Result_Telegram_Bot entry found for this telegram_id.")
        
        # Fetch the User with the given phone number
        try:
            user = User.objects.get(phone=phone)
        except User.DoesNotExist:
            return Response("User with this phone number not found.")
        
        # Fetch the Student associated with the User
        try:
            student = Student.objects.get(user=user)
        except Student.DoesNotExist:
            return Response("Student profile not found for this user.")
        
        # Fetch the latest result for this student
        latest_result = Result.objects.filter(student=student).order_by('-id').first()
        
        if not latest_result:
            return Response({"detail": "No results found for this student."}, status=status.HTTP_404_NOT_FOUND)
        
        # Serialize and return the latest result
        serializer = Result_Telegram_Serializers(latest_result)
        return Response(serializer.data, status=status.HTTP_200_OK)






class Result_Telegram_Bot_CreateVIEW(APIView):
    def post(self, request, *args, **kwargs):
        phone = request.data.get('phone')
        telegram_id = request.data.get('telegram_id')

        # Check if the phone exists in the User model
        try:
            user = User.objects.get(phone=phone)

        except User.DoesNotExist:
            return Response("Telfon raqam topilmadi !!!", status=status.HTTP_404_NOT_FOUND)


        result_bot = Result_Telegram_Bot.objects.create(phone=phone, telegram_id=telegram_id)
        serializer = Result_Telegram_Bot_Serializers(result_bot)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class Result_Telegram_Bot_ListView(APIView):
    def get(self, request):
        telegram_id = request.GET.get("telegram_id")

        if telegram_id:
            try:
                user = Result_Telegram_Bot.objects.get(telegram_id=telegram_id)
                serializer = Result_Telegram_Bot_Serializers(user)
                return Response({
                    "result": "success",
                    "data": serializer.data
                })
            except Result_Telegram_Bot.DoesNotExist:
                return Response("User with the given Telegram ID not found.", status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"error": "Telegram ID required."}, status=status.HTTP_400_BAD_REQUEST)

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







class ResultListView(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request):
        # Tokenni olish
        token_header = request.headers.get('Authorization', '')
        if not token_header or not token_header.startswith('Bearer '):
            return Response({"error": "Authorization token missing or invalid"}, status=status.HTTP_401_UNAUTHORIZED)

        token = token_header.split(' ')[1]
        try:
            # Tokenni dekodlash
            decoded_token = jwt.decode(token, options={"verify_signature": False})
        except jwt.DecodeError:
            return Response({"error": "Failed to decode token"}, status=status.HTTP_401_UNAUTHORIZED)

        # Token orqali studentni aniqlash
        student_id = decoded_token.get('student_id')
        if not student_id:
            raise AuthenticationFailed("No student ID found in token")

        # Studentni olish
        student = get_object_or_404(Student, id=student_id)

        # Eng oxirgi natijani olish
        result = Result.objects.filter(student=student).order_by('-id').first()

        if not result:
            return Response({"error": "No results found for this student"}, status=status.HTTP_404_NOT_FOUND)

        # Natija ma'lumotlarini olish
        result_data = {
            "science_name": result.science.name,  # Fan nomi
            "score": result.score,  # Ball
            "total_questions": result.total_questions,  # Jami savollar
            "correct_answers": result.correct_answers,  # To'g'ri javoblar
            "test_time": result.test_time,  # Vaqt (sekundlarda)
            "correct_questions": result.correct_questions,  # To'g'ri savollar (JSON)
            "incorrect_questions": result.incorrect_questions,  # Xato savollar (JSON)
        }

        # Response qaytarish
        return Response(result_data, status=status.HTTP_200_OK)










##########################                               ScienceListView                  ####################################################################
class ScienceListView(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request):
        sciences = Science.objects.all()
        serializer = ScienceSerializer(sciences, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class QuizListView(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request, science_id):
        # Get quizzes based on the science_id
        score_1_quizzes = Quiz.objects.filter(science_id=science_id, score=2.1)
        score_2_quizzes = Quiz.objects.filter(science_id=science_id, score=3.1)
        score_3_quizzes = Quiz.objects.filter(science_id=science_id, score=5.1)

        selected_score_1 = random.sample(list(score_1_quizzes), min(10, len(score_1_quizzes)))
        selected_score_2 = random.sample(list(score_2_quizzes), min(10, len(score_2_quizzes)))
        selected_score_3 = random.sample(list(score_3_quizzes), min(10, len(score_3_quizzes)))

        # Combine all selected quizzes
        selected_quizzes = selected_score_1 + selected_score_2 + selected_score_3

        # Serialize the selected quizzes
        serializer = QuizSerializer(selected_quizzes, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

from datetime import timedelta

class ResultCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Tokenni olish va tekshirish
        token_header = request.headers.get('Authorization', '')
        if not token_header or not token_header.startswith('Bearer '):
            return Response({"error": "Authorization token missing or invalid"}, status=status.HTTP_401_UNAUTHORIZED)

        token = token_header.split(' ')[1]

        try:
            # Imzoni tekshirmasdan tokenni ochish
            decoded_token = jwt.decode(token, options={"verify_signature": False})
        except jwt.DecodeError:
            return Response({"error": "Failed to decode token"}, status=status.HTTP_401_UNAUTHORIZED)

        # Studentni token orqali topish
        student_id = decoded_token.get('student_id')
        if not student_id:
            raise AuthenticationFailed("No student ID found in token")

        student = get_object_or_404(Student, id=student_id)

        # Foydalanuvchi kiritgan ma'lumotlar
        data = request.data
        answers = data.get("answers", [])
        test_time = data.get("test_time", 0)  # Test vaqti (sekundlarda)

        # Natija hisoblash uchun o'zgaruvchilar
        total_questions = len(answers)
        correct_answers = 0
        total_score = 0
        science_set = set()
        correct_questions = []
        incorrect_questions = []
        answer_more = []

        # Javoblarni qayta ishlash
        for index, answer in enumerate(answers, start=1):
            quiz_id = answer.get("quiz_id")
            user_answer = answer.get("answer")

            try:
                quiz = Quiz.objects.get(id=quiz_id)
                science_set.add(quiz.science)

                is_correct = quiz.answer == user_answer
                score = quiz.score if is_correct else 0

                if is_correct:
                    correct_answers += 1
                    total_score += quiz.score
                    correct_questions.append(quiz.id)
                else:
                    incorrect_questions.append(quiz.id)

                # Tartiblangan savollarni qo'shish
                answer_more.append({
                    "order": index,
                    "quiz_id": quiz_id,
                    "score": quiz.score,
                    "is_correct": is_correct
                })

            except Quiz.DoesNotExist:
                return Response({"error": f"Quiz with id {quiz_id} not found"}, status=status.HTTP_404_NOT_FOUND)

        # Fandagi savollarni tekshirish
        if len(science_set) != 1:
            return Response({"error": "All questions must belong to the same science"}, status=status.HTTP_400_BAD_REQUEST)
        science = science_set.pop()

        # Natija obyektini yaratish
        result = Result.objects.create(
            student=student,
            quiz=quiz,
            science=science,
            score=total_score,
            total_questions=total_questions,
            correct_answers=correct_answers,
            correct_questions=correct_questions,
            incorrect_questions=incorrect_questions,
            answer_more=answer_more,
            test_time=test_time
        )

        # Javob ma'lumotlarini qaytarish
        test_tim = (str(timedelta(seconds=int(result.test_time))))[2:7]
        response_data = {
            "student": student.id,
            "science": science.id,
            "score": total_score,
            "total_questions": total_questions,
            "correct_answers": correct_answers,
            "answer_more": answer_more,
            "test_time": test_tim,
        }
        return Response(response_data, status=status.HTTP_201_CREATED)




class Results_ALL_View(APIView):
    def get(self, request, *args, **kwargs):
        # Fetch all students
        students = Student.objects.all()
        data = []
        for student in students:
            results = Result.objects.filter(student=student)
            
            for result in results:
                test_tim = (str(timedelta(seconds=int(result.test_time))))[2:7]
                data.append({
                    "id": result.id,
                    "full_name": student.full_name,
                    "region": student.region,
                    "brithday": student.brithday,
                    "phone": student.user.phone,
                    "correct_answers": result.correct_answers,
                    "total_questions": result.total_questions,
                    "score": round(result.score, 1),
                    "test_time": test_tim,
                    "status_exam": result.status_exam,
                })

        return Response(data)
from django.db.models import Q
class Results_Add_View(APIView):
    def get(self, request, *args, **kwargs):
        students = Student.objects.all()
        data = []
        for student in students:
            results = Result.objects.filter(student=student).filter(
                           Q(status_exam__isnull=True) | Q(status_exam=False)
                                          )
            
            for result in results:
                test_tim = (str(timedelta(seconds=int(result.test_time))))[2:7]
                data.append({
                    "id": result.id,
                    "full_name": student.full_name,
                    "region": student.region,
                    "brithday": student.brithday,
                    "phone": student.user.phone,
                    "correct_answers": result.correct_answers,
                    "total_questions": result.total_questions,
                    "score": round(result.score, 1),
                    "test_time": test_tim,
                    "status_exam": result.status_exam,  # `status_exam` ham qo'shildi
                })

        return Response(data)

class Results_EXAM_View(APIView):
    def get(self, request, *args, **kwargs):
        # Fetch all students
        students = Student.objects.filter(status__in=[None, True])  # Exclude students with status=False
        data = []

        for student in students:
            results = Result.objects.filter(student=student).filter(
                           Q(status_exam__isnull=True) | Q(status_exam=False)
                                          )
            for result in results:
                test_tim = (str(timedelta(seconds=int(result.test_time))))[2:7]
                data.append({
                    "id": result.id,
                    "full_name": student.full_name,
                    "region": student.region,
                    "brithday": student.brithday,
                    "phone": student.user.phone,
                    "correct_answers": result.correct_answers,
                    "total_questions": result.total_questions,
                    "score": round(result.score, 1),
                    "test_time": test_tim,
                })

        sorted_data = sorted(data, key=lambda x: (-x["score"], x["test_time"]))

   
        pass_exam_count = Pass_Exam_Student.objects.first().count if Pass_Exam_Student.objects.exists() else 300


        return Response(sorted_data[:pass_exam_count])



class UpdatePassExamStudentAPIView(APIView):
    def get(self, request, pk, *args, **kwargs):
        # Modeldan kerakli obyektni olish
        student = get_object_or_404(Pass_Exam_Student, pk=pk)

        # Faqat `count` qiymatini qaytarish
        return Response({
            'count': student.count
        }, status=status.HTTP_200_OK)

    def put(self, request, pk, *args, **kwargs):
        # Modeldan kerakli obyektni olish
        student = get_object_or_404(Pass_Exam_Student, pk=pk)
        
        # Kiritilgan ma'lumotlarni olish
        new_count = request.data.get('count', None)
        
        if new_count is not None and isinstance(new_count, int) and new_count >= 0:
            # Ma'lumotlarni yangilash
            student.count = new_count
            student.save()
            return Response({
                'message': 'Count successfully updated!',
                'data': {
                    'id': student.id,
                    'count': student.count
                }
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'error': 'Invalid count value. It must be a positive integer.'
            }, status=status.HTTP_400_BAD_REQUEST)

    
class Pass_Exam_UpdateResultStatusAPIView(APIView):
    
    def patch(self, request):
        result_id = request.data.get('result_id')  # result_id ni body'dan olamiz
        
        if not result_id:
            return Response({"detail": "result_id is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            result = Result.objects.get(id=result_id)
        except Result.DoesNotExist:
            return Response({"detail": "Result not found."}, status=status.HTTP_404_NOT_FOUND)

        # Serializerni request ma'lumotlari bilan yangilaymiz
        serializer = Pass_Exam_ResultSerializer(result, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    




































class ResultCreateAPIView1231(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Tokenni olish va tekshirish
        token_header = request.headers.get('Authorization', '')
        if not token_header or not token_header.startswith('Bearer '):
            return Response({"error": "Authorization token missing or invalid"}, status=status.HTTP_401_UNAUTHORIZED)

        token = token_header.split(' ')[1]

        try:
            # Imzoni tekshirmasdan tokenni ochish
            decoded_token = jwt.decode(token, options={"verify_signature": False})
        except jwt.DecodeError:
            return Response({"error": "Failed to decode token"}, status=status.HTTP_401_UNAUTHORIZED)

        # Studentni token orqali topish
        student_id = decoded_token.get('student_id')
        if not student_id:
            raise AuthenticationFailed("No student ID found in token")

        student = get_object_or_404(Student, id=student_id)

        # Foydalanuvchi kiritgan ma'lumotlar
        data = request.data
        answers = data.get("answers", [])
        end_time_str = data.get("end_time")

        # Natija hisoblash uchun o'zgaruvchilar
        total_questions = len(answers)
        correct_answers = 0
        total_score = 0
        science_set = set()

        # Javoblarni qayta ishlash
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

        # Fandagi savollarni tekshirish
        if len(science_set) != 1:
            return Response({"error": "All questions must belong to the same science"}, status=status.HTTP_400_BAD_REQUEST)
        science = science_set.pop()

        # Urinishlar sonini aniqlash
        attempt_number = Result.objects.filter(student=student, science=science).count() + 1

        # End time formatini tekshirish
        try:
            end_time = datetime.fromisoformat(end_time_str)
        except ValueError:
            return Response({"error": "Invalid end_time format. Use ISO format"}, status=status.HTTP_400_BAD_REQUEST)

        # Natija obyektini yaratish
        result = Result.objects.create(
            student=student,
            quiz=quiz,
            science=science,
            score=total_score,
            total_questions=total_questions,
            correct_answers=correct_answers,
            attempt_number=attempt_number,
            end_time=end_time
        )
        result.calculate_status()
        result.calculate_test_time()

        # Telegram orqali xabar yuborish
        phone = student.user.phone
        result_bot = Result_Telegram_Bot.objects.filter(phone=phone).first()
        if not result_bot:
            return Response({"detail": "Telefon raqam topilmadi."}, status=status.HTTP_404_NOT_FOUND)

        telegram_id = result_bot.telegram_id
        message = (
            f"🏅 Test natijalari:\n\n"
            f"👤 O'quvchi: {student.full_name}\n"
            f"🔬 Fan: {science.name}\n"
            f"✅ To'g'ri javoblar: {correct_answers}/{total_questions}\n"
            f"📊 Umumiy ball: {total_score}\n"
            f"⏱️ Test vaqti: {result.test_time}\n"
        )
        BOT_TOKEN = "7826335243:AAGXTZvtzJ8e8g35Hrx_Swy7mwmRPd3T7Po"
        TELEGRAM_API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        response = requests.post(
            TELEGRAM_API_URL,
            json={"chat_id": telegram_id, "text": message, "parse_mode": "HTML"}
        )
        if response.status_code != 200:
            return Response(
                {"detail": f"Telegram xatolik: {response.json()}"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Muvaffaqiyatli javob qaytarish
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
