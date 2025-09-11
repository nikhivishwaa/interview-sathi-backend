from django.contrib import admin
from .models import Language, CodingQuestion, CodingSolution, TestCase, Submission, SubmissionLog


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ("name", "version", "docker_image")
    search_fields = ("name", "version")
    ordering = ("name", "version")
    list_filter = ("name",)


@admin.register(CodingQuestion)
class CodingQuestionAdmin(admin.ModelAdmin):    
    list_display = ("id", "title", "difficulty", "visibility", "author", "score", "created_at", "is_deleted")
    list_filter = ("difficulty", "visibility", "is_deleted")
    search_fields = ("title", "statement", "tags", "companies", "author__first_name")
    readonly_fields = ("created_at", "updated_at")
    ordering = ("-created_at",)


@admin.register(TestCase)
class TestCaseAdmin(admin.ModelAdmin):
    list_display = ("id", "question", "input_data", "expected_output", "is_hidden", "score")
    list_filter = ("is_hidden",)
    search_fields = ("question__title",)
    ordering = ("question",)




@admin.register(CodingSolution)
class CodingSolutionAdmin(admin.ModelAdmin):
    list_display = ("id", "question", "language", "created_at", "is_deleted")
    search_fields = ("question__title", "language__name")
    list_filter = ("language", "is_deleted")
    ordering = ("-created_at",)


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "question", "language", "status", "created_at")
    search_fields = ("user__first_name", "question__title")
    list_filter = ("status", "language", "created_at")
    ordering = ("-created_at",)
    readonly_fields = ("created_at", "updated_at")


@admin.register(SubmissionLog)
class SubmissionLogAdmin(admin.ModelAdmin):
    list_display = ("id", "submission", "testcase", "status", "time_taken")
    search_fields = ("submission__id", "submission__user__first_name", "submission__question__title")
    list_filter = ("status",)
    ordering = ("submission", "id")
