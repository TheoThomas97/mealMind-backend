from django.shortcuts import render
from rest_framework import viewsets, permissions, filters
from .models import MealPlan, MealPlanItem
from .serializers import MealPlanSerializer, MealPlanItemSerializer

# Create your views here.

class OwnerQuerySetMixin:
    def get_queryset(self):
        return self.model.objects.filter(owner=self.request.user)

class MealPlanViewSet(OwnerQuerySetMixin, viewsets.ModelViewSet):
    model = MealPlan
    queryset = MealPlan.objects.all()
    serializer_class = MealPlanSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['title']

class MealPlanItemViewSet(viewsets.ModelViewSet):
    queryset = MealPlanItem.objects.all()
    serializer_class = MealPlanItemSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['date']
