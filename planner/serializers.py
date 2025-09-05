from rest_framework import serializers
from .models import MealPlan, MealPlanItem
from recipes.models import Recipe

class MealPlanItemSerializer(serializers.ModelSerializer):
    recipe = serializers.PrimaryKeyRelatedField(queryset=Recipe.objects.all())
    class Meta:
        model = MealPlanItem
        fields = ['id', 'recipe', 'date']

class MealPlanSerializer(serializers.ModelSerializer):
    items = MealPlanItemSerializer(many=True, read_only=True)
    class Meta:
        model = MealPlan
        fields = ['id', 'title', 'items']

    def validate_title(self, value):
        if not value:
            raise serializers.ValidationError('Title is required.')
        return value
