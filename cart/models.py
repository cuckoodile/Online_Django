from django.db import models
from django.contrib.auth.models import User

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='carts', verbose_name='User', null=True, blank=True)
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE, related_name='carts', verbose_name='Product',null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        permissions = [
            ("can_view_cart", "Can view cart"),
            ("can_add_cart", "Can add cart"),
            ("can_edit_cart", "Can edit cart"),
            ("can_delete_cart", "Can delete cart"),
        ]

    def __str__(self):
        return f"Cart {self.id} - Created at {self.created_at}"