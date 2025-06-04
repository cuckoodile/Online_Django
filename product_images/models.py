from django.db import models

# Create your models here.
class ImageUpload(models.Model):
    img = models.ImageField(upload_to='/media/product_images', verbose_name='Product Image', null=True, blank=True)
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE, related_name='images', verbose_name='Product')

    def __str__(self):
        return f'{self.img}'