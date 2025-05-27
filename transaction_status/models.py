from django.db import models

# Create your models here.
class TransactionStatus(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        permissions = [
            ("can_view_transaction_status", "Can view transaction status"),
            ("can_add_transaction_status", "Can add transaction status"),
            ("can_edit_transaction_status", "Can edit transaction status"),
            ("can_delete_transaction_status", "Can delete transaction status"),
        ]

    def __str__(self):
        return self.name