from django.db import models
from django.contrib.auth.models import User
from product.models import Product
# Create your models here.
class ProductReview(models.Model):
    product = models.ForeignKey( Product,on_delete=models.CASCADE, related_name='product_reviews')
    user = models.ForeignKey( User, on_delete=models.CASCADE)
    review = models.CharField(max_length=255)
    rating = models.PositiveSmallIntegerField()
    review_id = models.ForeignKey(self, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        permissions = [
            ("can_view_product_review", "Can view product review"),
            ("can_add_product_review", "Can add product review"),
            ("can_edit_product_review", "Can edit product review"),
            ("can_delete_product_review", "Can delete product review"),
        ]

    def __str__(self):
        return f"Review by {self.user} on {self.product}"