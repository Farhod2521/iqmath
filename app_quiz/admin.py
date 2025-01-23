from django.contrib import admin
from .models import Science, Quiz, Result, Result_Telegram_Bot


class Result_Telegram_Bot_Admin(admin.ModelAdmin):
    list_display = ("phone", "telegram_id")


class ScienceAdmin(admin.ModelAdmin):
    list_display = ('name', 'duration_in_minutes', 'start_date', 'end_date')
    search_fields = ('name',)
    list_filter = ('start_date', 'end_date')
    ordering = ('name',)

class QuizAdmin(admin.ModelAdmin):
    list_display = ('science',  'answer', 'score', 'grade')
    search_fields = ('question',)
    list_filter = ('science', 'grade')
    ordering = ('-score',)

class ResultAdmin(admin.ModelAdmin):
    list_display = ('id', 'student', 'quiz', 'science', 'score', 'total_questions', 'correct_answers', 'status_exam')
    search_fields = ('student__first_name', 'student__last_name', 'quiz__question')
    list_filter = ('status_exam', 'quiz', 'science', 'student')
    ordering = ('-score',)
    raw_id_fields = ('student', 'quiz', 'science')

    def save_model(self, request, obj, form, change):
        """Urinishlar sonini boshqarish va statusni hisoblash"""
        obj.calculate_status(passing_score=50)
        super().save_model(request, obj, form, change)

admin.site.register(Science, ScienceAdmin)
admin.site.register(Quiz, QuizAdmin)
admin.site.register(Result, ResultAdmin)
admin.site.register(Result_Telegram_Bot, Result_Telegram_Bot_Admin)
