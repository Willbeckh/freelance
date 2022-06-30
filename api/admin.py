from django.contrib import admin

from .models import User, Job, Room, Message, Topic, Profile
# Register your models here.


admin.site.register(User)
admin.site.register(Job)
admin.site.register(Message)
admin.site.register(Room)
admin.site.register(Topic)
admin.site.register(Profile)

