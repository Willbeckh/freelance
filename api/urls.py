
from django.urls import path, include
from .views import RegisterView,LoginView,UserView,LogoutView,RefreshView,MessageViewSet,RoomViewSet,JobViewSet,TopicViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register('messages', MessageViewSet)
router.register('rooms', RoomViewSet)
router.register('jobs', JobViewSet)
router.register('topic', TopicViewSet)


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('user/', UserView.as_view(), name='user'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('refresh/', RefreshView.as_view(), name='refresh'),
    path('', include(router.urls))
]
