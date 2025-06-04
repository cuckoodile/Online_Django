from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal
from django.contrib.auth.models import User
from categories.models import Category
from product_images.models import ImageUpload

class Product(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    price = models.DecimalField(max_digits=8,decimal_places=2,validators=[MinValueValidator(Decimal('0.01'))])
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

class SpecificationName(models.Model):
    key = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.key}"
    
class SpecificationSize(models.Model):
    size = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.size}"
    
class SpecificationColor(models.Model):
    color = models.CharField(max_length=100)

    def __str__ (self):
        return f"{self.color}"
    
class Specification(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='specification')
    key = models.ForeignKey(SpecificationName, on_delete=models.CASCADE, related_name='specification',null=True,blank=True)
    value = models.CharField(max_length=100,null=True,blank=True)
    size = models.ForeignKey(SpecificationSize, on_delete=models.CASCADE, related_name='specification',null=True,blank=True)
    color = models.ForeignKey(SpecificationColor, on_delete=models.CASCADE, related_name='specification',null=True,blank=True)
    class Meta:
        unique_together = ('product', 'key', 'value', 'size')

    def __str__(self):
        key_str = self.key.key if self.key else "No Key"
        value_str = self.value if self.value else "No Value"
        size_str = self.size.size if self.size else "No Size"
        color_str = self.color.color if self.color else "No Color"
        return f"{key_str}: {value_str} | Size: {size_str} | Color: {color_str}"

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