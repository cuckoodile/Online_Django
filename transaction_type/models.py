from django.db import models

# Create your models here.
class TransactionType(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        permissions = [
            ("can_view_transaction_type", "Can view transaction type"),
            ("can_add_transaction_type", "Can add transaction type"),
            ("can_edit_transaction_type", "Can edit transaction type"),
            ("can_delete_transaction_type", "Can delete transaction type"),
        ]

    def __str__(self):
        return self.name