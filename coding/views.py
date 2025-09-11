import csv
import io
import json
import httpx
import asyncio
from asgiref.sync import async_to_sync
from django.conf import settings
from django.core.cache import cache
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.db.models import Q
from coding.models import CodingQuestion, TestCase, Submission, SubmissionLog, CodingSolution, Language
from coding.serializers import CodingQuestionSerializer, TestCaseSerializer
from coding.caching import get_languages, get_testcases




class LanguagesAPIView(APIView):
    permission_classes = [AllowAny, IsAuthenticated]
    
    def get(self, request):
        try:
            _languages = get_languages()
        
            response = {
                'status': 'success',
                'message': 'Programming Languages',
                'data': _languages
            }
            return Response(response, status=status.HTTP_200_OK)
            
        except Exception as e:
            print(e)
            response = {
                'status': 'failed',
                'message': 'Unable to load Programming Languages',
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)



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


async def run_worker(payload):
    async with httpx.AsyncClient(timeout=30.0) as client:
        resp = await client.post(f"{settings.WORKER_URL}/execute/testcases", json=payload)
        print("Worker status:", resp.status_code)
        print("Worker body:", resp.text)

        return resp.json()


# Execution API's 
class CompileAndRunAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, ps_id):
        code = request.data.get("code")
        language_id = request.data.get("language")
        language = get_languages(language_id)

        # fetch visible testcases
        testcases = get_testcases(ps_id)

        payload = {
            "code": code,
            "language": language['name'],
            "testcases": testcases,
        }


        result = async_to_sync(run_worker)(payload)
        return Response(result)


from django.db import connection, transaction

class SubmitAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, ps_id):
        user = request.user
        question = get_object_or_404(
            CodingQuestion, id=ps_id, is_deleted=False, visibility="public"
        )

        code = request.data.get("code")
        language_id = request.data.get("language")
        language = get_object_or_404(Language, id=language_id)

        # create submission record
        submission = Submission.objects.create(
            user=user,
            question=question,
            code=code,
            language=language,
            status="In Progress",
            metadata={},
        )

        # fetch all testcases
        all_testcases = get_testcases(ps_id, include_hidden=True)

        payload = {
            "code": code,
            "language": language.name.lower(),
            "testcases": all_testcases,
        }
        results = async_to_sync(run_worker)(payload).get("results", [])

        # build rows for raw insert
        rows = []
        status_overall = "Accepted"
        for r in results:
            status_log = "Pass" if r["status"] == "Accepted" else "Failed"
            if status_log == "Failed":
                status_overall = "Rejected"

            rows.append(
                f"""({submission.id},{r["testcase"]},'{r["actual_output"]}','{r["stderr"]}',{r["time_taken"]},'{status_log}','{r["status"]}')"""
            )

        # raw SQL bulk insert + submission update
        with transaction.atomic(), connection.cursor() as cursor:
            if rows:
                cursor.execute(
                    f"""
                    INSERT INTO submission_logs
                    (submission_id, testcase_id, actual_output, stderr, time_taken, status, message)
                    VALUES {",".join(rows)}
                    """
                )

        # fetch only visible testcase logs
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT sl.id, sl.testcase_id, tc.input_data, tc.expected_output, tc.score, 
                    sl.actual_output, sl.stderr, sl.time_taken, sl.status, sl.message
                FROM submission_logs sl
                JOIN test_cases tc ON sl.testcase_id = tc.id
                WHERE sl.submission_id = %s AND tc.is_hidden = FALSE
                """,
                [submission.id],
            )
            visible_results = [
                {
                    "log_id": row[0],
                    "testcase": row[1],
                    "input_data":row[2],
                    "expected_output":row[3],
                    "score":row[4],
                    "actual_output": row[5],
                    "stderr": row[6],
                    "time_taken": row[7],
                    "status": row[8],
                    "message": row[9],
                }
                for row in cursor.fetchall()
            ]

        submission.status = status_overall
        submission.save()

        return Response(
            {"submission_id": submission.id, "results": visible_results}
        )

    
class CustomRunAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, ps_id):
        question = get_object_or_404(CodingQuestion, id=ps_id, is_deleted=False)

        user_code = request.data.get("code")
        language_id = request.data.get("language")
        custom_input = request.data.get("input")

        language = get_languages(language_id)

        # fetch standard solution
        std_sol = CodingSolution.objects.filter(question=question).first()
        if not std_sol:
            return Response({"error": "No standard solution available"}, status=400)

        # prepare payload for user code + std solution
        user_payload = {
            "code": user_code,
            "language": language['name'],
            "testcases": [{"id": "custom", "input_data": custom_input, "expected_output": ""}],
        }
        std_payload = {
            "code": std_sol.code,
            "language": std_sol.language.name.lower(),
            "testcases": [{"id": "custom", "input_data": custom_input, "expected_output": ""}],
        }

            
        async def run_both():
            async with httpx.AsyncClient(timeout=25) as client:
                user_resp, std_resp = await asyncio.gather(
                    client.post(f"{settings.WORKER_URL}/execute/testcases", json=user_payload),
                    client.post(f"{settings.WORKER_URL}/execute/testcases", json=std_payload),
                )
                return user_resp.json(), std_resp.json()

        user_resp, std_resp = async_to_sync(run_both)()

        user_output = user_resp["results"][0]["actual_output"]
        std_output = std_resp["results"][0]["actual_output"]

        return Response({
            "input": custom_input,
            "expected_output": std_output,
            "user_output": user_output
        })
