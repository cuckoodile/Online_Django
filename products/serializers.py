from rest_framework import serializers
from .models import Product, ProductComment, Specification
from product_images.serializers import ImageSerializer
from transactions.models import Transaction, ProductTransaction
# from product_review.models import ProductReview

class ProductSerializer(serializers.ModelSerializer):
    stock = serializers.IntegerField(write_only=True, required=False)
    images = ImageSerializer(many=True, read_only=True)
    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'description', 'stock', 'category', 'images']
        depth = 2

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
  


class SpecificationSerializer(serializers.ModelSerializer):
    specification_name = serializers.SerializerMethodField()
    value = serializers.SerializerMethodField()
    size = serializers.SerializerMethodField()
    color = serializers.SerializerMethodField()

    class Meta:
        model = Specification
        fields = ['specification_name', 'value', 'size', 'color']

    def get_specification_name(self, obj):
        return {"Key": obj.key.key} if obj.key else {}

    def get_value(self, obj):
        return {"value": obj.value} if obj.value else {}

    def get_size(self, obj):
        return {"size": obj.size.size} if obj.size else {}

    def get_color(self, obj):
        return {"color": obj.color.color} if obj.color else {}


class ProductCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductComment
        fields = '__all__'
        depth = 2

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

class ProductGetSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True, read_only=True)
    comments = ProductCommentSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'description', 'stock', 'category', 'images', 'comments', 'specification']
        depth = 2

    def to_representation(self, instance):
        data = super().to_representation(instance)
        specifications = instance.specification.all()
        # Create a key-value dict for specifications
        data['specification'] = {
            s.key.key if s.key else "": s.value if s.value else ""
            for s in specifications if s.key
        }
        data['colors'] = [SpecificationSerializer(s).data['color'] for s in specifications if SpecificationSerializer(s).data['color']]
        data['sizes'] = [SpecificationSerializer(s).data['size'] for s in specifications if SpecificationSerializer(s).data['size']]
        return data