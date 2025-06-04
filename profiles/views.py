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
        serializer.save()

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
