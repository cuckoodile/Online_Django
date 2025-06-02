"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework_simplejwt.views import TokenVerifyView
from .views import UserView

# API URL Endpoints
from products.views import ProductView
from address.views import AddressListCreateView, AddressDetailView
from cart.views import CartListCreateView, CartDetailView
from categories.views import CategoryListCreateView, CategoryDetailView
from profiles.views import ProfileListView,ProfileCreateView,ProfileDetailView,AdminProfileListCreateView, AdminProfileDetailView
from transactions.views import TransactionListCreateView, TransactionDetailView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/login', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('api/users/', UserView.as_view(), name='user-list'),

    # API Endpoints
    path('api/products/', ProductView.as_view()),
    path('api/addresses/', AddressListCreateView.as_view(), name='address-list-create'),
    path('api/addresses/<int:pk>/', AddressDetailView.as_view(), name='address-detail'),
    path('api/carts/', CartListCreateView.as_view(), name='cart-list-create'),
    path('api/carts/<int:pk>/', CartDetailView.as_view(), name='cart-detail'),
    path('api/categories/', CategoryListCreateView.as_view(), name='category-list-create'),
    path('api/categories/<int:pk>/', CategoryDetailView.as_view(), name='category-detail'),
    path('api/profiles/', ProfileListView.as_view(), name='profile-list'),
    path('api/profiles/create/', ProfileCreateView.as_view(), name='profile-list-create'),
    path('api/profiles/<int:pk>/', ProfileDetailView.as_view(), name='profile-detail'),
    path('api/admin/profiles/',AdminProfileListCreateView.as_view(), name='admin-profile-list-create'),
    path('api/admin/profiles/<int:pk>/', AdminProfileDetailView.as_view(), name='admin-profile-detail'),
    path('api/transactions/', TransactionListCreateView.as_view(), name='transaction-list-create'),
    path('api/transactions/<int:pk>/', TransactionDetailView.as_view(), name='transaction-detail'),
]
