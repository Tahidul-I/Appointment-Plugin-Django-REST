from rest_framework import serializers
from .models import *
from ..schedule.models import StaffSchedule
class StaffProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaffProfile
        fields = ['id','name','description','image_url']

class StaffRecommendationSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaffProfile
        fields = ['id','name','image_url']

class SelectedStaffScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaffSchedule
        fields = ['scheduled_date']