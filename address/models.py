from django.db import models
from profiles.models import Profile


class Address(models.Model):
    region = models.CharField(max_length=255)
    province = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    barangay = models.CharField(max_length=255)
    house_address = models.CharField(max_length=255)
    zip_code = models.IntegerField()
    profile_id = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.region}, {self.province}, {self.city}, {self.barangay}, {self.house_address}, {self.zip_code}"
