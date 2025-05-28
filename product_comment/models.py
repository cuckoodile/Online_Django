from django.db import models
from django.contrib.auth.models import User
from products.models import Product

# Create your models here.
class ProductComment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    rating = models.PositiveSmallIntegerField()
    comment_id = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        permissions = [
            ("can_view_product_comment", "Can view product comment"),
            ("can_add_product_comment", "Can add product comment"),
            ("can_edit_product_comment", "Can edit product comment"),
            ("can_delete_product_comment", "Can delete product comment"),
        ]

    def __str__(self):
        return f"Comment by {self.user} on {self.product}: {self.comment[:20]}"