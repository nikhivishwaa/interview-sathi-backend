from django.shortcuts import render
from django.http import JsonResponse

def home(request):
    return JsonResponse({"message":"welcome to interview sathi"},status=200)

# post of the profile
# take resume
# strt interview
# ask followup questions
# summarize interview
# give feed back