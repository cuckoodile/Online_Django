from django.db import models
from django.contrib.auth.models import User
from transaction_type.models import TransactionType
from transaction_method.models import PaymentMethod
from transaction_status.models import TransactionStatus
from address.models import Address

# Create your models here.
class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    status = models.ForeignKey(TransactionStatus, on_delete=models.PROTECT, related_name='transactions')
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.PROTECT, null=True, blank=True)
    transaction_type = models.ForeignKey(TransactionType, on_delete=models.PROTECT, related_name='transactions')
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, blank=True)
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE, related_name='transactions', null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_void = models.BooleanField(default=False)
    amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    reference = models.CharField(max_length=100, blank=True)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"Transaction #{self.id} - {self.transaction_type.name} (User: {self.user.username})"

    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['user', 'timestamp']),
            models.Index(fields=['status']),
            models.Index(fields=['transaction_type']),
        ]
        verbose_name = "Transaction"
        verbose_name_plural = "Transactions"