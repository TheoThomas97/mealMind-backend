from django.db import models
from django.conf import settings
from recipes.models import Recipe
from django.contrib.auth import get_user_model

User = get_user_model()

def get_default_user():
     return User.objects.first().id


class MealPlan(models.Model):
    title = models.CharField(max_length=100)
    date = models.DateField()
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    def __str__(self):
        return self.title

class MealPlanItem(models.Model):
    meal_plan = models.ForeignKey(MealPlan, on_delete=models.CASCADE, related_name='items')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    date = models.DateField()
    def __str__(self):
        return f"{self.recipe.title} on {self.date}"
