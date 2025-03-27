from django.shortcuts import render
from django.http import JsonResponse

def home(request):
    return JsonResponse({"message":"welcome to interview sathi"},status=200)
