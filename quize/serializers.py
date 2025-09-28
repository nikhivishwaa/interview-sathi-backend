from rest_framework import serializers
from .models import QuizCategory, Quiz, Question, Option, UserQuizAttempt, UserAnswer

class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ["text", "is_correct"]  # expose is_correct for reference

class QuestionSerializer(serializers.ModelSerializer):
    options = OptionSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ["text", "marks", "description_right_options_answer", "options"]

class QuizSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Quiz
        fields = ["id", "title", "description", "duration_minutes", "questions"]

class QuizCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizCategory
        fields = ["id", "name", "description"]

class UserAnswerSerializer(serializers.ModelSerializer):
    question = serializers.StringRelatedField()
    selected_option = serializers.StringRelatedField()

    class Meta:
        model = UserAnswer
        fields = ["id", "question", "selected_option", "is_correct"]

class UserQuizAttemptSerializer(serializers.ModelSerializer):
    quiz = serializers.StringRelatedField()
    answers = UserAnswerSerializer(many=True, read_only=True, source="useranswer_set")

    class Meta:
        model = UserQuizAttempt
        fields = ["id", "quiz", "score", "started_at", "completed_at", "answers"]
