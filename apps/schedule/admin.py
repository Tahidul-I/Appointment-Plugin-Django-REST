from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(StaffSchedule)
admin.site.register(OnHoldTimeSlots)
admin.site.register(BaseTimeSlot)