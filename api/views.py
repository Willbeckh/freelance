from .serializers import UserSerializer,RoomSerializer,MessageSerializer,JobSerializer,TopicSerializer,ProfileSerializer,AuthTokenSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework import generics
from django.shortcuts import render, get_object_or_404



# local imports
from .models import User, Room, Message, Job, Topic, Profile
from .serializers import UserSerializer, RoomSerializer, MessageSerializer, JobSerializer, TopicSerializer, ProfileSerializer


class CreateUserView(generics.CreateAPIView):
    """
    this class generates the endpoint for viewing users
    """
    serializer_class = UserSerializer
    

    # method to get current authenticated user.
    def get_queryset(self):
        return super().get_queryset().filter(id=self.request.user.id)


class LoginView(ObtainAuthToken):
    """this class consumes the login serializer and generates the endpoint to login a user"""
    serializer_class = AuthTokenSerializer

    def post(self, request,*args,**kwargs):
        serializers = self.serializer_class(data=request.data,context={'request':request})
        serializers.is_valid(raise_exception=True)
        user = serializers.validated_data['user']
        token,created = Token.objects.get_or_create(user=user)
        return Response({
            'token':token.key,
            'username':user.username,
            'user_id':user.id,
            'email':user.email,
            'name':user.name
        })




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


    def post(self, request):
        response = Response()
        response.delete_cookie(key='refreshToken')
        response.data = {
            'message': 'success'
        }
        return response



class JobView(viewsets.ModelViewSet):
    """This class creates the endpoint to view a single job"""
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    
    def get(self, pk=None):
        job = get_object_or_404(self.queryset, id=pk)
        serializer = JobSerializer(job, many=False)
        return Response(serializer.data, content_type='application/json')