from django.contrib import admin
from .models import QuizCategory, Quiz, Question, Option, UserQuizAttempt, UserAnswer


@admin.register(QuizCategory)
class QuizCategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "description")
    search_fields = ("name",)


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "category", "duration_minutes")
    list_filter = ("category",)
    search_fields = ("title", "description")


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("id", "quiz", "text", "marks", "description_right_options_answer")
    search_fields = ("text",)
    list_filter = ("quiz",)


@admin.register(Option)
class OptionAdmin(admin.ModelAdmin):
    list_display = ("id", "question", "text", "is_correct")
    list_filter = ("is_correct",)
    search_fields = ("text",)


@admin.register(UserQuizAttempt)
class UserQuizAttemptAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "quiz", "score", "started_at", "completed_at")
    list_filter = ("quiz", "started_at", "completed_at")
    search_fields = ("user__username", "quiz__title")


@admin.register(UserAnswer)
class UserAnswerAdmin(admin.ModelAdmin):
    list_display = ("id", "attempt", "question", "selected_option", "is_correct")
    list_filter = ("is_correct", "question")
    search_fields = ("question__text", "selected_option__text")
