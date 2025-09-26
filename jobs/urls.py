from django.urls import path, include
from jobs import views

urlpatterns = [
    path('', views.JobsAPIView.as_view(), name='all_jobs'),# GET
]
