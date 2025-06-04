from django import forms
from .models import Product
from product_images.models import ImageUpload

class ProductAdminForm(forms.ModelForm):
    stock = forms.IntegerField(required=False, min_value=0, help_text="Initial stock (inbound transaction)")
    img = forms.ModelMultipleChoiceField(
        queryset=ImageUpload.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Product
        fields = '__all__'
