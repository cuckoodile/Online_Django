from django.contrib import admin
from .models import Transaction, TransactionStatus, TransactionMethod, TransactionType, ProductTransaction
from profiles.models import Profile  # Import the Profile model

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'type', 'status', 'payment_method', 'created_at', 'total_amount')
    list_filter = ('status', 'type', 'payment_method', 'created_at')
    search_fields = ('user__username', 'user__email', 'id')
    readonly_fields = ('created_at', 'updated_at', 'user', 'address')
    date_hierarchy = 'created_at'
    
    fieldsets = (
        (None, {
            'fields': ('user', 'address')
        }),
        ('Transaction Details', {
            'fields': ('status', 'payment_method', 'type')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if not obj.user_id:
            obj.user = request.user
        
        if not obj.address_id:
            try:
                profile = request.user.profile
                obj.address = profile.addresses.first() 
            except (AttributeError, Profile.DoesNotExist):
                pass
        
        super().save_model(request, obj, form, change)

    def total_amount(self, obj):
        return sum(pt.subtotal for pt in obj.product_transactions.all())
    total_amount.short_description = 'Total Amount'
    
    class ProductTransactionInline(admin.TabularInline):
        model = ProductTransaction
        extra = 1
        readonly_fields = ('subtotal',)
    
    inlines = [ProductTransactionInline]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "address":
            try:
                profile = request.user.profile
                kwargs["queryset"] = profile.addresses.all()
            except (AttributeError, Profile.DoesNotExist):
                pass
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

@admin.register(TransactionStatus)
class TransactionStatusAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

@admin.register(TransactionMethod)
class TransactionMethodAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

@admin.register(TransactionType)
class TransactionTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)