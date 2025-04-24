from django.db import models
from ..client.models import ClientProfile
from ..staff.models import StaffProfile
# Create your models here.
class StaffAccount(models.Model):
    client = models.ForeignKey(ClientProfile,on_delete=models.CASCADE,related_name="related_client_account")
    staff = models.ForeignKey(StaffProfile,on_delete=models.CASCADE,related_name="related_staff_account")
    username = models.CharField(max_length=100,unique=True)
    password = models.TextField()
    created_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

class GeneralUserAccount(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.TextField(blank=True,null=True)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)