from rest_framework import serializers
from .models import Science, Quiz, Result
from app_customer.models import Student








class ScienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Science
        fields = '__all__'

    def validate(self, data):
        if data['start_date'] >= data['end_date']:
            raise serializers.ValidationError("Start date must be earlier than end date.")
        return data







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
