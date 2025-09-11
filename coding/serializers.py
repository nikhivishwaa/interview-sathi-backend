from rest_framework import serializers
from coding.models import CodingQuestion, TestCase


class TestCaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestCase
        fields = ('id', 'input_data', 'expected_output')


class CodingQuestionSerializer(serializers.ModelSerializer):
    testcases = serializers.SerializerMethodField()

    class Meta:
        model = CodingQuestion
        fields = "__all__"

    def get_testcases(self, obj):
        # Only return visible testcases
        visible_testcases = obj.testcases.filter(is_hidden=False)
        return TestCaseSerializer(visible_testcases, many=True).data


        
