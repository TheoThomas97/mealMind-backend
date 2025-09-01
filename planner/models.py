from django.db import models
from django.conf import settings
from recipes.models import Recipe

class MealPlan(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="meal_plans")
    title = models.CharField(max_length=150)
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.start_date} – {self.end_date})"

class MealPlanItem(models.Model):
    BREAKFAST = "breakfast"
    LUNCH = "lunch"
    DINNER = "dinner"
    SNACK = "snack"
    MEAL_SLOT_CHOICES = [
        (BREAKFAST, "Breakfast"),
        (LUNCH, "Lunch"),
        (DINNER, "Dinner"),
        (SNACK, "Snack"),
    ]

    meal_plan = models.ForeignKey(MealPlan, on_delete=models.CASCADE, related_name="items")
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="meal_items")
    meal_date = models.DateField()
    meal_slot = models.CharField(max_length=20, choices=MEAL_SLOT_CHOICES)
    notes = models.CharField(max_length=255, blank=True)

    class Meta:
        indexes = [models.Index(fields=["meal_plan", "meal_date", "meal_slot"])]

    def __str__(self):
        return f"{self.meal_date} {self.meal_slot}: {self.recipe.title}"
