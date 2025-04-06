from django.urls import path, include
from interview import views

urlpatterns = [
    path('', views.home, name='home'),
    path('resumes/upload/', views.ResumeUploadView.as_view()),
    path('resumes/', views.ResumeListView.as_view()),
]
