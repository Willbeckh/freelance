import datetime
from django.shortcuts import render
import jwt
from .serializers import UserSerializer,RoomSerializer,MessageSerializer,JobSerializer,TopicSerializer,ProfileSerializer
from rest_framework.views import APIView
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.authentication import get_authorization_header
from rest_framework.response import Response
from rest_framework import viewsets, permissions
from rest_framework_swagger.views import get_swagger_view


# local imports
from .models import User, Room, Message, Job, Topic, Profile
from .serializers import UserSerializer, RoomSerializer, MessageSerializer, JobSerializer, TopicSerializer, ProfileSerializer
from .authentication import create_access_token, create_refresh_token, decode_access_token, decode_refresh_token


# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    """
    this class generates the endpoint for viewing users
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # permission_classes = [permissions.IsAuthenticated]

    # method to get current authenticated user.
    def get_queryset(self):
        return super().get_queryset().filter(id=self.request.user.id)


class RegisterView(APIView):
    """this class consumes the register serializer and generates the endpoint to register a user"""

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class LoginView(APIView):
    """this class consumes the login serializer and generates the endpoint to login a user"""

    def post(self, request):
        email = request.data['email']
        password = request.data['password']
        user = User.objects.filter(email=email).first()
        
        if user is None:
            raise(AuthenticationFailed('User not found'))

        if not user.check_password(password):
            raise(AuthenticationFailed('Incorrect Password'))

        payload = {
            'id':user.id,
            'exp':datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat':datetime.datetime.utcnow()
        }
        token = jwt.encode(payload,'secret',algorithm='HS256')
        response = Response()
        response.set_cookie(key='jwt',value=token,httponly=True)
        response.data = {
            'jwt':token
        }
        return response


class UserView(APIView):
    """this class consumes the user serializer and generates the endpoint to get the user details"""

    def get(self, request):
        token = request.COOKIES.get('jwt')
        
        if not token:
            raise(AuthenticationFailed('Unauthenticated!'))
        
        try:
            payload = jwt.decode(token,'secret',algorithms=['HS256'])
            
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated')
        
        user = User.objects.filter(id=payload['id']).first()
        serializer = UserSerializer(user)
        return Response(serializer.data)


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer


class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer


class JobViewSet(viewsets.ModelViewSet):
    serializer_class = JobSerializer

    def get_queryset(self):
        jobs = Job.objects.all()
        return jobs

    def retrieve(self, request, *args, **kwargs):
        params = kwargs
        jobs = Job.objects.filter(name=params['pk'])
        serializer = JobSerializer(jobs, many=True)
        return Response(serializer.data)


class TopicViewSet(viewsets.ModelViewSet):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer


class ProfileViewSet(viewsets.ModelViewSet):
    """This class creates the endpoint to view all availlable jobs"""
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    # get profile
    def get_queryset(self):
        """gets the profile for current user."""
        return Profile.objects.filter(user=self.request.user.id)


class RefreshView(APIView):
    def post(self, request):
        refresh_token = request.COOKIES.get('refreshToken')
        id = decode_refresh_token(refresh_token)
        access_token = create_access_token(id)
        return Response({
            'token': access_token
        })


class LogoutView(APIView):
    """
    This class sends a logout request to the server for the current authenticated user
    """

    def post(self, request):
        response = Response()
        response.delete_cookie(key='refreshToken')
        response.data = {
            'message': 'success'
        }
        return response


# swagger api
schema_view = get_swagger_view(title="Freelance API")
