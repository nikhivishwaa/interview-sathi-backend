from django.urls import path, include
from coding import views

urlpatterns = [
    path('languages/', views.LanguagesAPIView.as_view(), name='all_programming_languages'),# GET
    path('ps/', views.ProblemsAPIView.as_view(), name='all_problem_statements'),# GET, POST
    path('ps/<int:ps_id>/', views.ProblemStatementUpdateAPIView.as_view(), name='problem_statement'), # GET, PUT, DELETE
    path('ps/<int:ps_id>/run/', views.CompileAndRunAPIView.as_view(), name='problem_statement'), # POST
    path('ps/<int:ps_id>/submit/', views.SubmitAPIView.as_view(), name='problem_statement'), # POST
    path('ps/<int:ps_id>/custom-input/', views.CustomRunAPIView.as_view(), name='test_cases'), # POST
    path('ps/<int:ps_id>/testcases/', views.TestCasesAPIView.as_view(), name='test_cases'), # GET(get public testcases) , POST(upload csv which have input, output, score)
    path('ps/<int:ps_id>/testcases/<int:testcase_id>/', views.TestCasesAPIView.as_view(), name='test_cases'), # GET, POST
]
