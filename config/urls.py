from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from rest_framework.routers import DefaultRouter

from recipes.views import RecipeViewSet, IngredientViewSet, RecipeIngredientViewSet
from planner.views import MealPlanViewSet, MealPlanItemViewSet
from shopping.views import ShoppingListViewSet, ShoppingListItemViewSet
from accounts.views import UserRegistrationView

router = DefaultRouter()
router.register(r"recipes", RecipeViewSet, basename="recipe")
router.register("ingredients", IngredientViewSet, basename="ingredient")
router.register(r"recipe-ingredients", RecipeIngredientViewSet, basename="recipeingredient")
router.register(r"meal-plans", MealPlanViewSet, basename="mealplan")
router.register(r"meal-items", MealPlanItemViewSet, basename="mealitem")
router.register(r"shopping-lists", ShoppingListViewSet, basename="shoppinglist")
router.register(r"shopping-items", ShoppingListItemViewSet, basename="shoppingitem")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
    path("api/auth/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/auth/token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("api-auth/", include("rest_framework.urls")),
    path("api/auth/register/", UserRegistrationView.as_view(), name="user_register"),
]

