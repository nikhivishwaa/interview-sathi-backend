from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from accounts.models import User
from django.db.models import Q
import datetime as dt
import random as rd
from rest_framework.parsers import JSONParser
from rest_framework_simplejwt.tokens import RefreshToken
from accounts.serializers import RegisterSerializer, ProfileSerializer, ChangePasswordSerializer, ProfileUpdateSerializer
from accounts.models import User
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from rest_framework.generics import UpdateAPIView
from firebase_admin import auth as firebase_auth
from accounts.apps import firebase_app


class SignupViewSet(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            user = User.objects.filter(Q(phone=data.get('phone')) | Q(email=data.get('email')))
            if user.exists():
                response = {
                    'status': 'failed',
                    'message': 'User already exists',
                    'data': serializer.validated_data
                }
                return Response(response, status=status.HTTP_409_CONFLICT)
            else:
                user = serializer.save()
                print(user,"created successfully")
                response = {
                    'status': 'success',
                    'message': 'User registered successfully',
                    'data': {
                        "userId": user.id
                        }
                    }
                # sso login
                if user.verified:
                    refresh = RefreshToken.for_user(user)
                    user_data = ProfileSerializer(user).data
                    response['data']['refresh'] = str(refresh)
                    response['data']['access'] = str(refresh.access_token)
                    response['data']['user'] = user_data
            
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
        user = self.get_object()
        serializer = self.get_serializer(data=request.data)
        
        if serializer.is_valid():
            if not user.check_password(serializer.data.get('old_password')):
                response = {
                    'status': 'failed',
                    'message': 'Old password is incorrect'
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
            
            user.set_password(serializer.data.get('new_password'))
            user.save()
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

    def post(self, request):
        try:
            serializer = ProfileUpdateSerializer(data=request.data)
            if serializer.is_valid():
                data = serializer.validated_data
                user = request.user
                if user.phone != data['phone']:
                    try:
                        user = User.objects.get(phone=data.get('phone'))
                        response = {
                            "status":"failed",
                            "message":"Phone Number is Already Used. Try Another Number!",
                            "data":{}
                        }

                        return Response(response, status=status.HTTP_409_CONFLICT)
                    except Exception as e:
                        pass

                for key, value in data.items():
                    if hasattr(user, key):  # only set existing fields
                        setattr(user, key, value)
                user.save()
                p_serializer = ProfileSerializer(user)
                response = {
                    'status': 'success',
                    'message': 'Profile Updated Successfully',
                    'data': p_serializer.data
                }
                return Response(response, status=status.HTTP_202_ACCEPTED)
            else:
                response = {
                    'status': 'failed',
                    'message': 'Invalid Data',
                    'data': {},
                    'errors': serializer.errors
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            response = {
                'status': 'failed',
                'message': 'Something went Wrong!',
                'data': {},
            }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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
                    user_data = ProfileSerializer(user).data

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
                    return Response(response, status=status.HTTP_400_BAD_REQUEST)
            
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
    

class FirebaseLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        id_token = request.data.get("id_token")

        if not id_token:
            response = {
                    'status': 'failed',
                    'message': 'ID token is required',
                }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Verifying Firebase token
            decoded_token = firebase_auth.verify_id_token(id_token)
            print(decoded_token)
            uid = decoded_token["uid"]
            email = decoded_token.get("email")

        except Exception as e:
            response = {
                    'status': 'failed',
                    'message': 'Invalid Firebase token'
                }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        # Finding local user
        if email:
            try:
                user  = User.objects.get(email=email)
                refresh = RefreshToken.for_user(user)
                user_data = ProfileSerializer(user).data
            
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
            except User.DoesNotExist:
                response = {
                    'status': 'success',
                    'message': 'Complete the Signup'
                }

                print('new user with sso')
                return Response(response, status=status.HTTP_202_ACCEPTED)
