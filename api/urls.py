
from django.urls import path, include
from rest_framework import routers
from .views import *
from drf_yasg import openapi
from drf_yasg.views import get_schema_view as swagger_get_schema_view



# swgger documentation
schema_view = swagger_get_schema_view(
    openapi.Info(
        title='Freelance API',
        default_version='v1',
        description='Freelance market API documentation',
        contact=openapi.Contact(email="freelance.dev@gmail.com"),
    ),
    public=True,
)

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
    path('',include(router.urls)),
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-schema'),
]
