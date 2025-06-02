from django.contrib import admin
from .models import Transaction, TransactionStatus, TransactionMethod, TransactionType
# Register your models here.

class TransactionAdmin(admin.ModelAdmin):
    exclude = ('user', 'address')
    def save_model(self, request, obj, form, change):
        obj.user = request.user
        obj.address = request.user.address_set.first()  # Adjust if user-address relation is different
        super().save_model(request, obj, form, change)

admin.site.register(Transaction, TransactionAdmin)
admin.site.register(TransactionStatus)
admin.site.register(TransactionMethod)
admin.site.register(TransactionType)