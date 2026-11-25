from django.shortcuts import render
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterSerializer
from rest_framework.throttling import ScopedRateThrottle

class LoginAPIView(APIView):
  #override the default settings.py/rest_framework config here
  authentication_classes = []
  permission_classes = []  
  throttle_classes = [ScopedRateThrottle]
  throttle_scope = 'login' #used to identify which request limit should be applied to a particular API view.

# check if throttling works or not
  # def get_throttles(self):
  #   print("Throttle scope:", self.throttle_scope)
  #   print("Throttle classes:", self.throttle_classes)
  #   return super().get_throttles()
  
  def post(self,request):   
    print("Login API called")
    username = request.data.get('username')
    password = request.data.get('password')
    
    user = authenticate(username = username, password = password)
    if user is not None:
      token, created= Token.objects.get_or_create(user = user)
      return Response({'Token': token.key})
    return Response({'error': 'Invalid Credentials.'}, status=status.HTTP_401_UNAUTHORIZED)

class UserRegistration(APIView):
  authentication_classes = []
  permission_classes = []
  
  def post(self,request):
    serializer = RegisterSerializer(data = request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response({'message':"User Created Successfully."},status= status.HTTP_201_CREATED)
    
  
class LogoutAPIView(APIView):
  def post(self,request):
    # print(request.auth)
    request.auth.delete()
    return Response({'message': "User logout successfully"})
    