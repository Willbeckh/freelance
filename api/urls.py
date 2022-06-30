
from django.urls import path, include
from .views import RegisterView,LoginView,UserView,LogoutView,RefreshView,MessageViewSet,RoomViewSet,JobViewSet,TopicViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register('messages',MessageViewSet)
router.register('rooms',RoomViewSet)
router.register('jobs',JobViewSet)
router.register('topic',TopicViewSet)



urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/',LoginView.as_view()),
    path('user/',UserView.as_view()),
    path('logout/',LogoutView.as_view()),
    path('refresh/',RefreshView.as_view()),
    path('',include(router.urls))
]

