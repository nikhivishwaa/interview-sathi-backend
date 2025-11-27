from django.db import models
from accounts.models import User
from interviewsathi.storage_backends import PrivateMediaStorage


class Resume(models.Model):
    STATUS_UPLOADED = "uploaded"
    STATUS_PROCESSING = "processing"
    STATUS_READY = "ready"
    STATUS_REJECTED = "rejected"
    STATUS_ERROR = "error"

    STATUS_CHOICES = [
        (STATUS_UPLOADED, "Uploaded"),
        (STATUS_PROCESSING, "Processing"),
        (STATUS_READY, "Ready"),
        (STATUS_REJECTED, "Rejected"),
        (STATUS_ERROR, "Error"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="resumes",
        blank=False
    )

    file = models.FileField(
        storage=PrivateMediaStorage(),
        upload_to="resumes/",
    )
    name = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True, null=False, blank=False)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_UPLOADED,
    )
    reject_reason = models.TextField(blank=True)
    is_valid_resume = models.BooleanField(default=False)
    matches_user = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    
    # From Lambda
    parsed_text = models.TextField(blank=True)
    parsed_json = models.JSONField(default=dict, blank=True, null=True)

    # Optional: raw Lambda response for debugging/auditing
    lambda_raw = models.JSONField(blank=True, null=True)

    class Meta:
        ordering = ["-uploaded_at"]
        db_table = "resume"
        verbose_name = "Resume"
        verbose_name_plural = "Resumes"


    def __str__(self):
        return f"{self.user} - {self.name} ({self.status})"
