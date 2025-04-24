from django.db import models
from django.contrib.auth.models import User
from ..client.models import ClientProfile
from ..services.models import ServiceRelatedStaff,ClientServices
from ..staff.models import StaffProfile
import uuid
from django.utils import timezone

# Create your models here.

class AppointmentBooking(models.Model):
    client = models.ForeignKey(ClientProfile,on_delete=models.CASCADE,related_name="appointment_related_client")
    staff = models.ForeignKey(StaffProfile,on_delete=models.CASCADE,related_name="appointment_related_staff")
    start_time_slot = models.TimeField(blank=True,null=True)
    end_time_slot = models.TimeField(blank=True,null=True)
    selected_date = models.DateField(blank=True,null=True)
    name = models.CharField(max_length=500)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    appointment_note = models.TextField(blank=True,null=True)
    total_amount = models.FloatField()
    track_id = models.CharField(max_length=900,blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_success = models.BooleanField(default=False)
    user_id = models.CharField(max_length=1000,blank=True,null=True)
    def save(self, *args, **kwargs):
        if not self.track_id:
            self.track_id = str(uuid.uuid4())  # Generate a new UUID if no track_id exists
        super(AppointmentBooking, self).save(*args, **kwargs) 


class AppointmentRelatedServices(models.Model):
    appointment = models.ForeignKey(AppointmentBooking,on_delete=models.CASCADE,related_name="appointment")
    service = models.ForeignKey(ClientServices,on_delete=models.CASCADE,related_name="appointment_related_service")