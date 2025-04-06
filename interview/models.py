from django.db import models
from accounts.models import User

class QuestionPDF(models.Model):
    DOMAIN_CHOICES = (
        ('frontend', 'Frontend'),
        ('backend', 'Backend'),
    )
    DIFFICULTY_LEVEL = (
        ('l1', 'Basics'),
        ('l2', 'Intermediate'),
        ('l3', 'Advance'),
        ('l4', 'Pro'),
    )
    title = models.CharField(max_length=255)
    pdf_file = models.FileField(upload_to='question_pdfs/')
    domain = models.CharField(max_length=20, choices=DOMAIN_CHOICES)
    level = models.CharField(max_length=20, choices=DIFFICULTY_LEVEL)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.domain}: {self.level} - {self.title[:10]}..."

class Resume(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to='resumes/')
    uploaded_at = models.DateTimeField(auto_now_add=True, null=False, blank=False)
    parsed_text = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.first_name}'s Resume"

class InterviewSession(models.Model):
    ROLE_CHOICES = (
        ('frontend', 'Frontend'),
        ('backend', 'Backend'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True, null=False, blank=False)
    is_active = models.BooleanField(default=True, null=False, blank=False)


class InterviewQuestion(models.Model):
    DOMAIN_CHOICES = (
        ('frontend', 'Frontend'),
        ('backend', 'Backend'),
    )
    COMING_FROM_OPTIONS = (
        ('pdf', 'PDF'),
        ('model','Model')
    )

    domain = models.CharField(max_length=20, choices=DOMAIN_CHOICES, null=False, blank=False)  # e.g., 'frontend', 'backend'
    question_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, null=False, blank=False)
    source = models.ForeignKey(QuestionPDF, on_delete=models.CASCADE, related_name='questions', null=True, blank=True)  # source of the question
    coming_from = models.CharField(max_length=100, default="pdf", null=False, blank=False)  # 

    def __str__(self):
        return f"{self.domain} : question: {self.question_text[:10]}..."
    

class InterviewHistory(models.Model):
    session = models.ForeignKey(InterviewSession, on_delete=models.CASCADE, related_name='history')
    question = models.ForeignKey(InterviewQuestion, on_delete=models.CASCADE)
    answer = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
