from rest_framework import serializers
from .models import TransactionMethod

class TransactionMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionMethod
        fields = '__all__'

    def create(self, validated_data):
        return TransactionMethod.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

    def delete(self, instance):
        instance.delete()
        return None