from rest_framework import serializers
from interview.models import Resume

class ResumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resume
        fields = ['id', 'file', 'uploaded_at', 'parsed_text']
        read_only_fields = ['id', 'uploaded_at', 'parsed_text']
        extra_kwargs = {
            'file': {'required': True},
        }