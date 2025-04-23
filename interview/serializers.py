from rest_framework import serializers
from interview.models import Resume, InterviewSession

class ResumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resume
        fields = ['id', 'name', 'file', 'uploaded_at', 'last_updated']
        read_only_fields = ['id', 'uploaded_at']
        extra_kwargs = {
            'file': {'required': True},
        }

class InterviewSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = InterviewSession
        resume = ResumeSerializer()
        fields = ["id", "metadata", "user", "role",
                  "created_at", "scheduled_at", "started_at", "ended_at", "is_active", "status", "resume"
                  ]
        read_only_fields = ['id', 'created_at']
        