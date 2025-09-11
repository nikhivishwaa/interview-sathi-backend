from django.db import models
from accounts.models import User


class Language(models.Model):
    name = models.CharField(max_length=100)
    version = models.CharField(max_length=50)
    docker_image = models.CharField(max_length=200)

    class Meta:
        db_table = "languages"
        unique_together = ('name', 'version')
        ordering = ["name", "version"]

    def __str__(self):
        return self.name


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
    constraints = models.JSONField(default=list, blank=True)
    time_complexity = models.TextField(max_length=12, help_text='O(n)', blank=False, null=False)
    space_complexity = models.TextField(max_length=12, help_text='O(n)', blank=False, null=False)
    visibility = models.CharField(max_length=10, choices=VISIBILITY_CHOICES, default="public", blank=False, null=False)
    examples = models.JSONField(default=list, help_text=f"Example: {EXAMPLE}", blank=False, null=False)
    tags = models.JSONField(default=list, help_text=f'Example: ["Array", "Math"]', blank=True)
    companies = models.JSONField(default=list, help_text=f'Example: ["Amazon", "Flipkart"]', blank=True)
    score = models.FloatField(default=100.0, blank=False, null=False)
    metadata = models.JSONField(default=dict, blank=True, null=False)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='problem_statement', null=True)
    is_deleted = models.BooleanField(default=False, null=False, blank=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        db_table = "coding_questions"
        verbose_name = "Coding Question"
        verbose_name_plural = "Coding Questions"
        indexes = [models.Index(fields=["difficulty"]), models.Index(fields=["title"])]

    def __str__(self):
        return self.title

class CodingSolution(models.Model):
    code = models.TextField(blank=False, null=False)
    language = models.ForeignKey(Language, on_delete=models.CASCADE, blank=False, null=False)
    question = models.ForeignKey(CodingQuestion, on_delete=models.CASCADE, blank=False, null=False, related_name='standard_solution')
    is_deleted = models.BooleanField(default=False, null=False, blank=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "coding_solution"
        ordering = ["-created_at"]
        unique_together = ('question', 'language')
        verbose_name = "Coding Solution"
        verbose_name_plural = "Coding Solutions"

    def __str__(self):
        return f"Solution for {self.question} in {self.language.name}"



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


class Submission(models.Model):
    STATUS_CHOICES = [
        ("In Progress", "In Progress"),
        ("Accepted", "Accepted"),
        ("Rejected", "Rejected"),
        ("Compilation Error", "Compilation Error"),
        ("Runtime Error", "Runtime Error"),
        ("TLE", "TLE"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="submissions", blank=False, null=False)
    question = models.ForeignKey(CodingQuestion, on_delete=models.CASCADE, related_name="submissions", blank=False, null=False)
    code = models.TextField(default='', blank=False, null=False)
    language = models.ForeignKey(Language, on_delete=models.CASCADE, blank=False, null=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="In Progress")
    metadata = models.JSONField(default=dict, blank=True, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "submissions"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["user", "question"]),
        ]

    def __str__(self):
        return f"Submission #{self.id}"


class SubmissionLog(models.Model):
    STATUS_CHOICES = [
        ("Pass", "Pass"),
        ("Failed", "Failed"),
    ]
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE, related_name="logs")
    testcase = models.ForeignKey(TestCase, on_delete=models.CASCADE, null=False, blank=False)
    actual_output = models.TextField(blank=True)
    stderr = models.TextField(blank=True)
    time_taken = models.FloatField(default=0.0)
    status = models.CharField(max_length=10,choices=STATUS_CHOICES)
    message = models.CharField(max_length=30, default="", null=False, blank=False)

    class Meta:
        db_table = "submission_logs"
        ordering = ["submission", "testcase"]
        unique_together = ["submission", "testcase"]
        indexes = [models.Index(fields=["submission", "testcase"])]

    def __str__(self):
        return f"{self.submission}"
