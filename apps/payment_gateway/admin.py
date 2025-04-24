from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(StripePaymentGateway)
admin.site.register(PaypalPaymentGateway)


