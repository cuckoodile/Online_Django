from django.db import models

# Create your models here.
class PaymentMethod(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        permissions = [
            ("can_view_payment_method", "Can view payment method"),
            ("can_add_payment_method", "Can add payment method"),
            ("can_edit_payment_method", "Can edit payment method"),
            ("can_delete_payment_method", "Can delete payment method"),
        ]

    def __str__(self):
        return self.name