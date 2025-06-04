from django.shortcuts import render
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from .models import Transaction
from .serializers import TransactionSerializer
from profiles.permissions import IsAdminGroup
# Create your views here.

class TransactionListeView(ListAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated,IsAdminGroup]
    depth = 2

class TransactionCreateView(CreateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]
    depth = 2

    def perform_create(self, serializer):
        profile = self.request.user.profile
        serializer.save(profile=profile)


class TransactionDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]
    depth = 2

    def get_object(self):
        return self.request.user.transactions.get(pk=self.kwargs['pk'])
