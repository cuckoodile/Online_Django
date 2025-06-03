from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Profile
from core.serializers import UserSerializer

class ProfileSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    email = serializers.EmailField(source='user.email', required=False, allow_blank=True)
    username = serializers.CharField(source='user.username', required=False, allow_blank=True)
    password = serializers.CharField(
        source='user.password',
        style={'input_type': 'password'},
        required=False,
        allow_blank=True
    )
    role = serializers.CharField(source='profile.role', read_only=True) 

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

    def validate(self, data):
        request = self.context.get('request')
        if request and request.method == 'POST':
            user_id = request.data.get('user_id')
            username = request.data.get('username')
            email = request.data.get('email')
            password = request.data.get('password')
            if not user_id and not username and not (email and password):
                raise serializers.ValidationError(
                    'You must provide either user_id, username, or username/email/password to create a profile.'
                )
        return data

    def get_full_name(self, obj):
        if isinstance(obj, dict): 
            return f"{obj.get('first_name', '')} {obj.get('last_name', '')}"
        return f"{obj.first_name} {obj.last_name}"

    def create(self, validated_data):
        user_data = validated_data.pop('user', None)
        from core.serializers import UserSerializer
        # Always set role to 'customer' for normal profile creation
        validated_data['role'] = 'customer'
        user = None
        if isinstance(user_data, dict):
            # Add password_confirmation for UserSerializer
            user_data['password_confirmation'] = user_data['password']
            user_serializer = UserSerializer(data=user_data)
            user_serializer.is_valid(raise_exception=True)
            user = user_serializer.save()
        elif isinstance(user_data, User):
            user = user_data
        profile = Profile.objects.create(user=user, **validated_data)
        from django.contrib.auth.models import Group
        group, _ = Group.objects.get_or_create(name='Customer')
        user.groups.clear()
        user.groups.add(group)
        return profile

    def update(self, instance, validated_data):
        validated_data.pop('role', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


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

    def create(self, validated_data):
        user_data = validated_data.pop('user', None)
        role = validated_data.get('role', 'customer')
        from core.serializers import UserSerializer
        user = None
        if isinstance(user_data, dict):
            user_data['password_confirmation'] = user_data['password']
            user_serializer = UserSerializer(data=user_data)
            user_serializer.is_valid(raise_exception=True)
            user = user_serializer.save()
        elif isinstance(user_data, User):
            user = user_data
        from .models import Profile
        if user and Profile.objects.filter(user=user).exists():
            raise serializers.ValidationError({'user': 'A profile for this user already exists.'})
        profile = Profile.objects.create(user=user, **validated_data) if user else Profile.objects.create(**validated_data)
        if user:
            from django.contrib.auth.models import Group
            group, _ = Group.objects.get_or_create(name=role.capitalize() if role != 'admin' else 'Admin')
            user.groups.clear()
            user.groups.add(group)
        return profile

    def update(self, instance, validated_data):
        role = validated_data.get('role', getattr(instance, 'role', None))
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        user = getattr(instance, 'user', None)
        if user:
            from django.contrib.auth.models import Group
            group, _ = Group.objects.get_or_create(name=role.capitalize() if role != 'admin' else 'Admin')
            user.groups.clear()
            user.groups.add(group)
        return instance

    def delete(self, instance):
        instance.delete()
        return None

class AdminProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = [
            'role',
        ]

    def create(self, validated_data):
        user = validated_data.pop('user', None)
        role = validated_data.get('role', 'customer')
        from .models import Profile
        if user and Profile.objects.filter(user=user).exists():
            raise serializers.ValidationError({'user': 'A profile for this user already exists.'})
        profile = Profile.objects.create(user=user, **validated_data) if user else Profile.objects.create(**validated_data)
        if user:
            from django.contrib.auth.models import Group
            group, _ = Group.objects.get_or_create(name=role.capitalize() if role != 'admin' else 'Admin')
            user.groups.clear()
            user.groups.add(group)
        return profile

    def update(self, instance, validated_data):
        role = validated_data.get('role', getattr(instance, 'role', None))
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        # Sync user group with role
        user = getattr(instance, 'user', None)
        if user:
            from django.contrib.auth.models import Group
            group, _ = Group.objects.get_or_create(name=role.capitalize() if role != 'admin' else 'Admin')
            user.groups.clear()
            user.groups.add(group)
        return instance

    def delete(self, instance):
        instance.delete()
        return None