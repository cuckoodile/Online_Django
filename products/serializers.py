from rest_framework import serializers
from .models import Product
from product_image.serializers import ImageSerializer
from transactions.models import Transaction

class ProductSerializer(serializers.ModelSerializer):
    stock = serializers.IntegerField(write_only=True, required=False)
    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'description', 'stock']

    def create(self, validated_data):
        stock = validated_data.pop('stock', None)
        product = Product.objects.create(**validated_data)
        if stock is not None and stock > 0:
            Transaction.objects.create(
                product=product,
                type_id=1,
                payment_method_id=2,
                status_id=4,
                quantity=stock
            )
        return product

    def update(self, instance, validated_data):
        stock = validated_data.pop('stock', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if stock is not None and stock > 0:
            transaction, created = Transaction.objects.get_or_create(
                product=instance,
                type_id=1,
                payment_method_id=2,
                status_id=4,
                defaults={'quantity': stock}
            )
            if not created:
                transaction.quantity = stock
                transaction.save()
        return instance

    def delete(self, instance):
        instance.delete()
        return None
  

class ProductGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"
        depth = 1