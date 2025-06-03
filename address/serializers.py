from rest_framework import serializers
from address.models import Address

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'
        read_only_fields = ['profile_id']

    def create(self, validated_data):
        request = self.context.get('request')
        if request and hasattr(request.user, 'profile'):
            validated_data['profile_id'] = request.user.profile
        return Address.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

    def delete(self, instance):
        instance.delete()
        return None