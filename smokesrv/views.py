from django.shortcuts import render
from smokesrv.models import User
from rest_framework import viewsets
from smokesrv.serializers import ResponseUserSerializer, UserSerializer, FriendsListSerializer
from django.core import serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.decorators import api_view
from gcm.models import get_device_model
from SmokeServer import settings
import json
import requests

@api_view(['POST'])
def update_gcm(request):
    email = request.DATA['email']
    if request.DATA['gcm_id'] :
        try :
            user = User.objects.get(email=email)
            user.gcm_id = request.DATA['gcm_id']
            user.save()
            response_serializer = ResponseUserSerializer(user)
            return Response(response_serializer.data)
        except User.DoesNotExist:
           pass
    return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def smoke_request(request):
    if 'invited' in request.DATA and 'inviter' in request.DATA:
        invited = request.DATA['invited']
        try :
            invited_user = User.objects.get(email=invited)
            inviter = request.DATA['inviter']
            message = { "from" : inviter, "action" : "smoke" }
            resp = send_gcm_message(invited_user.gcm_id, message)
            if resp.status_code == 200:
                return Response(resp.text)
        except User.DoesNotExist:
            pass
    return Response(status=status.HTTP_400_BAD_REQUEST)

def send_gcm_message(reg_id, message, collapse_key=None):
    message = json.dumps(message)
    values = {
        'registration_ids': [reg_id],
        'data': {"message":str(message)}
    }   

    headers = {
        'UserAgent': "GCM-Server",
        'Content-Type': 'application/json',
        'Authorization': 'key=' + settings.GCM_API_KEY,
    }

    response = requests.post(url="https://android.googleapis.com/gcm/send",data=json.dumps(values), headers=headers)

    return response

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
        u = User(email=email,password=password) 
        u.save()
        response_serializer = ResponseUserSerializer(u) 
        return Response(response_serializer.data)

@api_view(['POST'])
def get_friends(request):
    email = request.DATA['email']
    try : 
        user = User.objects.get(email=email)
        response_serializer = FriendsListSerializer(user)
        return Response(response_serializer.data)
    except User.DoesNotExist:
        return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def add_friend(request):
    adder = request.DATA['adder']
    addee = request.DATA['addee']
    try :
        adder_user = User.objects.get(email=adder)
        addee_user = User.objects.get(email=addee)
        adder_user.friends_list += "," + str(addee_user.id)
        addee_user.friends_list += "," + str(adder_user.id)
        adder_user.massage()
        addee_user.massage()
        adder_user.save()
        addee_user.save()
        resp = ResponseUserSerializer(adder_user)
        return Response(resp.data)
    except User.DoesNotExist:
        return Response(status=status.HTTP_400_BAD_REQUEST)

class UserList(APIView):
    
    def get(self, request, format=None):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
