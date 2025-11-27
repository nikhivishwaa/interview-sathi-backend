import uuid
from typing import Any, Dict
from django.core.exceptions import ValidationError
from django.db import transaction
from resume.models import Resume
from resume.services.validation import call_resume_validator_lambda


MAX_RESUME_SIZE_BYTES = 5 * 1024 * 1024  # 5 MB


def upload_resume(user, uploaded_file) -> Resume:
    """
    Public entrypoint used by the API:

    1. Validate incoming file (type/size).
    2. Create Resume row.
    3. Call Lambda for validation and parsing.
    4. Update Resume with flags, parsed_text/json, status.

    If validation fails for business reasons, so ValidationError raised.
    """

    if not uploaded_file:
        raise ValidationError("Resume not provided.")

    if not uploaded_file.name.lower().endswith(".pdf"):
        raise ValidationError("Resume must be a PDF file.")

    if uploaded_file.size > MAX_RESUME_SIZE_BYTES:
        raise ValidationError("Resume too large. Max 5 MB.")

    original_name = uploaded_file.name
    uploaded_file.name = f"{uuid.uuid4()}_{original_name[-20:]}"

    with transaction.atomic():
        resume = Resume.objects.create(
            user=user,
            file=uploaded_file,
            name=original_name,
            status=Resume.STATUS_UPLOADED,
        )

        run_validation_and_update(resume)

    return resume


def run_validation_and_update(resume: Resume) -> None:
    """
    Call Lambda and update the Resume instance in-place.
    All DB writes are done inside the outer transaction in upload_resume().
    """
    resume.status = Resume.STATUS_PROCESSING
    resume.save(update_fields=["status"])

    user = resume.user

    try:
        result: Dict[str, Any] = call_resume_validator_lambda(resume, user)
    except Exception as exc:
        # Hard infra error (Lambda / network / IAM)
        resume.status = Resume.STATUS_ERROR
        resume.reject_reason = f"Validation service error: {exc}"
        resume.save(update_fields=["status", "reject_reason"])
        return

    
    parsed_text = result.get("parsed_text") or ""
    parsed_json = result.get("parsed_json") or None
    del result['parsed_json']
    del result['parsed_text']
    resume.lambda_raw = result

    if result.get("status") != "ok":
        resume.status = Resume.STATUS_ERROR
        resume.reject_reason = result.get("reason") or "Unknown validation error."
        resume.save(update_fields=["status", "reject_reason", "lambda_raw"])
        return

    is_resume = bool(result.get("is_resume"))
    matches_user = bool(result.get("matches_user"))

    resume.is_valid_resume = is_resume
    resume.matches_user = matches_user

    if not is_resume:
        resume.status = Resume.STATUS_REJECTED
        resume.reject_reason = (
            result.get("reason")
            or "Uploaded file does not look like a resume."
        )
        resume.save(
            update_fields=[
                "status",
                "reject_reason",
                "is_valid_resume",
                "matches_user",
                "lambda_raw",
            ]
        )
        return

    if not matches_user:
        resume.status = Resume.STATUS_REJECTED
        resume.reject_reason = (
            result.get("reason")
            or "Resume does not appear to belong to this account."
        )
        resume.save(
            update_fields=[
                "status",
                "reject_reason",
                "is_valid_resume",
                "matches_user",
                "lambda_raw",
            ]
        )
        return

    # if resume belonging to user.
    resume.parsed_text = parsed_text
    resume.parsed_json = parsed_json
    resume.status = Resume.STATUS_READY

    resume.save(
        update_fields=[
            "status",
            "parsed_text",
            "parsed_json",
            "is_valid_resume",
            "matches_user",
            "lambda_raw",
        ]
    )
