from django.contrib import admin, messages
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
    list_display = ['id', 'user', 'resume', 'role', 'is_active', 'status', 'created_at']
    search_fields = ['user__first_name', 'user__last_name', 'role']
    list_filter = ['role', 'is_active', 'status']
    actions = ['mark_completed', 'mark_scheduled']

    @admin.action(description='Mark Interview as Completed')
    def mark_completed(self, request, queryset):
        queryset.update(status='completed')
        messages.success(request, f"{'Interview' if queryset.count()>1 else 'Interviews'} Successfully marked as Completed!")

    @admin.action(description='Mark Interview as Scheduled')
    def mark_scheduled(self, request, queryset):
        queryset.update(status='scheduled')
        messages.success(request, f"{'Interview' if queryset.count()>1 else 'Interviews'} Successfully marked as Scheduled!")

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
    