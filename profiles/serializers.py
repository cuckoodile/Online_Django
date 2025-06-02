from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Profile

class ProfileSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    first_name = serializers.CharField(source='user.first_name', required=False, allow_blank=True)
    last_name = serializers.CharField(source='user.last_name', required=False, allow_blank=True)
    email = serializers.EmailField(source='user.email')
    username = serializers.CharField(source='user.username')
    password = serializers.CharField(
        source='user.password',
        style={'input_type': 'password'}
    )
    role = serializers.CharField(source='profile.role', default="customer" , read_only=True) 

    class Meta:
        model = Profile
        fields = [
            'id',
            'user_id',
            'username',
            'email',
            'password',
            'first_name',
            'last_name',
            'full_name',
            'role',
            'contact_number',
            'profile_image',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'user_id', 'timestamp']

    def get_full_name(self, obj):
        if isinstance(obj, dict): 
            return f"{obj.get('first_name', '')} {obj.get('last_name', '')}"
        return f"{obj.first_name} {obj.last_name}"

    def create(self, validated_data):
        user_data = {
            "username": validated_data.pop("username"),
            "email": validated_data.pop("email"),
            "password": validated_data.pop("password"),
        }
        user = User.objects.create_user(**user_data)

        profile = Profile.objects.create( **validated_data)
        return profile


class ProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = [
            'first_name',
            'last_name',
            'contact_number',
            'profile_image'
        ]

    def create(self, validated_data):
        return Profile.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

    def delete(self, instance):
        instance.delete()
        return None
    
class AdminProfileSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    email = serializers.EmailField(source='user.email')
    username = serializers.CharField(source='user.username')
    password = serializers.CharField(
        source='user.password',
        style={'input_type': 'password'}
    )

    class Meta:
        model = Profile
        fields = [
            'id',
            'user_id',
            'username',
            'email',
            'password',
            'first_name',
            'last_name',
            'full_name',
            'role',
            'contact_number',
            'profile_image',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'user_id', 'timestamp']

    def get_full_name(self, obj):
        return obj.full_name

class AdminProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = [
            'role',
        ]

    def create(self, validated_data):
        return Profile.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

    def delete(self, instance):
        instance.delete()
        return None