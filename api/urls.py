
from django.urls import path, include
# from .views import  LoginView, MessageViewSet, RoomViewSet, JobViewSet, TopicViewSet, ProfileViewSet,CreateUserView
from .views import *
from rest_framework import routers

router = routers.DefaultRouter()
router.register('messages', MessageViewSet)
router.register('rooms', RoomViewSet)
router.register('jobs', JobViewSet, basename='jobs')
router.register('topic', TopicViewSet)
router.register('profile', ProfileViewSet)


urlpatterns = [
    path('signup/',CreateUserView.as_view()),
    path('login/',LoginView.as_view(),name='login'),
    path('job/<int:pk>/',JobView.as_view({'get':'retrieve'}),name='job'),
    path('',include(router.urls))
]
