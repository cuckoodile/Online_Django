from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import FormParser , MultiPartParser
from .models import Product
from .serializers import ProductGetSerializer , ProductSerializer
from product_image.serializers import ImageSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly

# Create your views here.
class ProductView(APIView):
    parser_classes = [FormParser , MultiPartParser]
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self , request):
        data = Product.objects.all().order_by('-id')
        serializer = ProductGetSerializer(data , many=True)
        return Response(serializer.data)

    def post(self , request):
        image_files = request.FILES.getlist('img') # 
        data = request.data.copy()
        print(image_files)
        serializer = ProductSerializer(data=data)
        if serializer.is_valid():
                product_instance = serializer.save()
                for img in image_files:
                    image_serializer = ImageSerializer(data={'img': img})
                    if image_serializer.is_valid():
                        img_instance = image_serializer.save()
                        product_instance.img.add(img_instance)
                return Response({'ok': True , 'data': serializer.data}, status=201)
        return Response({'ok': False , 'message': serializer.errors}, status=400)

      

    def patch(self , request):
        pass

    def delete(self , request):
        pass