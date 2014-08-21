from django.shortcuts import render
from smokesrv.models import User
from rest_framework import viewsets
from smokesrv.serializers import ResponseUserSerializer, UserSerializer
from django.core import serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.decorators import api_view

@api_view(['POST'])
def register_or_login(request):
    email = request.DATA['email']
    password = request.DATA['password']
    try :
        user = User.objects.get(email=email)
        if user.password != password :
            return Response(status=status.HTTP_400_BAD_REQUEST)
        response_serializer = ResponseUserSerializer(user)
        return Response(response_serializer.data)
    except User.DoesNotExist:
        u = User(email=email, friends_list = '', password=password) 
        u.save()
        response_serializer = ResponseUserSerializer(u) 
        return Response(response_serializer.data)

class UserList(APIView):
    
    def get(self, request, format=None):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
