from django.db import models
from ..client.models import ClientProfile
# Create your models here.

class StaffProfile(models.Model):
    client = models.ForeignKey(ClientProfile,on_delete=models.CASCADE,related_name="client_staff")
    name = models.CharField(max_length=300)
    description = models.TextField()
    image_url = models.TextField()

    def __str__(self):
        return f"{self.client.company_name} | {self.name}"