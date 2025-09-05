from rest_framework import serializers
from .models import Ingredient, Recipe, RecipeIngredient

class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ["id", "name"]

    def validate_name(self, value):
        if not value:
            raise serializers.ValidationError("Ingredient name is required.")
        return value

class RecipeIngredientSerializer(serializers.ModelSerializer):
    ingredient_data = serializers.DictField(write_only=True)
    quantity = serializers.CharField(write_only=True)
    unit = serializers.CharField(write_only=True)
    class Meta:
        model = RecipeIngredient
        fields = ['id', "recipe", 'ingredient_data', 'amount', 'quantity', 'unit']

    def validate(self, attrs):
        if not attrs.get('recipe'):
            raise serializers.ValidationError({'recipe': 'Recipe is required.'})
        return attrs
    def create(self, validated_data):
        ingredient_data = validated_data.pop('ingredient_data')
        quantity = validated_data.pop('quantity')
        unit = validated_data.pop('unit')
        # Use get_or_create to avoid duplicate ingredients with same name
        # Allow duplicate names: use first matching or create new if none
        ingredient = Ingredient.objects.filter(name=ingredient_data['name']).first()
        if not ingredient:
            ingredient = Ingredient.objects.create(name=ingredient_data['name'])
        validated_data['ingredient'] = ingredient
        validated_data['amount'] = f"{quantity} {unit}" if quantity and unit else str(quantity or unit)
        return super().create(validated_data)

class RecipeSerializer(serializers.ModelSerializer):
    ingredients = RecipeIngredientSerializer(many=True, read_only=True)
    class Meta:
        model = Recipe
        fields = ['id', 'title', 'ingredients']

    def validate_title(self, value):
        if not value:
            raise serializers.ValidationError('Title is required.')
        return value
