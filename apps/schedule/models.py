from django.db import models
from ..staff.models import StaffProfile
from ..client.models import ClientProfile
from django.utils.dateparse import parse_date
from datetime import datetime, timedelta
class AvailableDates(models.Model):
    client = models.ForeignKey(ClientProfile,on_delete=models.CASCADE,related_name="date_related_client")
    staff = models.ForeignKey(StaffProfile,on_delete=models.CASCADE,related_name="date_related_staff")
    available_date = models.CharField(max_length=200)
    month = models.CharField(max_length=500)
    day = models.CharField(max_length=500)
    year = models.CharField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Parse the date string from the available_date field
        parsed_date = parse_date(self.available_date)  # Converts "2024-08-22" to a date object

        if parsed_date:
            # Extract the day, month, and year
            self.day = str(parsed_date.day)
            self.month = parsed_date.strftime('%m')  # Get the month as a two-digit string, e.g., "08"
            self.year = str(parsed_date.year)

        # Call the parent class's save method to save the data to the database
        super(AvailableDates, self).save(*args, **kwargs)
        
    def __str__(self):
        return f"{self.staff.client.name} | {self.staff.name} | {self.available_date}"

class AvailableTime(models.Model):
    date_object = models.ForeignKey(AvailableDates,on_delete=models.CASCADE,related_name="date_related_time")
    time_slot = models.TimeField(blank=True,null=True)
    is_booked = models.BooleanField(default=False)
    on_hold = models.BooleanField(default=False)
    hold_time = models.DateTimeField(null=True, blank=True)
    on_hold_for = models.CharField(max_length=10000,blank=True,null=True) 

    def __str__(self):
        return f"{self.date_object.staff.client.name} | {self.date_object.staff.name} | {self.date_object.available_date}"

# class DateManagement(models.Model):
#     browser_token = models.TextField(blank=True,null=True)
#     staff = models.ForeignKey(StaffProfile,on_delete=models.CASCADE,related_name="selected_staff_from_browser")
#     client = models.ForeignKey(ClientProfile,on_delete=models.CASCADE,related_name="selected_staff_related_client")
#     related_date = models.DateTimeField(blank=True,null=True)


# class DateRelatedTimeManagement(models.Model):
#     date_obj = models.ForeignKey(DateManagement,on_delete=models.CASCADE,related_name="related_time")
#     time_slot = models.TimeField(blank=True,null=True)
#     is_booked = models.BooleanField(default=False)
#     hold_time = models.DateTimeField(null=True, blank=True)
#     on_hold_for = models.CharField(max_length=10000,blank=True,null=True)  


class StaffSchedule(models.Model):
    client = models.ForeignKey(ClientProfile,on_delete=models.CASCADE,related_name="schedule_related_client")
    staff = models.ForeignKey(StaffProfile,on_delete=models.CASCADE,related_name="schedule_related_staff")
    scheduled_date = models.DateField()
    shift_starts = models.TimeField()
    shift_ends = models.TimeField()
    break_time_starts = models.TimeField(blank=True,null=True)
    break_time_ends = models.TimeField(blank=True,null=True)

class BaseTimeSlot(models.Model):
    client = models.ForeignKey(ClientProfile,on_delete=models.CASCADE,related_name="base_time_related_client")
    staff = models.ForeignKey(StaffProfile,on_delete=models.CASCADE,related_name="base_time_related_staff")
    date_str = models.DateField()
    start = models.TimeField()
    end = models.TimeField()
    created_at = models.DateTimeField()
    duration = models.IntegerField()

    def save(self, *args, **kwargs):
        # Combine date and start time to calculate the end time
        start_datetime = datetime.combine(self.date_str, self.start)
        end_datetime = start_datetime + timedelta(minutes=self.duration)
        
        # Set the end time to the calculated time
        self.end = end_datetime.time()
        
        # Call the original save method
        super().save(*args, **kwargs)


class OnHoldTimeSlots(models.Model):
    client = models.ForeignKey(ClientProfile,on_delete=models.CASCADE,related_name="hold_time_related_client")
    staff = models.ForeignKey(StaffProfile,on_delete=models.CASCADE,related_name="hold_time_related_staff")
    date_schedule = models.DateField(blank=True,null=True)
    time_slot = models.TimeField(blank=True,null=True)
    on_hold_for = models.TextField(blank=True,null=True)
    created_at = models.DateTimeField(blank=True,null=True)
