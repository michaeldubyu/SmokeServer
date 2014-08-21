from smokesrv.models import User
from rest_framework import serializers

class ResponseUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'email', 'friends_list' )
        read_only_fields = ('id', 'email', 'password',)

class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ('id', 'email', 'password')
