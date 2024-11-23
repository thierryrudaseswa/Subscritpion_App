from django.shortcuts import render
from rest_framework import viewsets, permissions
from .models import Customer, InteractionLog
from .serializers import CustomerSerializer, InteractionLogSerializer

# Create your views here.


class CustomerViewSet(viewsets.ModelViewSet):
    serializer_class = CustomerSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Customer.objects.all()
        return Customer.objects.filter(user=self.request.user)


class InteractionLogViewSet(viewsets.ModelViewSet):
    serializer_class = InteractionLogSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return InteractionLog.objects.all()
        return InteractionLog.objects.filter(customer__user=self.request.user)
