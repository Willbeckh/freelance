from django.contrib import admin
from .models import Message,Room,User,Job,Topic

# Register your models here.

admin.site.register(Message)
admin.site.register(Room)
admin.site.register(User)
admin.site.register(Job)
admin.site.register(Topic)