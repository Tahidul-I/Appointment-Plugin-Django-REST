from django.db import models
from ..client.models import ClientProfile
# Create your models here.
class AuthServiceUser(models.Model):
    client = models.ForeignKey(ClientProfile,on_delete=models.CASCADE,related_name="auth_service_client")
    name = models.CharField(max_length=500)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20,blank=True,null=True)
    password = models.TextField()
    is_active = models.BooleanField(default=False)
