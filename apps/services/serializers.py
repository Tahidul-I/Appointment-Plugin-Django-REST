from rest_framework import serializers
from .models import *
from ..staff.models import StaffProfile
from ..schedule.serializers import *
class ClientServicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientServices
        fields = ['id','name','description','old_price','new_price','image_url','duration','total_minutes']

class ServiceRelatedStaffSerializer(serializers.ModelSerializer):
    staff_id = serializers.IntegerField(source='staff.id',read_only=True)
    name = serializers.CharField(source='staff.name',read_only=True)
    description = serializers.CharField(source = 'staff.description', read_only=True)
    image_url = serializers.URLField(source='staff.image_url',read_only=True)
    class Meta:
        model = ServiceRelatedStaff
        fields = ['staff_id','name','description','image_url']

class ClientServicesSerializerForSelect(serializers.ModelSerializer):
    class Meta:
        model = ClientServices
        fields = ['id','name']