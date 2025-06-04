from django.contrib import admin
from .models import Cart
from django.utils.html import format_html
from django.core.exceptions import ValidationError

class CartAdmin(admin.ModelAdmin):
    list_display = ('user_info', 'product_info', 'quantity', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('user__username', 'product__name')
    list_select_related = ('user', 'product')
    raw_id_fields = ('user',)
    autocomplete_fields = ['product']
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        (None, {
            'fields': ('user', 'product', 'quantity')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def user_info(self, obj):
        if obj.user:
            return f"{obj.user.username} ({obj.user.email})"
        return "No user"
    user_info.short_description = 'User'
    user_info.admin_order_field = 'user__username'
    
    def product_info(self, obj):
        if obj.product:
            return format_html(
                '<a href="/admin/products/product/{}/change/">{}</a> (Stock: {})',
                obj.product.id,
                obj.product.name,
                obj.product.stock
            )
        return "No product"
    product_info.short_description = 'Product'
    product_info.admin_order_field = 'product__name'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'product')
    
    def save_model(self, request, obj, form, change):
        if not obj.product:
            raise ValidationError("A product must be selected")
        if obj.quantity < 1:
            raise ValidationError("Quantity must be at least 1")
        super().save_model(request, obj, form, change)

admin.site.register(Cart, CartAdmin)