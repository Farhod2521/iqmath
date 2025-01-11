from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from .models import Student, User


# @admin.register(Student)
# class StudentAdmin(TranslationAdmin):
#     list_display = ('full_name', 'region', 'districts', 'address', 'brithday', 'academy_or_school', 'class_name', 'status')



# Register the User model (if needed)
admin.site.register(User)
admin.site.register(Student)
