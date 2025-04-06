from django.apps import AppConfig


class InterviewConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'interview'

    verbose_name = 'Interview Management'
    def ready(self):
        from interview.signals import extract_questions_from_pdf  , post_save, QuestionPDF
        post_save.connect(extract_questions_from_pdf, sender=QuestionPDF)
        
