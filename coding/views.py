import csv
import io
import json
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.db.models import Q
from coding.models import CodingQuestion, TestCase
from coding.serializers import CodingQuestionSerializer, TestCaseSerializer


class ProblemsAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        try:
            questions = CodingQuestion.objects.filter(visibility='public',
                                       is_deleted=False
                                    ).values('id', 'title','difficulty','tags','companies','score','author', 'created_at')
        
            response = {
                'status': 'success',
                'message': 'Coding Questions',
                'data': questions
            }
            return Response(response, status=status.HTTP_200_OK)
            
        except Exception as e:
            print(e)
            response = {
                'status': 'failed',
                'message': 'Unable to load coding questions',
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

    # def post(self, request):
    #     try:
    #         serializer = ProfileUpdateSerializer(data=request.data)
    #         if serializer.is_valid():
    #             data = serializer.validated_data
    #             user = request.user
    #             if user.phone != data['phone']:
    #                 try:
    #                     user = User.objects.get(phone=data.get('phone'))
    #                     res = {
    #                         "status":"failed",
    #                         "message":"Phone Number is Already Used. Try Another Number!",
    #                         "data":{}
    #                     }

    #                     return Response(res, status=status.HTTP_409_CONFLICT)
    #                 except Exception as e:
    #                     pass

    #             for key, value in data.items():
    #                 if hasattr(user, key):  # only set existing fields
    #                     setattr(user, key, value)
    #             user.save()
    #             p_serializer = ProfileSerializer(user)
    #             res = {
    #                 'status': 'success',
    #                 'message': 'Profile Updated Successfully',
    #                 'data': p_serializer.data
    #             }
    #             return Response(res, status=status.HTTP_202_ACCEPTED)
    #         else:
    #             res = {
    #                 'status': 'failed',
    #                 'message': 'Invalid Data',
    #                 'data': {},
    #                 'errors': serializer.errors
    #             }
    #             return Response(res, status=status.HTTP_400_BAD_REQUEST)
    #     except Exception as e:
    #         res = {
    #             'status': 'failed',
    #             'message': 'Something went Wrong!',
    #             'data': {},
    #         }
    #         return Response(res, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ProblemStatementUpdateAPIView(APIView):
    def get(self, request, ps_id):
        try:
            ps = CodingQuestion.objects.get(Q(pk=ps_id) & Q(is_deleted=False) & (Q(author=request.user) | Q(visibility='public')))
            res = {
                'status': 'success',
                'message': 'Coding Questions',
                'data': CodingQuestionSerializer(ps).data
            }
            return Response(res, status=status.HTTP_200_OK)
        except CodingQuestion.DoesNotExist:
            res = {
                'status': 'failed',
                'message': 'Coding Question Not Found'
            }
            return Response(res, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, ps_id):
        try:
            ps = CodingQuestion.objects.get(pk=ps_id, is_deleted=False)
            if ps.author == request.user:
                serializer = CodingQuestionSerializer(ps, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    res = {
                        'status': 'success',
                        'message': 'Coding Question updated',
                        'data': serializer.data
                    }
                
                    return Response(res, status=status.HTTP_200_OK)
                res = {
                    'status': 'failed',
                    'message': 'Coding Question cannot be updated due to incorrect data',
                    'data': serializer.errors
                }
                return Response(res, status=status.HTTP_304_NOT_MODIFIED)
        
            else:
                res = {
                    'status': 'Failed',
                    'message': 'You cannot update this Coding Question',
                }
                
                return Response(res, status=status.HTTP_400_BAD_REQUEST)
        
        except CodingQuestion.DoesNotExist:
            res = {
                'status': 'failed',
                'message': 'Coding Question Not Found'
            }
            return Response(res, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, ps_id):
        try:
            ps = CodingQuestion.objects.get(pk=ps_id, is_deleted=False)
            if ps.author == request.user:
                ps.is_deleted = True
                ps.save()
                res = {
                    'status': 'success',
                    'message': 'Coding Question Deleted',
                }
                
                return Response(res, status=status.HTTP_204_NO_CONTENT)
            else:
                res = {
                    'status': 'Failed',
                    'message': 'You cannot delete this Coding Question',
                }
                
                return Response(res, status=status.HTTP_400_BAD_REQUEST)
        except CodingQuestion.DoesNotExist:
            res = {
                'status': 'Failed',
                'message': 'Coding Question not found',
            }
            return Response(res, status=status.HTTP_404_NOT_FOUND)


class TestCasesAPIView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def get(self, request, ps_id):
        try:
            
            ps = CodingQuestion.objects.get(Q(pk=ps_id) & Q(is_deleted=False) & (Q(author=request.user) | Q(visibility='public')))
            testcases = ps.testcases.filter(is_hidden=False)
            res = {
                'status': 'success',
                'message': 'visible Testcases',
                'data': TestCaseSerializer(testcases, many=True).data
            }
            return Response(res, status=status.HTTP_200_OK)
        except (CodingQuestion.DoesNotExist, TestCase.DoesNotExist):
            res = {
                'status': 'failed',
                'message': 'Testcases not found',
            }
            return Response(res, status=status.HTTP_404_NOT_FOUND)


    def post(self, request, ps_id, testcase_id=None):
        try:
            question = CodingQuestion.objects.get(id=ps_id, is_deleted=False, author=request.user)
            testcases = []

            # Handling Testcase file upload (CSV or JSON)
            if "file" in request.FILES:
                file_obj = request.FILES["file"]
                filename = file_obj.name.lower()

                if filename.endswith(".csv"):
                    decoded_file = file_obj.read().decode("utf-8-sig")
                    reader = csv.DictReader(io.StringIO(decoded_file))

                    for row in reader:
                        testcases.append(
                            TestCase(
                                question=question,
                                input_data=row.get("input", "").strip(),
                                expected_output=row.get("output", "").strip(),
                                is_hidden=row.get("hidden", "true").lower() in ("true", "1"),
                                score=float(row.get("score", 0) or 0),
                            )
                        )

                elif filename.endswith(".json"):
                    data = json.load(file_obj)
                    if not isinstance(data, list):
                        res = {
                            "status":"failed",
                            "message": "JSON must be an array of testcases"
                        }
                        return Response(res, status=status.HTTP_400_BAD_REQUEST)

                    for row in data:
                        testcases.append(
                            TestCase(
                                question=question,
                                input_data=row.get("input", "").strip(),
                                expected_output=row.get("output", "").strip(),
                                is_hidden=str(row.get("hidden", "true")).lower() in ("true", "1"),
                                score=float(row.get("score", 0) or 0),
                            )
                        )
                else:
                    res = {
                        "status":"failed",
                        "message": "Unsupported file format (use .csv or .json)"
                    }
                    return Response(res, status=status.HTTP_400_BAD_REQUEST)

                TestCase.objects.bulk_create(testcases, batch_size=50)
                res = {
                    "status":"success",
                    "message": f"{len(testcases)} Testcases Uploaded"
                }
                
                return Response(res, status=status.HTTP_201_CREATED)

            # Add single testcase
            data = request.data.copy()
            data["question"] = question.id
            serializer = TestCaseSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                res = {
                    "status":"success",
                    "message": "Testcase Created"
                }
                return Response(res, status=status.HTTP_201_CREATED)
            
            
            res = {
                "status":"failed",
                "message": "Incorrect values Found",
                "errors": serializer.errors
            }
            return Response(res, status=status.HTTP_400_BAD_REQUEST)

        except CodingQuestion.DoesNotExist:
            res = {
                "status":"failed",
                "message": "Question Not Found"
            }
            return Response(res, status=status.HTTP_404_NOT_FOUND)