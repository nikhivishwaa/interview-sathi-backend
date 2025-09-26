import httpx
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.conf import settings


class JobsAPIView(APIView):
    permission_classes = [AllowAny]

    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/11',
        'systemid':settings.JOBS_API_APP_ID,
        'clientid':settings.JOBS_API_CLIENT_ID,
        'Appid':settings.JOBS_API_APP_ID
    }

    def fetch_jobs(self, role: str = 'frontend', page_no: int = 1):
        keyword = role.replace(' ', '%20')
        seo_key = role.replace(' ', '-') + f'-{page_no}' if page_no > 1 else ''
        url = f"{settings.JOBS_API}?noOfResults=20&urlType=search_by_keyword&searchType=adv&keyword={keyword}{f'&pageNo={page_no}' if page_no>1 else ''}&seoKey={seo_key}-jobs&src=popular_roles_homepage_srch&latLong="

        response = httpx.get(url, headers=self.HEADERS, timeout=15)
        response.raise_for_status()
        jobs_data = response.json()

    def get(self, request):
        role = request.query_params.get('role', 'data scientist')
        page_no = int(request.query_params.get('pageNo', 1))

        try:
            jobs_data = self.fetch_jobs(role, page_no)
            response = {
                'status': 'success',
                'message': f'Jobs for "{role}" (page {page_no})',
                'data': jobs_data.get('jobDetails',[])
            }
            return Response(response, status=status.HTTP_200_OK)

        except httpx.HTTPStatusError as e:
            return Response(
                {'status': 'failed', 'message': f'API returned {e.response.status_code}'},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            res = {'status': 'failed', 'message': f'Unable to load jobs: {str(e)}'}
            return Response(res, status=status.HTTP_400_BAD_REQUEST)