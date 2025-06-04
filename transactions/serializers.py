from rest_framework import serializers
from .models import Transaction

class TransactionSerializer(serializers.ModelSerializer):
    status_name = serializers.CharField(source='status.name', read_only=True)
    payment_method_name = serializers.CharField(source='payment_method.name', read_only=True)
    user_email = serializers.EmailField(source='user.email', read_only=True)
    user_username = serializers.CharField(source='user.username', read_only=True)
    type_name = serializers.CharField(source='type.name', read_only=True)

    class Meta:
        model = Transaction
        fields = [
            'id',
            'status',
            'status_name',
            'user',
            'user_email',
            'user_username',
            'payment_method',
            'payment_method_name',
            'type',
            'type_name',
        ]
        read_only_fields = ['id']
        depth =1
    
    def create(self, validated_data):
        return Transaction.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

    def delete(self, instance):
        instance.delete()
        return None

class TransactionCreateSerializer(serializers.ModelSerializer):
    products = serializers.ListField(child=serializers.IntegerField(), write_only=True)
    quantity = serializers.ListField(child=serializers.IntegerField(), write_only=True)
    subtotal = serializers.ListField(child=serializers.DecimalField(max_digits=8, decimal_places=2), write_only=True)

    class Meta:
        model = Transaction
        fields = [
            'status',
            'user',
            'payment_method',
            'transaction_type',
            'address',
            'amount',
            'reference',
            'is_void',
            'products',
            'quantity',
            'subtotal',
        ]

    def validate(self, data):
        products = data.get('products', [])
        quantities = data.get('quantity', [])
        subtotals = data.get('subtotal', [])
        if not (len(products) == len(quantities) == len(subtotals)):
            raise serializers.ValidationError('Products, quantity, and subtotal lists must have the same length.')
        return data

    def create(self, validated_data):
        products = validated_data.pop('products', [])
        quantities = validated_data.pop('quantity', [])
        subtotals = validated_data.pop('subtotal', [])
        transaction = Transaction.objects.create(**validated_data)
        # Assuming ProductTransaction is the related model
        from .models import ProductTransaction
        for product_id, qty, sub in zip(products, quantities, subtotals):
            ProductTransaction.objects.create(
                transaction=transaction,
                product_id=product_id,
                quantity=qty,
                subtotal=sub
            )
        return transaction

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

    def delete(self, instance):
        instance.delete()
        return None

class TransactionUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = [
            'status',
            'payment_method',
            'is_void',
            'reference'
        ]

    def create(self, validated_data):
        return Transaction.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

    def delete(self, instance):
        instance.delete()
        return None