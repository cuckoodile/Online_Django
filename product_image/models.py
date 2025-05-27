from django.db import models
from products.models import Product

# Create your models here.
class ImageUpload(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images', null=True, blank=True)
    img = models.ImageField(upload_to='media/')

    def __str__(self):
        return f'{self.img}'

    class Meta:
        permissions = [
            ("can_view_product_image", "Can view product image"),
            ("can_add_product_image", "Can add product image"),
            ("can_edit_product_image", "Can edit product image"),
            ("can_delete_product_image", "Can delete product image"),
        ]