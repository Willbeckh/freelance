from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUser
from django.utils.translation import gettext as _
from .models import User, Job, Room, Message, Topic, Profile, JobPipeline
# Register your models here.


class UserAdmin(BaseUser):
    ordering = ['id']
    list_display = ['id','email','username','name']
    list_display_links = ['id','email']
    fieldsets = (
        (None,{'fields':('username','email','password')}),
        (_('Personal Info'),{'fields':('name',)}),
        (_('Permissions'),{'fields':('is_active','is_staff','is_superuser')}),
        (_('Imp dates'),{'fields':('last_login',)})
    )
    add_fieldsets = (
        (None,{
            'classes':('wide'),
            'fields':('email','username','password1','password2') 
               }),
    )

admin.site.register(User,UserAdmin)
admin.site.register(Job)
admin.site.register(Message)
admin.site.register(Room)
admin.site.register(Topic)
admin.site.register(Profile)


# registers job pipeline to admin
class PipelineAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['job_details']}),
        ('Applicants', {'fields': ['applicants']})
    ]


admin.site.register(JobPipeline, PipelineAdmin)
