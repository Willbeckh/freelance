from rest_framework import serializers
from .models import User, Topic, Room, Job, Message, Profile
from django.contrib.auth import get_user_model,authenticate
from django.contrib.auth.hashers import make_password

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'name', 'email', 'password']
        extra_kwargs = {
            'password': {
                'write_only': True,
                'min_length':8
                }
        }

    def create(self, validate_data):
        return get_user_model().objects.create_user(**validate_data)


class AuthTokenSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(
        style = {'input_type' : 'password'},
        trim_whitespace = False
    )
    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        
        user = authenticate(request = self.context.get('request'),email = email,password = password)
        if not user:
            raise serializers.ValidationError('Invalid credentials')
        attrs['user'] = user
        return attrs


class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = ['name']


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['id', 'name', 'description', 'created',
                  'updated', 'host', 'topic', 'participants']


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'user', 'room', 'body', 'created', 'updated']


class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = ['id', 'name', 'company', 'location', 'created',
                  'updated', 'host', 'description', 'experience', 'status']


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'avatar', 'email', 'bio', 'user']
