from django.db import models

# Create your models here.
class ImageUpload(models.Model):
    img = models.ImageField(upload_to='media/')

    def __str__(self):
        return f'{self.img}'