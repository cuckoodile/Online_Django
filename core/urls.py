from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.conf.urls.static import static
from django.conf import settings
from rest_framework_simplejwt.views import TokenVerifyView
from .views import UserView

# API URL Endpoints
from products.views import (
    ProductListView, ProductCreateView, ProductRetrieveUpdateDeleteView,
    ProductCommentListView, ProductCommentCreateView, ProductCommentRetrieveUpdateDeleteView,
    SpecificationListView, SpecificationCreateView, SpecificationRetrieveUpdateDeleteView,
)
from address.views import AddressListView, AddressDetailView, AddressCreateView
from cart.views import CartListView, CartDetailView, CartCreateView
from categories.views import CategoryListCreateView, CategoryDetailView
from profiles.views import ProfileListView,ProfileCreateView,ProfileDetailView,AdminProfileListCreateView, AdminProfileDetailView
from transactions.views import TransactionListeView, TransactionDetailView, TransactionCreateView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('api/users/', UserView.as_view(), name='user-list'),

    # API Endpoints for Products
    path('api/products/', ProductListView.as_view()),
    path('api/products/create/', ProductCreateView.as_view(), name='product-create'),
    path('api/products/<int:pk>/', ProductRetrieveUpdateDeleteView.as_view(), name='product-detail'),
    # ProductComment endpoints
    path('product-comments/', ProductCommentListView.as_view(), name='productcomment-list'),
    path('product-comments/create/', ProductCommentCreateView.as_view(), name='productcomment-create'),
    path('product-comments/<int:pk>/', ProductCommentRetrieveUpdateDeleteView.as_view(), name='productcomment-detail'),

    # Specification endpoints
    path('specifications/', SpecificationListView.as_view(), name='specification-list'),
    path('specifications/create/', SpecificationCreateView.as_view(), name='specification-create'),
    path('specifications/<int:pk>/', SpecificationRetrieveUpdateDeleteView.as_view(), name='specification-detail'),

    # ProductReview endpoints
    # path('product-reviews/', ProductReviewListView.as_view(), name='productreview-list'),
    # path('product-reviews/create/', ProductReviewCreateView.as_view(), name='productreview-create'),
    # path('product-reviews/<int:pk>/', ProductReviewRetrieveUpdateDeleteView.as_view(), name='productreview-detail'),
    # API Endpoints for Addresses
    path('api/addresses/', AddressListView.as_view(), name='address-list-create'),
    path('api/addresses/create/', AddressCreateView.as_view(), name='address-create'),
    path('api/addresses/<int:pk>/', AddressDetailView.as_view(), name='address-detail'),
    # API Endpoints for Carts
    path('api/carts/', CartListView.as_view(), name='cart-list-create'),
    path('api/carts/create/', CartCreateView.as_view(), name='cart-create'),
    path('api/carts/<int:pk>/', CartDetailView.as_view(), name='cart-detail'),
    # API Endpoints for Categories
    path('api/categories/', CategoryListCreateView.as_view(), name='category-list-create'),
    path('api/categories/<int:pk>/', CategoryDetailView.as_view(), name='category-detail'),
    # API Endpoints for Profiles
    path('api/profiles/', ProfileListView.as_view(), name='profile-list'),
    path('api/profiles/create/', ProfileCreateView.as_view(), name='profile-list-create'),
    path('api/profiles/<int:pk>/', ProfileDetailView.as_view(), name='profile-detail'),
    # API Endpoints for Admin Profiles
    path('api/admin/profiles/',AdminProfileListCreateView.as_view(), name='admin-profile-list-create'),
    path('api/admin/profiles/<int:pk>/', AdminProfileDetailView.as_view(), name='admin-profile-detail'),
    # API Endpoints for Transactions
    path('api/transactions/', TransactionListeView.as_view(), name='transaction-list-create'),
    path('api/transactions/create/', TransactionCreateView.as_view(), name='transaction-create'),
    path('api/transactions/<int:pk>/', TransactionDetailView.as_view(), name='transaction-detail'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)