from smokesrv.models import User
from rest_framework import serializers

class FriendsListSerializer(serializers.Serializer):
    friends_list = serializers.Field(source='get_email_friends_list')

    class Meta:
        model = User
        fields = ('friends_list',)

class ResponseUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'email', 'gcm_id' )
        read_only_fields = ('id', 'email', 'password',)

class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'gcm_id', 'friends_list')


