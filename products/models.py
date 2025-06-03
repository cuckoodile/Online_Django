from django.db import models
from django.contrib.auth.models import User
from categories.models import Category
from transactions.models import Transaction

class SpecificationName(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name}"
    
class Specification(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='specifications')
    name = models.ForeignKey(SpecificationName, on_delete=models.CASCADE, related_name='specifications')
    value = models.CharField(max_length=100)

    class Meta:
        unique_together = ('product', 'name', 'value')

    def __str__(self):
        return f"{self.name.name}: {self.value} for {self.product.name}"
    
class Product(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    price = models.DecimalField(max_digits=10, decimal_places=2)

    # Automatic fields
    publisher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products', verbose_name='Publisher ID')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def stock(self):
        from transactions.models import ProductTransaction
        inbound = ProductTransaction.objects.filter(product=self, transaction__type__id=1).aggregate(models.Sum('quantity'))['quantity__sum'] or 0
        outbound = ProductTransaction.objects.filter(product=self, transaction__type__id=2).aggregate(models.Sum('quantity'))['quantity__sum'] or 0
        return inbound - outbound
    
    def __str__(self):
        return self.name

    class Meta:
        permissions = [
            ("can_view_product", "Can view product"),
            ("can_add_product", "Can add product"),
            ("can_edit_product", "Can edit product"),
            ("can_delete_product", "Can delete product"),
        ]

class ProductComment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    rating = models.PositiveSmallIntegerField()
    comment_id = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Comment by {self.user} on {self.product}: {self.comment[:20]}"

    class Meta:
        permissions = [
            ("can_view_product_review", "Can view product review"),
            ("can_add_product_review", "Can add product review"),
            ("can_edit_product_review", "Can edit product review"),
            ("can_delete_product_review", "Can delete product review"),
        ]