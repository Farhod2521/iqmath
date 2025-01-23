from rest_framework import serializers
from .models import Science, Quiz, Result, Result_Telegram_Bot 
from app_customer.models import Student





class Result_Telegram_Bot_Serializers(serializers.ModelSerializer):
    class Meta:
        model =  Result_Telegram_Bot
        fields = "__all__"
    
    def validate_phone(self, phone):
   
        if Result_Telegram_Bot.objects.filter(phone=phone).exists():
            raise serializers.ValidationError("Bu telefon raqam allaqachon ro'yxatdan o'tgan.")
        return phone

class ScienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Science
        fields = '__all__'

    def validate(self, data):
        if data['start_date'] >= data['end_date']:
            raise serializers.ValidationError("Start date must be earlier than end date.")
        return data



class  Quiz_Add_Serializers(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = "__all__"



class ScienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Science
        fields = '__all__'


class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = ['id', 'question', 'A', 'B', 'C', 'D', 'grade', 'science']


from rest_framework import serializers
from .models import Result

class ResultSerializer(serializers.ModelSerializer):
    student = serializers.PrimaryKeyRelatedField(queryset=Student.objects.all())
    quiz = serializers.PrimaryKeyRelatedField(queryset=Quiz.objects.all())
    science = serializers.PrimaryKeyRelatedField(queryset=Science.objects.all())

    class Meta:
        model = Result
        fields = ['student', 'quiz', 'science', 'score', 'total_questions', 'correct_answers', 'attempt_number', 'end_time']



class Result_Telegram_Serializers(serializers.ModelSerializer):
    student = serializers.SerializerMethodField()
    science = serializers.SerializerMethodField()

    class Meta:
        model = Result
        fields = [
            "student",
         
            "science",
            "score",
            "total_questions",
            "correct_answers",
      
            "test_time",
        ]

    def get_student(self, obj):
        return obj.student.full_name
    
    def get_science(self, obj):
        return obj.science.name
    


class Pass_Exam_ResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Result
        fields = ['id', 'status_exam']