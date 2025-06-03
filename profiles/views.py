from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, ListAPIView,CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Profile
from .serializers import ProfileSerializer, ProfileUpdateSerializer,AdminProfileSerializer,AdminProfileUpdateSerializer
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError
from .permissions import IsAdminGroup


class ProfileListView(ListAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Profile.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save()

class ProfileCreateView(CreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    def perform_create(self, serializer):
        user_id = self.request.data.get("user_id")
        username = self.request.data.get("username")
        if user_id:
            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                raise ValidationError({"user_id": "User does not exist"})
            if hasattr(user, 'profile'):
                raise ValidationError({"profile": "Profile already exists for this user"})
            serializer.save(user=user)
        elif username:
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                raise ValidationError({"username": "User does not exist"})
            if hasattr(user, 'profile'):
                raise ValidationError({"profile": "Profile already exists for this user"})
            serializer.save(user=user)
        else:
            user_data = {
                "username": self.request.data.get("username"),
                "email": self.request.data.get("email"),
                "password": self.request.data.get("password"),
            }
            if User.objects.filter(username=user_data["username"]).exists():
                raise ValidationError({"username": "Username already taken"})
            user = User.objects.create_user(**user_data)
            serializer.save(user=user)

class ProfileDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = ProfileUpdateSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user.profile
    
class AdminProfileListCreateView(ListCreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = AdminProfileSerializer
    permission_classes = [IsAuthenticated, IsAdminGroup]

    def perform_create(self, serializer):
        serializer.save()

class AdminProfileDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Profile.objects.all()
    serializer_class = AdminProfileUpdateSerializer
    permission_classes = [IsAuthenticated, IsAdminGroup]

    def get_object(self):
        from .models import Profile
        return Profile.objects.get(pk=self.kwargs['pk'])
