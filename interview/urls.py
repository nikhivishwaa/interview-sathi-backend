from django.urls import path, include
from interview import views

urlpatterns = [
    path('', views.home, name='home'),
    path('health/', views.health, name='health'),
    # path('resumes/', views.ResumeAPIView.as_view()),
    # path('resumes/<int:resume_id>/', views.ResumeUpdateAPIView.as_view()),
    path('interviews/', views.ScheduleInterviewView.as_view()),
    path('feedback/<int:interview_id>/', views.InterviewFeedbackView.as_view()),
    path('interviews/<int:interview_id>/', views.CancelInterviewView.as_view()),
]
