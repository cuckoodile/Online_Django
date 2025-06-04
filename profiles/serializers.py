from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
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
    address = serializers.SerializerMethodField()

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
            'address',
            'role',
            'contact_number',
            'profile_image',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'user_id', 'timestamp']

    def get_full_name(self, obj):
        if isinstance(obj, dict):
            return f"{obj.get('first_name', '')} {obj.get('last_name', '')}".strip()
        return f"{obj.first_name} {obj.last_name}".strip()

    def get_address(self, obj):
        if isinstance(obj, dict):
            return None
        
        addresses = obj.addresses.all()
        if addresses.exists():
            address = addresses.first()
            from address.serializers import AddressSerializer
            return AddressSerializer(address).data
        return None


    def validate(self, data):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return data
        
        user_data = data.get('user', {})
        if not all([user_data.get('username'), 
                   user_data.get('email'), 
                   user_data.get('password')]):
            raise serializers.ValidationError(
                'For new accounts, you must provide username, email and password'
            )
        return data

    def create(self, validated_data):
        request = self.context.get('request')
        
        if request and request.user.is_authenticated:
            validated_data.pop('user', None)
            profile = Profile.objects.create(
                user=request.user,
                **validated_data
            )
            return profile
        else:
            user_data = validated_data.pop('user')
            
            if User.objects.filter(username=user_data['username']).exists():
                raise ValidationError({'username': 'This username is taken'})
            if User.objects.filter(email=user_data['email']).exists():
                raise ValidationError({'email': 'This email is already registered'})
            
            user = User.objects.create_user(
                username=user_data['username'],
                email=user_data['email'],
                password=user_data['password']
            )
            
            profile = Profile.objects.create(
                user=user,
                **validated_data
            )
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

    address = serializers.SerializerMethodField()
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
            'address',
            'role',
            'contact_number',
            'profile_image',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'user_id', 'timestamp']

    def get_full_name(self, obj):
        return obj.full_name

    def get_address(self, obj):
        address_obj = getattr(obj, 'address', None)
        if address_obj:
            return str(address_obj)
        return None

    def create(self, validated_data):
        user_data = validated_data.pop('user', None)
        role = validated_data.get('role', 'customer')
        from core.serializers import UserSerializer
        from django.contrib.auth.models import User
        user = None
        if isinstance(user_data, dict):
            username = user_data.get('username')
            email = user_data.get('email')
            user_qs = User.objects.filter(username=username)
            if not user_qs.exists() and email:
                user_qs = User.objects.filter(email=email)
            if user_qs.exists():
                user = user_qs.first()
                from .models import Profile
                if Profile.objects.filter(user=user).exists():
                    raise serializers.ValidationError({'user': 'A profile for this user already exists.'})
            else:
                user_data['password_confirmation'] = user_data['password']
                user_serializer = UserSerializer(data=user_data)
                user_serializer.is_valid(raise_exception=True)
                user = user_serializer.save()
                password = user_data['password']
                user.set_password(password)
                user.save()
        elif isinstance(user_data, User):
            user = user_data
            from .models import Profile
            if Profile.objects.filter(user=user).exists():
                raise serializers.ValidationError({'user': 'A profile for this user already exists.'})
        from .models import Profile
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