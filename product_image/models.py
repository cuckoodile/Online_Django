from django.db import models
from products.models import Product

# Create your models here.
class ImageUpload(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images', null=True, blank=True)
    img = models.ImageField(upload_to='media/')

    def __str__(self):
        return f'{self.img}'