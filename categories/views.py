from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from categories.models import Category
from categories.serializers import CategorySerializer
from rest_framework.permissions import IsAuthenticated
# Create your views here.

class CategoryListCreateView(ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    # permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save()

class CategoryDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    # permission_classes = [IsAuthenticated]

    def get_object(self):
        return super().get_object()
