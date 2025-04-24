from django.db import models
from ..client.models import ClientProfile

# Create your models here.
class StripePaymentGateway(models.Model):
    client = models.ForeignKey(ClientProfile,on_delete=models.CASCADE,related_name="stripe_payment_related_client")
    stripe_secret_key = models.TextField() #This will contain encrypted stripe secret key

class PaypalPaymentGateway(models.Model):
    client = models.ForeignKey(ClientProfile,on_delete=models.CASCADE,related_name="paypal_payment_related_client")
    paypal_credentials = models.TextField() # This will conatain an encrypted string which will return both the paypal client id and paypal secret
