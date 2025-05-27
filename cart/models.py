from django.db import models

class Cart(models.Model):
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