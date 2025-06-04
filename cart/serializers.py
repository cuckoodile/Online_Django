from rest_framework import serializers
from cart.models import Cart
from products.models import Product
class CartSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        label="Select Product",
    )
    
    class Meta:
        model = Cart
        fields = ['id', 'user', 'product', 'quantity']
        depth = 1
        extra_kwargs = {
            'user': {'read_only': True}
        }

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

    def delete(self, instance):
        instance.delete()
        return None