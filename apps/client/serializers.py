from rest_framework import serializers
from .models import *


class ClientProfileSerializerForClientDashboard(serializers.ModelSerializer):
    class Meta:
        model = ClientProfile
        fields = ['id','company_name','address','logo','description','email','domain','country','phone','city']

class ClientDetailSerializerForAdminDashboard(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username',read_only=True)
    is_active = serializers.BooleanField(source='user.is_active',read_only=True)
    class Meta:
        model = ClientProfile
        fields = ['id','company_name','address','logo','description','email','domain','country','phone','city','unique_key','staff_limit','username','is_active']

class ClientProfileSerializerForAdminDashboard(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username',read_only=True)
    is_active = serializers.BooleanField(source='user.is_active',read_only=True)
    class Meta:
        model = ClientProfile
        fields = ['id','company_name','email','domain','username','is_active']