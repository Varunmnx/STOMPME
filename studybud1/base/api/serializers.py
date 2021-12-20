from rest_framework.serializers import ModelSerializer
from base.models import Room

#objects cant be converted to json data 
class RoomSerializer(ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'