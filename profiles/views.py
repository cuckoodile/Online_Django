from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, ListAPIView,CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Profile
from .serializers import ProfileSerializer, ProfileUpdateSerializer,AdminProfileSerializer,AdminProfileUpdateSerializer
from django.contrib.auth.models import User


# Create your views here.

class ProfileListView(ListAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save()

class ProfileCreateView(CreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    def perform_create(self, serializer):
        user_data = {
            "username": self.request.data.get("username"),
            "email": self.request.data.get("email"),
            "password": self.request.data.get("password"),
        }
        if User.objects.filter(username=user_data["username"]).exists():
            return Response({"error": "Username already taken"}, status=status.HTTP_400_BAD_REQUEST)

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
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save()

class AdminProfileDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Profile.objects.all()
    serializer_class = AdminProfileUpdateSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user.profile
