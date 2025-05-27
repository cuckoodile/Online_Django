from django.contrib import admin
from .models import Product
from .forms import ProductAdminForm
from transactions.models import Transaction
from product_image.models import ImageUpload
from transaction_type.models import TransactionType
from transaction_method.models import PaymentMethod
from transaction_status.models import TransactionStatus

class ImageUploadInline(admin.TabularInline):
    model = ImageUpload
    extra = 1

class ProductAdmin(admin.ModelAdmin):
    form = ProductAdminForm
    readonly_fields = ('publisher',)
    exclude = ()
    list_display = ('name', 'category', 'price', 'publisher', 'stock')
    inlines = [ImageUploadInline]

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.publisher = request.user
        super().save_model(request, obj, form, change)
        stock = form.cleaned_data.get('stock')
        if stock is not None and stock > 0:
            Transaction.objects.create(
                product=obj,
                user=request.user,
                transaction_type=TransactionType.objects.get(pk=1),
                payment_method=PaymentMethod.objects.get(pk=2),
                status=TransactionStatus.objects.get(pk=4),
                quantity=stock
            )

admin.site.register(Product, ProductAdmin)