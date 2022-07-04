from django.contrib import admin

from .models import User, Job, Room, Message, Topic, Profile, JobPipeline


# Register your models here.
admin.site.register(User)
admin.site.register(Job)
admin.site.register(Message)
admin.site.register(Room)
admin.site.register(Topic)
admin.site.register(Profile)


# registers job pipeline to admin
class PipelineAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['author']}),
        ('Title', {'fields': ['job_title']}),
        ('Status', {'fields': ['job_status']}),
        ('Applicants', {'fields': ['applicants']}),
    ]


admin.site.register(JobPipeline, PipelineAdmin)
