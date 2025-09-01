from django.db import models
from django.conf import settings
from planner.models import MealPlan
from recipes.models import Ingredient

class ShoppingList(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="shopping_lists")
    title = models.CharField(max_length=150)
    from_meal_plan = models.ForeignKey(MealPlan, null=True, blank=True, on_delete=models.SET_NULL, related_name="shopping_lists")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class ShoppingListItem(models.Model):
    shopping_list = models.ForeignKey(ShoppingList, on_delete=models.CASCADE, related_name="items")
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE, related_name="shopping_items")
    quantity = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    unit = models.CharField(max_length=32, blank=True)
    is_checked = models.BooleanField(default=False)
    notes = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.ingredient.name} ({self.quantity or ''} {self.unit})"
