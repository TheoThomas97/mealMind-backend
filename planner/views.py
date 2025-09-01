from rest_framework import viewsets
from .models import MealPlan, MealPlanItem
from .serializers import MealPlanSerializer, MealPlanItemSerializer

class MealPlanViewSet(viewsets.ModelViewSet):
    queryset = MealPlan.objects.all().order_by("-created_at")
    serializer_class = MealPlanSerializer

class MealPlanItemViewSet(viewsets.ModelViewSet):
    queryset = MealPlanItem.objects.all()
    serializer_class = MealPlanItemSerializer
