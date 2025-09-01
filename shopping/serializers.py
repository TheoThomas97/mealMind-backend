from rest_framework import serializers
from .models import ShoppingList, ShoppingListItem

class ShoppingListItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShoppingListItem
        fields = ["id","shopping_list","ingredient","quantity","unit","is_checked","notes"]

class ShoppingListSerializer(serializers.ModelSerializer):
    items = ShoppingListItemSerializer(many=True, read_only=True)
    class Meta:
        model = ShoppingList
        fields = ["id","title","from_meal_plan","created_at","items"]
