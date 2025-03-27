from django.urls import path, include
from interview import views

urlpatterns = [
    path('', views.home, name='home'),
    
]
