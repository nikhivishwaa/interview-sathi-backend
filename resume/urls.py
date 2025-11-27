from django.urls import path, include
from resume import views

urlpatterns = [
    path('', views.ResumeAPIView.as_view()),
    path('<int:resume_id>/', views.ResumeUpdateAPIView.as_view()),
]
