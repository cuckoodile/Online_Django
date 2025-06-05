from django.shortcuts import render
from django.db.models import Count
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView,CreateAPIView
from categories.models import Category
from categories.serializers import CategorySerializer
from rest_framework.permissions import IsAuthenticated,AllowAny
from profiles.permissions import IsAdminGroup
# Create your views here.

class CategoryListCreateView(ListAPIView):
    queryset = Category.objects.annotate(product_count=Count('products'))
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]
    depth = 2

    def perform_create(self, serializer):
        serializer.save()

class CategoryCreateView(CreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated, IsAdminGroup]

    def perform_create(self, serializer):
        serializer.save()

class CategoryDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated ,IsAdminGroup]

    def get_object(self):
        return super().get_object()
