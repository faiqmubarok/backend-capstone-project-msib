from django.db import models
from django.contrib.auth.models import User

class Address(models.Model):
    province = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    sub_district = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.province}, {self.city}, {self.district}, {self.sub_district}, {self.postal_code}"

class Finance(models.Model):
    bank = models.CharField(max_length=100)
    no_rekening = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.bank}, {self.no_rekening}"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    name = models.CharField(max_length=100)
    no_ktp = models.CharField(max_length=16, null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    job = models.CharField(max_length=100, null=True, blank=True)
    address = models.OneToOneField(Address, on_delete=models.CASCADE)
    finance = models.OneToOneField(Finance, on_delete=models.CASCADE)
    photoProfile = models.ImageField(upload_to='profilePictures/', null=True, blank=True)
    last_update = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.user.email

