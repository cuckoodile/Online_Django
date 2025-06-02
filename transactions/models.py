from django.db import models
from django.contrib.auth.models import User
from address.models import Address

# Create your models here.
class TransactionStatus(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name
    
class TransactionMethod(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name
    
class TransactionType(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name
    
class ProductTransaction(models.Model):
    transaction = models.ForeignKey('Transaction', on_delete=models.CASCADE, related_name='product_transactions')
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE, related_name='product_transactions')
    quantity = models.PositiveIntegerField(default=1)
    subtotal = models.DecimalField(max_digits=8, decimal_places=2)

    def save(self, *args, **kwargs):
        self.subtotal = self.product.price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in Transaction #{self.transaction.id}"

class Transaction(models.Model):
    status = models.ForeignKey(TransactionStatus, on_delete=models.PROTECT, related_name='transactions')
    payment_method = models.ForeignKey(TransactionMethod, on_delete=models.PROTECT, null=True, blank=True)
    type = models.ForeignKey(TransactionType, on_delete=models.PROTECT, related_name='transactions')
    products = models.ManyToManyField('products.Product', through='ProductTransaction', related_name='transactions')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # AUTOMATIC
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions', editable=False)
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, blank=True, editable=False)

    def __str__(self):
        return f"Transaction #{self.id} - {self.type.name} (User: {self.user.username})"