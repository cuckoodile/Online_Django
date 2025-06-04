from django.shortcuts import render
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from .models import Transaction
from profiles.models import Profile
from .serializers import TransactionSerializer,TransactionCreateSerializer
from profiles.permissions import IsAdminGroup
# Create your views here.

class TransactionListView(ListAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]
    depth = 2

class TransactionListViewByID(ListAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]
    depth = 2

    def get_queryset(self):
        return self.request.user.transactions.filter(pk=self.kwargs['pk'])

class TransactionCreateView(CreateAPIView):
    serializer_class = TransactionCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        address = None
        try:
            profile = self.request.user.profile
            address = profile.addresses.first()
        except (AttributeError, Profile.DoesNotExist):
            pass
        
        serializer.save(
            user=self.request.user,
            address=address
        )
class TransactionDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]
    depth = 2

    def get_object(self):
        return self.request.user.transactions.get(pk=self.kwargs['pk'])
