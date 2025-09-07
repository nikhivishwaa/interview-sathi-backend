from django.db import models
from accounts.models import User


# class Language(models.Model):
#     name = models.CharField(max_length=100)
#     version = models.CharField(max_length=50)
#     docker_image = models.CharField(max_length=200)
#     time_limit = models.IntegerField(help_text="Time limit in milliseconds")
#     memory_limit = models.IntegerField(help_text="Memory limit in MB")

#     class Meta:
#         db_table = "languages"
#         ordering = ["name", "version"]
#         indexes = [models.Index(fields=["name", "version"])]

#     def __str__(self):
#         return f"{self.name} {self.version}"


class CodingQuestion(models.Model):
    DIFFICULTY_CHOICES = (
        ("Easy", "Easy"),
        ("Medium", "Medium"),
        ("Hard", "Hard"),
    )
    VISIBILITY_CHOICES = (
        ("public", "Public"),
        ("private", "Private"),
    )

    EXAMPLE = {
        "input":"n=5 arr[n]=[1, 2, 3, 4, 5]",
        "output":"12",
        "explanation":"taking 5 values as input and summing up last 3 values",
    }

    title = models.CharField(max_length=200, blank=False, null=False)
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, blank=False, null=False)
    statement = models.TextField(blank=False, null=False)
    code = models.TextField(blank=False, null=False)
    constraints = models.JSONField(default=list, blank=True)
    time_complexity = models.TextField(max_length=12, help_text='O(n)', blank=False, null=False)
    space_complexity = models.TextField(max_length=12, help_text='O(n)', blank=False, null=False)
    visibility = models.CharField(max_length=10, choices=VISIBILITY_CHOICES, default="public", blank=False, null=False)
    examples = models.JSONField(default=list, help_text=f"Example: {EXAMPLE}", blank=False, null=False)
    tags = models.JSONField(default=list, help_text=f'Example: ["Array", "Math"]', blank=True)
    companies = models.JSONField(default=list, help_text=f'Example: ["Amazon", "Flipkart"]', blank=True)
    score = models.FloatField(default=100.0, blank=False, null=False)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='problem_statement', null=True)
    is_deleted = models.BooleanField(default=False, null=False, blank=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "coding_questions"
        ordering = ["-created_at"]
        verbose_name = "Coding Question"
        verbose_name_plural = "Coding Questions"
        indexes = [models.Index(fields=["difficulty"]), models.Index(fields=["title"])]

    def __str__(self):
        return self.title


class TestCase(models.Model):
    question = models.ForeignKey(
        CodingQuestion, on_delete=models.CASCADE, related_name="testcases"
    )
    input_data = models.TextField()
    expected_output = models.TextField()
    score = models.FloatField(default=100)
    is_hidden = models.BooleanField(default=True)

    class Meta:
        db_table = "test_cases"
        ordering = ["question"]
        verbose_name = "Test Case"
        verbose_name_plural = "Test Cases"
        indexes = [
            models.Index(fields=["question", "is_hidden"]),
        ]

    def __str__(self):
        return f"TestCase for {self.question.title}"