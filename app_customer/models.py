from django.db import models
from django.contrib.auth.models import AbstractUser
from app_main.models import Region, Districts


class User(AbstractUser):
    # username = None  # username maydonini o'chirish
    phone = models.CharField(max_length=15, unique=True)  # phone endi unikallashadi
    role = models.CharField(
        max_length=10,
        choices=[('student', 'Student'), ('teacher', 'Teacher'), ('admin', 'Admin')],
        default='student'
    )
    sms_code = models.CharField(max_length=6, blank=True, null=True)

    USERNAME_FIELD = 'phone'  # Login uchun phone maydoni ishlatiladi
    REQUIRED_FIELDS = []  # Phone maydonidan tashqari talab qilinadigan maydonlar

    def __str__(self):
        return f'{self.phone} - {self.role}'

ACADEMY_OR_SCHOOL = (
    ("Litsey", "Litsey"),
    ("Maktab", "Maktab"),
)

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    full_name = models.CharField(max_length=200)
    region = models.ForeignKey(Region, on_delete=models.PROTECT)
    districts = models.ForeignKey(Districts, on_delete=models.CASCADE)
    address = models.CharField(max_length=500)
    brithday = models.CharField(max_length=20)
    academy_or_school = models.CharField(max_length=20, choices=ACADEMY_OR_SCHOOL)
    class_name = models.CharField(max_length=20)
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.full_name


