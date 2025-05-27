from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        permissions = [
            ("can_view_category", "Can view category"),
            ("can_add_category", "Can add category"),
            ("can_edit_category", "Can edit category"),
            ("can_delete_category", "Can delete category"),
        ]

    def __str__(self):
        return self.name