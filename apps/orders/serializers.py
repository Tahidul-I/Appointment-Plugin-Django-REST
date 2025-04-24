from rest_framework import serializers
from ..orders.models import Order

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id','company_name','domain','email','created_at']

class OrderDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id','company_name','domain','email','address','phone','country','city','total_amount','created_at']