from django.contrib import admin
from coding.models import CodingQuestion, TestCase


@admin.register(CodingQuestion)
class CodingQuestionAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "difficulty", "visibility", "author", "created_at", "is_deleted")
    list_filter = ("difficulty", "visibility", "is_deleted")
    search_fields = ("title", "statement", "author__first_name")
    ordering = ("-created_at",)


@admin.register(TestCase)
class TestCaseAdmin(admin.ModelAdmin):
    list_display = ("id", "question", "input_data", "expected_output", "is_hidden", "score")
    list_filter = ("is_hidden",)
    search_fields = ("question__title",)
    ordering = ("question",)
