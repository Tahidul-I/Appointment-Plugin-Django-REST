from django.db import models
from django.contrib.auth.models import User
import uuid
import secrets

class ClientProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name="client_profile",blank=True,null=True)
    company_name = models.CharField(max_length=500)
    description = models.TextField(blank=True,null=True)
    address = models.TextField(blank=True,null=True)
    logo = models.TextField(blank=True,null=True)
    domain = models.CharField(max_length=700,unique=True)
    email = models.EmailField()
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    phone = models.CharField(max_length=30,blank=True,null=True)
    unique_key = models.TextField(blank=True,null=True,unique=True)
    created_at = models.DateTimeField(blank=True,null=True)
    staff_limit = models.IntegerField(default=5)
    using_auth_service = models.BooleanField(default=False)
    def save(self, *args, **kwargs):
        if not self.unique_key:
            self.unique_key =  self.generate_unique_key()
        while True:
            try:
                super(ClientProfile, self).save(*args, **kwargs)
                break  # Exit the loop if save is successful
            except:
                # Regenerate the unique key if a duplicate key error occurs
                self.unique_key = self.generate_unique_key()
                # Optionally log the collision and retry
                continue  # Retry saving with the new unique key
    
    def generate_unique_key(self):
        # Generate a unique key using uuid4
        self.unique_key = f"{secrets.token_hex(16)}-{uuid.uuid4()}".upper()
        unique_key = str(uuid.uuid4()).replace('-', '')+f"{secrets.token_hex(16)}".upper()
        # Convert to uppercase
        return unique_key.upper()
    
    def __str__(self):
        return self.company_name


class CompanyProfile(models.Model):
    client =  models.OneToOneField(ClientProfile,on_delete=models.CASCADE,related_name="company_profile")
    name = models.CharField(max_length=500)
    address = models.TextField()
    logo = models.TextField()
    description = models.TextField()

    def __str__(self):
        return self.name
    

# class ClientUSerInformation(models.Model):
#     client = models.ForeignKey(ClientProfile,on_delete=models.CASCADE,related_name="user_related_client")
#     name = models.CharField(max_length= 200)
#     email = models.CharField(max_length=100,unique=True)
#     password  = models.TextField()
#     otp = models.CharField(max_length=20)


# login url should be provided
# register url should be provided
# sending otp url should be provide
# forger password url should be provided
# Change password url should be  provided