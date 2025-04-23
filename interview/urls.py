from django.urls import path, include
from interview import views

urlpatterns = [
    path('', views.home, name='home'),
    path('resumes/', views.ResumeAPIView.as_view()),
    path('resumes/<int:resume_id>/', views.ResumeUpdateAPIView.as_view()),
    path('interviews/', views.ScheduleInterviewView.as_view()),
]
