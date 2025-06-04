from django.shortcuts import render
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView,CreateAPIView
from rest_framework import viewsets

from rest_framework.parsers import FormParser , MultiPartParser
from .models import Product, ProductComment, Specification
# from product_review.models import ProductReview
from .serializers import ProductGetSerializer , ProductSerializer , ProductCommentSerializer, SpecificationSerializer
from product_images.serializers import ImageSerializer
from rest_framework.permissions import IsAuthenticated
from profiles.permissions import IsAdminGroup, IsCustomerGroup, IsShipperGroup, IsOrderTrackerGroup

# Create your views here.
class ProductListView(ListAPIView):
    queryset = Product.objects.all().order_by('-id')
    parser_classes = [FormParser, MultiPartParser]
    permission_classes = []
    serializer_class = ProductGetSerializer

class ProductListViewById(ListAPIView):
    serializer_class = ProductGetSerializer
    parser_classes = [FormParser, MultiPartParser]

    def get_queryset(self):
        product_id = self.kwargs['pk']
        return Product.objects.filter(id=product_id).order_by('-id')
    
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

    def perform_update(self, serializer):
        product_instance = serializer.save()
        image_files = self.request.FILES.getlist('img')
        for img in image_files:
            image_serializer = ImageSerializer(data={'img': img})
            if image_serializer.is_valid():
                img_instance = image_serializer.save()
                product_instance.img.add(img_instance)

class ProductCommentListView(ListAPIView):
    queryset = ProductComment.objects.all().order_by('-id')
    serializer_class = ProductCommentSerializer
    permission_classes = [IsCustomerGroup, IsAuthenticated]

class ProductCommentCreateView(CreateAPIView):
    queryset = ProductComment.objects.all()
    serializer_class = ProductCommentSerializer
    permission_classes = [IsAdminGroup, IsAuthenticated]

    def perform_create(self, serializer):
        product_comment_instance = serializer.save()
        comment_id = self.request.data.get('comment_id')
        if comment_id:
            product_comment_instance.comment_id = ProductComment.objects.get(pk=comment_id)
            product_comment_instance.save()

class ProductCommentRetrieveUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    queryset = ProductComment.objects.all()
    serializer_class = ProductCommentSerializer
    permission_classes = [IsAdminGroup, IsAuthenticated]

    def get_object(self):
        from .models import ProductComment
        return ProductComment.objects.get(pk=self.kwargs['pk'])
class SpecificationListView(ListAPIView):
    queryset = Specification.objects.all().order_by('-id')
    serializer_class = SpecificationSerializer
    permission_classes = [IsAuthenticated]

class SpecificationCreateView(CreateAPIView):
    queryset = Specification.objects.all()
    serializer_class = SpecificationSerializer
    permission_classes = [IsAdminGroup, IsAuthenticated]

    def perform_create(self, serializer):
        product = self.request.data.get('product')
        name = self.request.data.get('name')
        value = self.request.data.get('value')
        if product and name and value:
            specification_instance = serializer.save(product_id=product, name_id=name, value=value)
            return specification_instance
        else:
            raise ValueError("Product, Name, and Value are required fields.")

class SpecificationRetrieveUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    queryset = Specification.objects.all()
    serializer_class = SpecificationSerializer
    permission_classes = [IsAdminGroup, IsAuthenticated]

    def get_object(self):
        from .models import Specification
        return Specification.objects.get(pk=self.kwargs['pk'])


# class ProductReviewListView(ListAPIView):
#     queryset = ProductReview.objects.all().order_by('-id')
#     serializer_class = ProductReviewSerializer
#     permission_classes = [IsAuthenticated]

# class ProductReviewCreateView(CreateAPIView):
#     queryset = ProductReview.objects.all()
#     serializer_class = ProductReviewSerializer
#     permission_classes = [IsCustomerGroup, IsAuthenticated]

#     def perform_create(self, serializer):
#         product = self.request.data.get('product')
#         user = self.request.data.get('user')
#         rating = self.request.data.get('rating')
#         review = self.request.data.get('review')

#         if product and user and rating is not None and review:
#             product_review_instance = serializer.save(product_id=product, user_id=user, rating=rating, review=review)
#             return product_review_instance
#         else:
#             raise ValueError("Product, User, Rating, and Review are required fields.")

# class ProductReviewRetrieveUpdateDeleteView(RetrieveUpdateDestroyAPIView):
#     queryset = ProductReview.objects.all()
#     serializer_class = ProductReviewSerializer
#     permission_classes = [IsCustomerGroup, IsAuthenticated]

#     def get_object(self):
#         from .models import ProductReview
#         return ProductReview.objects.get(pk=self.kwargs['pk'])
