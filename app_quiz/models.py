from django.db import models
from ckeditor.fields import RichTextField
from app_customer.models import Student



from django.core.exceptions import ValidationError

class Science(models.Model):
    name = models.CharField(max_length=200)
    duration_in_minutes = models.PositiveIntegerField(default=60)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    def clean(self):
        if self.start_date >= self.end_date:
            raise ValidationError("Start date must be earlier than end date.")

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'Science'

ANSWER = (
    ('A','A'),
    ('B','B'),
    ('C','C'),
    ('D','D'),
)
CLASS_NAME = (
    ('10','10'),
    ('11','11'),
    ('1','1'),
    ('2','2'),
    ('3','3'),
)

class Quiz(models.Model):
    science  =  models.ForeignKey(Science,  on_delete=models.PROTECT)
    question  =  RichTextField()
    A =  RichTextField()
    B =  RichTextField()
    C =  RichTextField()
    D =  RichTextField()
    answer =  models.CharField(max_length=20, choices=ANSWER)
    score =  models.FloatField()
    grade   =  models.CharField(max_length=10, choices=CLASS_NAME)

    class Meta:
        db_table = 'Quiz'

from django.core.exceptions import ValidationError

from django.utils.timezone import now
from datetime import timedelta

class Result(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='results')
    quiz = models.ForeignKey('Quiz', on_delete=models.CASCADE, related_name='results')
    science = models.ForeignKey('Science', on_delete=models.CASCADE, related_name='results')
    score = models.FloatField()
    total_questions = models.PositiveIntegerField()
    correct_answers = models.PositiveIntegerField()
    start_time = models.DateTimeField(auto_now_add=True)
    test_time = models.PositiveIntegerField()  # Necha minut ishlagan vaqt sifatida saqlanadi
    status_exam = models.BooleanField(null=True, default=None)
    correct_questions = models.JSONField(default=list)  # To'g'ri javoblar (savollarni id-lari bilan)
    incorrect_questions = models.JSONField(default=list)  # Xato javoblar (savollarni id-lari bilan)
    answer_more = models.JSONField(default=list)  # Random savollar va ularga tegishli ballar

    def __str__(self):
        return f"{self.student} - {self.quiz} - {self.score}"

    class Meta:
        db_table = 'Result'
        ordering = ['-score']
        verbose_name = 'Result'
        verbose_name_plural = 'Results'



class Pass_Exam_Student(models.Model):
    count =  models.PositiveIntegerField(default=300)

class Result_Telegram_Bot(models.Model):
    phone = models.CharField(max_length=200)
    telegram_id = models.PositiveIntegerField()

    def __str__(self):
        return self.phone