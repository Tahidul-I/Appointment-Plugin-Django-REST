from rest_framework import serializers
from .models import *

class AppointmentRelatedServicesSerializer(serializers.ModelSerializer):
    service_name = serializers.CharField(source="service.name") 
    price = serializers.FloatField(source="service.new_price")
    banner_url = serializers.CharField(source="service.image_url")
    service_duration = serializers.CharField(source="service.duration")
    class Meta:
        model = AppointmentRelatedServices
        fields = ['service_name','price','banner_url','service_duration']



class BookingSerializer(serializers.ModelSerializer):
    staff_name = serializers.CharField(source='staff.name',read_only=True)
    user_name = serializers.CharField(source='name',read_only=True)
    user_email = serializers.EmailField(source='email',read_only=True)
    user_phone = serializers.CharField(source='phone',read_only=True)
    services = AppointmentRelatedServicesSerializer(source='appointment', many=True)
    class Meta:
        model = AppointmentBooking
        fields = ['id','staff_name','start_time_slot','end_time_slot','selected_date','user_name','user_email','user_phone','appointment_note','total_amount','created_at','services']

class UserBookingSerializer(serializers.ModelSerializer):
    staff_name = serializers.CharField(source='staff.name',read_only=True)
    user_name = serializers.CharField(source='name',read_only=True)
    user_email = serializers.EmailField(source='email',read_only=True)
    user_phone = serializers.CharField(source='phone',read_only=True)
    total_cost = serializers.CharField(source='total_amount',read_only=True)
    reservation_making_date = serializers.DateTimeField(source='created_at',read_only=True)
    scheduled_date = serializers.DateField(source='selected_date',read_only=True)
    services = AppointmentRelatedServicesSerializer(source='appointment', many=True)
    class Meta:
        model = AppointmentBooking
        fields = ['id','staff_name','start_time_slot','end_time_slot','user_name','user_email','user_phone','appointment_note','total_cost','scheduled_date','reservation_making_date','services']