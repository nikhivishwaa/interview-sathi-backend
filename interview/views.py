from django.http import JsonResponse
from rest_framework.generics import ListAPIView
from interview.models import Resume, InterviewSession
from django.utils import timezone
from interview.serializers import ResumeSerializer, InterviewSessionSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from interview.utils.resume_parser import parse_resume_text, clean_resume_text
from rest_framework import status
import uuid
from django.core.cache import cache

def get_cached_resume(user_id):
    key = f"user_resume_{user_id}"
    data = cache.get(key)
    if not data:
        # fetch from DB and store in cache
        resume = Resume.objects.filter(user_id=user_id).latest('uploaded_at')
        data = resume.parsed_text
        cache.set(key, data, timeout=3600)  # 1 hour cache
    return data



class ResumeAPIView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser]

    def get(self, request):
        try:
            resumes = Resume.objects.filter(user=self.request.user).order_by('-uploaded_at')
            serializer = ResumeSerializer(resumes, many=True)

            res = {
                "status":"success",
                "message":"your uploaded resumes",
                "data": serializer.data
            }
            print(res)
            return Response(res, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"status":"failed"}, status=status.HTTP_404_NOT_FOUND)
        
    def post(self, request):
        try:
            resume_file = request.FILES.get('resume')
            resume_name = request.data.get('name').strip()
            if not resume_file:
                return Response({"status":"failed","message": "resume not provided."}, status=status.HTTP_400_BAD_REQUEST)
            
            if not resume_file.name.endswith('.pdf'):
                return Response({"status":"failed","message": "resume must be pdf file."}, status=status.HTTP_400_BAD_REQUEST)
            
            if not resume_name:
                resume_name = resume_file.name
        
            resume_file.name = f"{uuid.uuid4()}_{resume_file.name[-10:]}"
            resume = Resume.objects.create(user=request.user, file=resume_file, name=resume_name)
            # parsed_text = parse_resume_text(resume.file.path)
            # resume.parsed_text = parsed_text
            # resume.save()
            raw_text = parse_resume_text(resume.file.path)
            cleaned_text = clean_resume_text(raw_text)
            resume.parsed_text = cleaned_text
            resume.save()

            serializer = ResumeSerializer(resume)

            res = {
                "status":"success",
                "message": "Resume uploaded and parsed.",
                "data": serializer.data
            }

            return Response(res, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"status":"failed","message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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

def home(request):
    return JsonResponse({"message":"welcome to interview sathi"},status=200)

# post of the profile
# take resume
# strt interview
# ask followup questions
# summarize interview
# give feed back

class ScheduleInterviewView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:         
            sessions = InterviewSession.objects.filter(
                user=request.user
            ).order_by('-created_at')

            serializer = InterviewSessionSerializer(sessions, many=True)

            res = {
                "status":"success",
                "message":"Your interview list",
                "data":serializer.data
            }
            
            return Response(res, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            res = {
                "status":"failed",
                "message": "Something went Wrong",
                "data":[]
            }
            return Response(res, status=status.HTTP_404_NOT_FOUND)
        
    def post(self, request):
        print(request.data)
        role = request.data.get('role')
        resume_id = request.data.get('resume_id')
        scheduled_at = request.data.get('scheduled_at')  # ISO string

        if role not in ['frontend', 'backend']:
            res = {
                "status":"failed",
                "message": "Invalid role",
                "data":{}
            }
            return Response(res, status=status.HTTP_404_NOT_FOUND)
        
        if not resume_id or not resume_id.isnumeric():
            res = {
                "status":"failed",
                "message": "Select the Resume",
                "data":{}
            }
            return Response(res, status=status.HTTP_404_NOT_FOUND)

        try:
            print("checking resume")
            resume = Resume.objects.get(id=resume_id, user=request.user)
            # resume = Resume.objects.get(id=3, user=request.user)
            print("checked resume")
            session = InterviewSession.objects.create(
                user=request.user,
                resume=resume,
                role=role,
                scheduled_at=scheduled_at,
                metadata={}
            )
            print('session:', session)

            serializer = InterviewSessionSerializer(session)

            res = {
                "status":"success",
                "message":"interview is scheduled",
                "data":serializer.data
            }
            
            return Response(res, status=status.HTTP_201_CREATED)
        except Exception as e:
            res = {
                "status":"failed",
                "message": "Resume not found",
                "data":{}
            }
            return Response(res, status=status.HTTP_404_NOT_FOUND)
