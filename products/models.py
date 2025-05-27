from django.db import models
from django.contrib.auth.models import User
from categories.models import Category
from transactions.models import Transaction

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=255, unique=True)
    publisher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products', verbose_name='Publisher ID')
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    @property
    def stock(self):
        inbound = Transaction.objects.filter(product=self, transaction_type__id=1).aggregate(models.Sum('quantity'))['quantity__sum'] or 0
        outbound = Transaction.objects.filter(product=self, transaction_type__id=2).aggregate(models.Sum('quantity'))['quantity__sum'] or 0
        return inbound - outbound