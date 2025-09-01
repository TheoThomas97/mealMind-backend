from rest_framework import serializers
from .models import Recipe, Ingredient, RecipeIngredient

class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ["id", "name", "unit", "created_at"]

class RecipeIngredientWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipeIngredient
        fields = ["id", "ingredient", "quantity", "unit"]

class RecipeIngredientReadSerializer(serializers.ModelSerializer):
    ingredient = IngredientSerializer()
    class Meta:
        model = RecipeIngredient
        fields = ["id", "ingredient", "quantity", "unit"]

class RecipeSerializer(serializers.ModelSerializer):
    recipe_ingredients = RecipeIngredientReadSerializer(many=True, read_only=True)
    class Meta:
        model = Recipe
        fields = ["id","title","description","instructions","servings","image_url","created_at","recipe_ingredients"]
