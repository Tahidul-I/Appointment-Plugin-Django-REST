from django.db import models
from django.utils import timezone
# Create your models here.
class Order(models.Model):
    company_name = models.CharField(max_length=200)
    domain = models.TextField()
    email = models.EmailField()
    address = models.TextField()
    phone = models.CharField(max_length=200)
    country = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    total_amount = models.FloatField()
    is_successful = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)