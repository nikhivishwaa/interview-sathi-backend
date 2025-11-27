import json
from typing import Any, Dict
import boto3
from django.conf import settings


lambda_client = boto3.client(
    "lambda",
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    region_name=settings.AWS_S3_REGION_NAME,
)


def call_resume_validator_lambda(resume, user) -> Dict[str, Any]:
    """
    Call the AWS Lambda that validates & parses a resume.
    Returns the raw JSON dict from Lambda, or raises on hard failure (e.g., network / auth errors).
    """

    payload = {
        "bucket": settings.AWS_STORAGE_BUCKET_NAME,
        "key": f"media/private/{resume.file.name}",
        "user": {
            "id": user.id,
            "full_name": user.get_full_name(),
            "email": user.email,
        },
    }

    response = lambda_client.invoke(
        FunctionName=settings.RESUME_VALIDATOR_LAMBDA_NAME,
        InvocationType="RequestResponse",
        Payload=json.dumps(payload),
    )

    raw_body = response.get("Payload").read()
    data: Dict[str, Any] = json.loads(raw_body or "{}")
    return data
