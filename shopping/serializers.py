from rest_framework import serializers
from .models import ShoppingList, ShoppingListItem
from recipes.models import Ingredient

class ShoppingListItemSerializer(serializers.ModelSerializer):

    ingredient = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all(), required=False)
    ingredient_data = serializers.DictField(write_only=True, required=False)
    shopping_list = serializers.PrimaryKeyRelatedField(queryset=ShoppingList.objects.all(), write_only=True)

    class Meta:
        model = ShoppingListItem
        fields = ['id', 'ingredient', 'ingredient_data', 'quantity', 'shopping_list']

    def create(self, validated_data):
        ingredient_data = validated_data.pop('ingredient_data', None)
        shopping_list = validated_data.pop('shopping_list')
        if ingredient_data:
            ingredient, _ = Ingredient.objects.get_or_create(**ingredient_data)
            validated_data['ingredient'] = ingredient
        validated_data['shopping_list'] = shopping_list
        return super().create(validated_data)

class ShoppingListSerializer(serializers.ModelSerializer):

    items = ShoppingListItemSerializer(many=True, required=False)
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = ShoppingList
        fields = ['id', 'title', 'items', 'user', 'created_at']

    def validate_title(self, value):
        if not value:
            raise serializers.ValidationError('Title is required.')
        return value

    def create(self, validated_data):
        items_data = validated_data.pop('items', [])
        shopping_list = ShoppingList.objects.create(**validated_data)
        for item_data in items_data:
            ingredient_data = item_data.pop('ingredient_data', None)
            if ingredient_data:
                ingredient, _ = Ingredient.objects.get_or_create(**ingredient_data)
                item_data['ingredient'] = ingredient
            ShoppingListItem.objects.create(shopping_list=shopping_list, **item_data)
        return shopping_list