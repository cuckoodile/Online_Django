from django.db import models
from products.models import Product

class ProductSpecification(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_specifications')
    details = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        permissions = [
            ("can_view_product_specification", "Can view product specification"),
            ("can_add_product_specification", "Can add product specification"),
            ("can_edit_product_specification", "Can edit product specification"),
            ("can_delete_product_specification", "Can delete product specification"),
        ]

    def __str__(self):
        return f"Specs for {self.product.name}"
