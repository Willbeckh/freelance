from django.db import models
from django.contrib.auth.models import AbstractUser,BaseUserManager,AbstractBaseUser,PermissionsMixin
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save
from rest_framework.authtoken.models import Token


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender,instance=None,created=False,**kwargs):
    if created:
        Token.objects.create(user=instance)

class UserManager(BaseUserManager):
    def create_user(self,email,username=None,password=None,**extrafields):
        if not email:
            raise ValueError('Please enter email before proceeding')
        user = self.model(username=username,email=self.normalize_email(email),**extrafields)
        user.set_password(password)
        user.save(using=self._db)
        return user
        
    def create_superuser(self,email,password,username=None):
        user = self.create_user(email,username,password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
        
        
class User(AbstractBaseUser,PermissionsMixin):
    username = models.CharField(max_length=255,unique=True,null=True)
    email = models.EmailField(max_length=255,unique=True)
    name = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    
    objects = UserManager()
    
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
    ('Premium', 'premmium')
)


class Job(models.Model):
    name = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    location = models.TextField(null=True, blank=True)
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


