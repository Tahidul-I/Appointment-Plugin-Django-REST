from rest_framework import serializers
from .models import *
from ..client.models import ClientProfile

class ClientCredentialSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username',read_only=True)
    is_active = serializers.BooleanField(source='user.is_active',read_only=True)
    class Meta:
        model = ClientProfile
        fields = ['id','company_name','domain','email','username','is_active','using_auth_service']