from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from accounts.models import User
from django.db.models import Q
import datetime as dt
import random as rd
from rest_framework.parsers import JSONParser
from rest_framework_simplejwt.tokens import RefreshToken
from accounts.serializers import LoginSerializer, RegisterSerializer, ProfileSerializer, ChangePasswordSerializer
from accounts.models import User
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status

from rest_framework.generics import UpdateAPIView



class SignupViewSet(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        print(type(serializer))
        if serializer.is_valid():
            data = serializer.validated_data
            user = User.objects.filter(Q(phone=data.get('phone')) | Q(email=data.get('email')))
            if user.exists():
                response = {
                    'status': 'failed',
                    'message': 'User already exists',
                    'data': serializer.validated_data
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
            else:
                user = serializer.save()
                print(user,"created successfully")
                response = {
                    'status': 'success',
                    'message': 'User registered successfully',
                    }
                return Response(response, status=status.HTTP_201_CREATED)
            
        response = {
            'status': 'failed',
            'message': 'User registration failed',
            'errors': serializer.errors
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

class ChangePasswordView(UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = [IsAuthenticated]
    
    def get_object(self, queryset=None):
        obj = self.request.user
        return obj
    
    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)
        
        if serializer.is_valid():
            if not self.object.check_password(serializer.data.get('old_password')):
                response = {
                    'status': 'failed',
                    'message': 'Old password is incorrect'
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
            
            self.object.set_password(serializer.data.get('new_password'))
            self.object.save()
            response = {
                'status': 'success',
                'message': 'Password updated successfully'
            }
            return Response(response, status=status.HTTP_200_OK)
        
        response = {
            'status': 'failed',
            'message': 'Password update failed',
            'errors': serializer.errors
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)


class ProfileViewSet(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        print(request.user)
        if request.user:
            serializer = ProfileSerializer(request.user)
            response = {
                'status': 'success',
                'message': 'User detail',
                'data': serializer.data
            }
            return Response(response, status=status.HTTP_200_OK)
            
        response = {
            'status': 'failed',
            'message': 'User profile failed',
            'errors': serializer.errors
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)


class LoginViewSet(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        print(request)
        email = request.data.get('email').lower()
        password = request.data.get('password')
        user = None
        if email and password:
            try:
                if email.isnumeric():
                    user = User.objects.get(phone=email)
                else:
                    user = User.objects.get(email=email)

                # now check credentials   
                if user and user.check_password(password):
                    refresh = RefreshToken.for_user(user)
                    user_data = LoginSerializer(user).data

                    response = {
                        'status': 'success',
                        'message': 'User logged in successfully',
                        'data': {
                            'refresh': str(refresh),
                            'access': str(refresh.access_token),
                            'user': user_data,
                        }
                    }

                    print('user', user, 'logged in')
                    return Response(response, status=status.HTTP_200_OK)
                else:
                    response = {
                        'status': 'failed',
                        'message': 'Invalid Credentials'
                    }
                    return Response(response, status=status.HTTP_404_NOT_FOUND)
            
            except User.DoesNotExist:
                print("error")
                response = {
                    'status': 'failed',
                    'message': 'User does not exist'
                }
                return Response(response, status=status.HTTP_404_NOT_FOUND)
            
        response  = {
            'status': 'failed',
            'message': 'Please provide both mobile no./email and password'
        }
        
        return Response(response, status=status.HTTP_400_BAD_REQUEST)