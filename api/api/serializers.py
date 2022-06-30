from rest_framework.serializers import ModelSerializer
from api.models import Room, Job


class RoomSerializer(ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'


class JobSerializer(ModelSerializer):
    class Meta:
        model = Job
        fields = '__all__'
