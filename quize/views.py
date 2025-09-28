from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.utils import timezone

from .models import QuizCategory, Quiz, Question, Option, UserQuizAttempt, UserAnswer
from .serializers import QuizCategorySerializer, QuizSerializer, UserQuizAttemptSerializer

class QuizCategoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        categories = QuizCategory.objects.all()
        serializer = QuizCategorySerializer(categories, many=True)
        return Response({"status": "success", "data": serializer.data})


class QuizListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, category_id):
        quizzes = Quiz.objects.filter(category_id=category_id)
        serializer = QuizSerializer(quizzes, many=True)
        return Response({"status": "success", "data": serializer.data})


class QuizDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, quiz_id):
        try:
            quiz = Quiz.objects.get(id=quiz_id)
            serializer = QuizSerializer(quiz)
            return Response({"status": "success", "data": serializer.data})
        except Quiz.DoesNotExist:
            return Response({"status": "failed", "message": "Quiz not found"}, status=404)


class SubmitQuizView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, quiz_id):
        try:
            quiz = Quiz.objects.get(id=quiz_id)
            answers = request.data.get("answers", [])

            attempt = UserQuizAttempt.objects.create(user=request.user, quiz=quiz, score=0)
            score = 0

            for ans in answers:
                qid = ans.get("question")
                oid = ans.get("option")
                try:
                    question = Question.objects.get(id=qid, quiz=quiz)
                    option = Option.objects.get(id=oid, question=question)
                    is_correct = option.is_correct
                    if is_correct:
                        score += question.marks
                    UserAnswer.objects.create(
                        attempt=attempt,
                        question=question,
                        selected_option=option,
                        is_correct=is_correct
                    )
                except Exception:
                    continue

            attempt.score = score
            attempt.completed_at = timezone.now()
            attempt.save()

            serializer = UserQuizAttemptSerializer(attempt)
            return Response({"status": "success", "score": score, "data": serializer.data})

        except Quiz.DoesNotExist:
            return Response({"status": "failed", "message": "Quiz not found"}, status=404)
