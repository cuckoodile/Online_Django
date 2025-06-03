from rest_framework import serializers
from .models import Product, ProductComment, Specification
from product_image.serializers import ImageSerializer
from transactions.models import Transaction, ProductTransaction
from product_review.models import ProductReview

class ProductSerializer(serializers.ModelSerializer):
    stock = serializers.IntegerField(write_only=True, required=False)
    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'description', 'stock']

    def create(self, validated_data):
        stock = validated_data.pop('stock', None)
        product = Product.objects.create(**validated_data)
        if stock is not None and stock > 0:
            transaction = Transaction.objects.create(
                product=product,
                type_id=1,
                payment_method_id=2,
                status_id=4
            )
            ProductTransaction.objects.create(
                transaction=transaction,
                product=product,
                quantity=stock
            )
        return product

    def update(self, instance, validated_data):
        stock = validated_data.pop('stock', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if stock is not None and stock > 0:
            transaction, _ = Transaction.objects.get_or_create(
                product=instance,
                type_id=1,
                payment_method_id=1,
                status_id=3
            )
            product_transaction, created = ProductTransaction.objects.get_or_create(
                transaction=transaction,
                product=instance,
                defaults={'quantity': stock}
            )
            if not created:
                product_transaction.quantity = stock
                product_transaction.save()
        return instance

    def delete(self, instance):
        instance.delete()
        return None
  

class ProductGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"
        depth = 1

class SpecificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specification
        fields = '__all__'

class ProductReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductReview
        fields = '__all__'
        
    def create(self, validated_data):
        return ProductReview.objects.create(**validated_data)
    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
    def delete(self, instance):
        instance.delete()
        return None

class ProductCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductComment
        fields = '__all__'

    def create(self, validated_data):
        return ProductComment.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

    def delete(self, instance):
        instance.delete()
        return None