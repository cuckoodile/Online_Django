from django import forms
from django.contrib import admin
from .models import Cart
from products.models import Product

class CartAdminForm(forms.ModelForm):
    products = forms.ModelMultipleChoiceField(
        queryset= Product.objects.all(),
        required=False,
        widget=admin.widgets.FilteredSelectMultiple("Products", False)
    )
    quantities = forms.CharField(
        required=False,
        help_text="Enter quantities for each product separated by commas (e.g., 2,1,3)"
    )

    class Meta:
        model = Cart
        fields = '__all__'

    def save(self, commit=True):
        cart = super().save(commit=commit)
        products = self.cleaned_data.get('products', [])
        quantities = self.cleaned_data.get('quantities', '').split(',') if self.cleaned_data.get('quantities') else []
        
        for i, product in enumerate(products):
            quantity = int(quantities[i]) if i < len(quantities) else 1
            Cart.objects.create(
                user=cart.user,
                product=product,
                quantity=quantity
            )
        
        return cart