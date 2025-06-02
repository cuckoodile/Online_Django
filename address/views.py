from django.shortcuts import render
from address.models import Address
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from address.serializers import AddressSerializer

class AddressListCreateView(ListCreateAPIView):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer

class AddressDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer

    def get_object(self):
        return super().get_object()