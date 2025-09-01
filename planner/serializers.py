from rest_framework import serializers
from .models import MealPlan, MealPlanItem

class MealPlanItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MealPlanItem
        fields = ["id","meal_plan","recipe","meal_date","meal_slot","notes"]

class MealPlanSerializer(serializers.ModelSerializer):
    items = MealPlanItemSerializer(many=True, read_only=True)
    class Meta:
        model = MealPlan
        fields = ["id","title","start_date","end_date","created_at","items"]
