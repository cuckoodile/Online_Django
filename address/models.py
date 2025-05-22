from django.db import models
from django.contrib.auth.models import User
from django.db import models

class Address(models.Model):
    region = models.CharField(max_length=255)
    province = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    barangay = models.CharField(max_length=255)
    house_address = models.CharField(max_length=255)
    zip_code = models.IntegerField()
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return self
