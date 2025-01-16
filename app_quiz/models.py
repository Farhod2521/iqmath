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
    attempt_number = models.PositiveIntegerField(default=1)  # Urinishlar soni
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField()
    test_time = models.CharField(max_length=50)  # Necha minut ishlagan vaqt sifatida saqlanadi
    status = models.CharField(
        max_length=20,
        choices=[
            ('passed', 'Passed'),
            ('failed', 'Failed'),
        ],
        default='failed'
    )

    def calculate_status(self, passing_score=50):
        """Natija holatini hisoblash"""
        if self.score >= passing_score:
            self.status = 'passed'
        else:
            self.status = 'failed'
        self.save()

    def calculate_test_time(self):
        """Boshlanish va tugash vaqtlaridan necha minut ishlaganini hisoblash"""
        duration = self.end_time - self.start_time
        minutes = duration.total_seconds() // 60
        self.test_time = f"{int(minutes)} minutes"
        self.save()

    def __str__(self):
        return f"{self.student} - {self.quiz} - {self.score} points (Attempt {self.attempt_number})"

    class Meta:
        db_table = 'Result'
        ordering = ['-score']
        verbose_name = 'Result'
        verbose_name_plural = 'Results'


class Result_Telegram_Bot(models.Model):
    phone = models.CharField(max_length=200)
    telegram_id = models.PositiveIntegerField()

    def __str__(self):
        return self.phone