from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255,unique=True)
    password = models.CharField(max_length=255)
    username = None
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f'{self.name}'


class Topic(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Room(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    participants = models.ManyToManyField(
        User, related_name='participants', blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.name


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.body[0:50]


# project tracking status
STATUS = (
    ('Available', 'available'),
    ('In Progress', 'in progress'),
    ('Canceled', 'canceled'),
    ('Done', 'done'),
    ('Premium', 'premium')
)


class Job(models.Model):
    name = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    location = models.CharField(max_length=80,null=True, blank=True)
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    description = models.TextField(null=True, blank=True)
    experience = models.TextField(null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=50, choices=STATUS, default='available')

    def __str__(self):
        return self.name


class Profile(models.Model):
    avatar = models.ImageField(null=True, default="avatar.svg")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.EmailField(unique=True, null=True)
    bio = models.TextField(null=True)

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.user


# Job tracking pipeline.
class JobPipeline(models.Model):
    
    job_details = models.ForeignKey(Job, on_delete=models.CASCADE, null=True) 
    applicants = models.ManyToManyField(User, related_name='applicants')
    date_added = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return str(self.job_details.name)