from django.contrib import admin
from . models import*
# Register your models here.
class ClientProfileAdmin(admin.ModelAdmin):
    model = ClientProfile
    exclude = ['password']

admin.site.register(ClientProfile, ClientProfileAdmin)