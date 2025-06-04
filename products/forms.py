from django import forms
from .models import Product
from product_images.models import ImageUpload
from .models import Specification

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

class SpecificationInlineForm(forms.ModelForm):
    class Meta:
        model = Specification
        fields = '__all__'
        widgets = {
            'size': forms.Select(attrs={'style': 'width: 150px;'}),
            'color': forms.Select(attrs={'style': 'width: 150px;'}),
        }