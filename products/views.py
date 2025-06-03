from django.shortcuts import render
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView,CreateAPIView

from rest_framework.parsers import FormParser , MultiPartParser
from .models import Product
from .serializers import ProductGetSerializer , ProductSerializer
from product_image.serializers import ImageSerializer
from rest_framework.permissions import IsAuthenticated
from profiles.permissions import IsAdminGroup

# Create your views here.
class ProductListView(ListAPIView):
    queryset = Product.objects.all().order_by('-id')
    parser_classes = [FormParser, MultiPartParser]
    permission_classes = [IsAdminGroup,IsAuthenticated]
    serializer_class = ProductGetSerializer
    
class ProductCreateView(CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    parser_classes = [FormParser, MultiPartParser]
    permission_classes = [IsAdminGroup,IsAuthenticated]

    def perform_create(self, serializer):
        product_instance = serializer.save()
        image_files = self.request.FILES.getlist('img')
        for img in image_files:
            image_serializer = ImageSerializer(data={'img': img})
            if image_serializer.is_valid():
                img_instance = image_serializer.save()
                product_instance.img.add(img_instance)

class ProductRetrieveUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    parser_classes = [FormParser, MultiPartParser]
    permission_classes = [IsAdminGroup,IsAuthenticated]

    def get_object(self):
        from .models import Profile
        return Profile.objects.get(pk=self.kwargs['pk'])
    

    def perform_update(self, serializer):
        product_instance = serializer.save()
        image_files = self.request.FILES.getlist('img')
        for img in image_files:
            image_serializer = ImageSerializer(data={'img': img})
            if image_serializer.is_valid():
                img_instance = image_serializer.save()
                product_instance.img.add(img_instance)
