from django.urls import path
from .views import QuizCategoryView, QuizListView, QuizDetailView, SubmitQuizView

urlpatterns = [
    path("categories/", QuizCategoryView.as_view(), name="quiz-categories"),
    path("categories/<int:category_id>/quizzes/", QuizListView.as_view(), name="quiz-list"),
    path("<int:quiz_id>/", QuizDetailView.as_view(), name="quiz-detail"),
    path("<int:quiz_id>/submit/", SubmitQuizView.as_view(), name="quiz-submit"),
    # path("history/", UserQuizHistoryView.as_view(), name="quiz-history")

]
