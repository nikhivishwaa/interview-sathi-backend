# interview/routing.py
from django.urls import path
from interview.consumers import InterviewConsumer

websocket_urlpatterns = [
    path("ws/interview/<int:session_id>/", InterviewConsumer.as_asgi()),
]
