from django.contrib import admin
from interview.models import QuestionPDF, Resume, InterviewSession,InterviewQuestion, InterviewHistory

@admin.register(QuestionPDF)
class QuestionPDFAdmin(admin.ModelAdmin):
    list_display = ['id', 'domain', 'level', 'title', 'pdf_file', 'uploaded_at']
    search_fields = ['title', 'domain', 'level']
    list_filter = ['domain','level']

@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'file', 'uploaded_at']
    search_fields = ['user__first_name', 'user__last_name']

@admin.register(InterviewSession)
class InterviewSessionAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'resume', 'role', 'is_active', 'created_at']
    search_fields = ['user__first_name', 'user__last_name']
    list_filter = ['role', 'is_active']

@admin.register(InterviewQuestion)
class InterviewQuestionAdmin(admin.ModelAdmin):
    list_display = ['id', 'domain', 'created_at', 'question', 'source', 'coming_from']
    search_fields = ['question_text', 'domain', 'coming_from']

    def question(self,obj):
        return obj.question_text[:100] + '...'

@admin.register(InterviewHistory)
class InterviewHistoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'session', 'question', 'answer', 'created_at']
    search_fields = ['session__role', 'question__domain']
    