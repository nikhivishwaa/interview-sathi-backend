from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from resume.models import Resume
from resume.serializers import ResumeSerializer
from resume.services.pipeline import upload_resume


class ResumeAPIView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser]

    def get(self, request, *args, **kwargs):
        resumes = Resume.objects.filter(user=request.user, status=Resume.STATUS_READY, is_deleted=False).order_by('-uploaded_at')
        serializer = ResumeSerializer(resumes, many=True)

        res = {
            "status": "success",
            "message": "your uploaded resumes",
            "data": serializer.data,
        }
        return Response(res, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        resume_file = request.FILES.get("resume")

        try:
            resume = upload_resume(request.user, resume_file)
            serializer = ResumeSerializer(resume)

            if resume.status == Resume.STATUS_REJECTED:
                return Response(
                    {
                        "status": "failed",
                        "message": resume.reject_reason,
                        "data": serializer.data,
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if resume.status == Resume.STATUS_ERROR:
                return Response(
                    {
                        "status": "failed",
                        "message": "There was an error processing your resume.",
                        "data": serializer.data,
                    },
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

            return Response(
                {
                    "status": "success",
                    "message": "Resume uploaded and processed.",
                    "data": serializer.data,
                },
                status=status.HTTP_201_CREATED,
            )

        except ValidationError as exc:
            return Response(
                {"status": "failed", "message": str(exc)},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as exc:
            return Response(
                {"status": "failed", "message": str(exc)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class ResumeUpdateAPIView(APIView):
    permission_classes = [IsAuthenticated] 
    def put(self, request, resume_id):
        try:
            resume_name = request.data.get('name').strip()
            if not resume_name:
                return Response({"status":"failed","message": "resume_name must be provided."}, status=status.HTTP_400_BAD_REQUEST)
            
           
            resume = Resume.objects.get(id=resume_id, user=request.user)
            resume.name=resume_name
            resume.save()

            serializer = ResumeSerializer(resume)

            res = {
                "status":"success",
                "message": "Resume updated successfully",
                "data": serializer.data
            }

            return Response(res, status=status.HTTP_202_ACCEPTED)
        except Exception as e:
            return Response({"status":"failed","message": "Resume not Exist"}, status=status.HTTP_404_NOT_FOUND)
    
    def delete(self, request, resume_id):
        try:
            resume = Resume.objects.get(id=resume_id, user=request.user)
            resume.is_deleted=True
            resume.save()

            res = {
                "status":"success",
                "message": "Resume deleted successfully",
            }

            return Response(res, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"status":"failed","message": "Resume not Exist"}, status=status.HTTP_404_NOT_FOUND)
