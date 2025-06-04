from django.db import models
from profiles.models import Profile


class Address(models.Model):
    region = models.CharField(max_length=255, blank=True, null=True)
    province = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    barangay = models.CharField(max_length=255, blank=True, null=True)
    house_address = models.CharField(max_length=255, blank=True, null=True)
    zip_code = models.IntegerField()
    profile_id = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True, related_name='addresses', verbose_name='Profile')

    def __str__(self):
        return f"{self.region}, {self.province}, {self.city}, {self.barangay}, {self.house_address}, {self.zip_code}"
