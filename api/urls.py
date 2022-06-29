from django.urls import re_path,path,include
from .views import RegisterView



urlpatterns = [
    path('register/', RegisterView.as_view()),
    
]