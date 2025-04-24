from django.db import models
from ..client.models import ClientProfile
from ..staff.models import StaffProfile
# Create your models here.
class ClientServices(models.Model):
    client = models.ForeignKey(ClientProfile,on_delete=models.CASCADE,related_name="client_services")
    name = models.CharField(max_length=500)
    description = models.TextField()
    is_free = models.BooleanField(default=False)
    old_price = models.FloatField()
    new_price = models.FloatField()
    image_url = models.TextField()
    duration = models.CharField()
    total_minutes = models.IntegerField()
    def __str__(self):
        return f"{self.client.name} | {self.name}"
    
class ServiceRelatedStaff(models.Model):
    service = models.ForeignKey(ClientServices,on_delete=models.CASCADE,related_name="related_service")
    staff = models.ForeignKey(StaffProfile,on_delete=models.CASCADE,related_name="related_staff")

    def __str__(self):
        return f"{self.service.client.name} | {self.service.name} | {self.staff.name}"