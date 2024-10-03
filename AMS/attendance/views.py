from django.shortcuts import render,HttpResponse
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view,APIView,permission_classes
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.hashers import make_password,check_password
from .models import Admin,Teacher,Students
from datetime import datetime 

# Create your views here.
def get_token(user):
    refresh = RefreshToken.for_user(user)
    return{
        'refresh':str(refresh),
        'access':str(refresh.access_token),
    }

@api_view(['POST'])
def signup(request):
    name = request.data.get('name')
    role = request.data.get('role')
    username = request.data.get('username')
    password = request.data.get('password')

    if not name or not role or not username or not password:
        return Response({"error":"Please provide all required feilds"},
        status=status.HTTP_400_BAD_REQUEST)
    
    if User.objects.filter(username=username).exists():
        return Response({"error":"User already exits"},
        status=status.HTTP_400_BAD_REQUEST)
    #create new user
    user = User.objects.create_user(username=username,password=password)
    
    #create new admin/teacher
    teacher = Teacher(user=user,name=name,role=role)
    admin = Admin(user=user,name=name,role=role)
    teacher.save()
    admin.save()

    #generating token
    tokens = get_token(user)
    return Response({"success":True,"tokens":tokens})

@api_view(['POST'])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')

    print(f"username:{username}")
    
    try:
        user = User.objects.get(username=username)
        if user.check_password(password):
            token = get_token(user)
            return Response(token,status=status.HTTP_200_OK)
        else:
            return Response({"error":"invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)
    except User.DoesNotExist:
        return Response({"error":"user not found"},status=status.HTTP_400_BAD_REQUEST)
    
    

         
