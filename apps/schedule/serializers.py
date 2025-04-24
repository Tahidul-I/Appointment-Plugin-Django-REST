from rest_framework import serializers
from .models import *

class AvailableTimeSerializer(serializers.ModelSerializer):
    start_time = serializers.SerializerMethodField()
    class Meta:
        model = AvailableTime
        fields = ['id','start_time','is_booked']
    def get_start_time(self, obj):
        # Format `start_time` to "HH:MMAM/PM"
        return obj.time_slot.strftime('%I:%M%p')

class AvailableDatesSerializer(serializers.ModelSerializer):
    date_related_time = AvailableTimeSerializer(many=True, read_only=True)
    class Meta:
        model = AvailableDates
        fields = ['id','available_date','date_related_time']


class AvailableDatesSerializerForPlugin(serializers.ModelSerializer):
    date_related_time = serializers.SerializerMethodField()

    class Meta:
        model = AvailableDates
        fields = ['id', 'available_date', 'date_related_time']

    def get_date_related_time(self, obj):
        # Fetch only the times where on_hold is False
        token = self.context.get('token')
        if token:
            available_times = obj.date_related_time.filter(
                models.Q(on_hold=False) | models.Q(on_hold=True, on_hold_for=token)
            )
        else:
            available_times = obj.date_related_time.filter(on_hold=False)
        return AvailableTimeSerializer(available_times, many=True).data
    

class StaffScheduleSerializer(serializers.ModelSerializer):
    shift_starts = serializers.SerializerMethodField()
    shift_ends = serializers.SerializerMethodField()
    break_time_starts = serializers.SerializerMethodField()
    break_time_ends = serializers.SerializerMethodField()

    class Meta:
        model = StaffSchedule
        fields = '__all__'

    def get_shift_starts(self, obj):
        return obj.shift_starts.strftime("%I:%M%p")

    def get_shift_ends(self, obj):
        return obj.shift_ends.strftime("%I:%M%p")

    def get_break_time_starts(self, obj):
        return obj.break_time_starts.strftime("%I:%M%p") if obj.break_time_starts else None

    def get_break_time_ends(self, obj):
        return obj.break_time_ends.strftime("%I:%M%p") if obj.break_time_ends else None


class StaffScheduleSerializerForPlugin(serializers.ModelSerializer):
    class Meta:
        model = StaffSchedule
        fields = ['scheduled_date']