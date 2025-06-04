from django.contrib import admin
from .forms import ProductAdminForm,SpecificationInlineForm
from .models import Product, SpecificationName, Specification, ProductComment, SpecificationSize, SpecificationColor
from transactions.models import Transaction, TransactionType, TransactionStatus, TransactionMethod, ProductTransaction
from product_images.models import ImageUpload

class ProductSpecificationInline(admin.TabularInline):
    model = Specification
    form = SpecificationInlineForm
    extra = 1
    autocomplete_fields = ['key','size','color']


class ImageUploadInline(admin.TabularInline):
    model = ImageUpload
    extra = 1

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    form = ProductAdminForm
    exclude = ('publisher', 'img')
    list_display = ('name', 'category', 'price', 'stock')
    inlines = [ProductSpecificationInline, ImageUploadInline]

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.publisher = request.user
        super().save_model(request, obj, form, change)
        stock = form.cleaned_data.get('stock')
        if stock is not None and stock > 0:
            transaction = Transaction.objects.create(
                user=request.user,
                type=TransactionType.objects.get(pk=1),
                payment_method=TransactionMethod.objects.get(pk=2),
                status=TransactionStatus.objects.get(pk=4)
            )
            ProductTransaction.objects.create(
                transaction=transaction,
                product=obj,
                quantity=stock
            )

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if 'img' in form.base_fields:
            form.base_fields.pop('img')
        return form

class SpecificationNameAdmin(admin.ModelAdmin):
    search_fields = ['key']

class SpecificationSizeAdmin(admin.ModelAdmin):
    search_fields = ['size']

class SpecificationColorAdmin(admin.ModelAdmin):
    search_fields = ['color']

admin.site.register(SpecificationSize, SpecificationSizeAdmin)
admin.site.register(SpecificationName, SpecificationNameAdmin)
admin.site.register(SpecificationColor,SpecificationColorAdmin)
admin.site.register(ProductComment)