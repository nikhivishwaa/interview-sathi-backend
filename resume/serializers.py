from rest_framework import serializers
from resume.models import Resume


class ResumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resume
        fields = ['id', 'name', 'file', 'uploaded_at', 'last_updated']
        read_only_fields = ['id', 'uploaded_at', 'file']
        