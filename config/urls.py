from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

# import your viewsets
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# Minimal test viewset
class PingViewSet(viewsets.ViewSet):
    def list(self, request):
        # 'request' is required by DRF ViewSet signature
        return Response({"ping": "pong"})

from recipes.views import RecipeViewSet, IngredientViewSet, RecipeIngredientViewSet
from planner.views import MealPlanViewSet, MealPlanItemViewSet
from shopping.views import ShoppingListViewSet, ShoppingListItemViewSet

router = DefaultRouter()
router.register(r"ping", PingViewSet, basename="ping")
router.register(r"recipes", RecipeViewSet, basename="recipe")
router.register(r"ingredients", IngredientViewSet, basename="ingredient")
router.register(r"recipe-ingredients", RecipeIngredientViewSet, basename="recipeingredient")
router.register(r"meal-plans", MealPlanViewSet, basename="mealplan")
router.register(r"meal-items", MealPlanItemViewSet, basename="mealitem")
router.register(r"shopping-lists", ShoppingListViewSet, basename="shoppinglist")
router.register(r"shopping-items", ShoppingListItemViewSet, basename="shoppingitem")

class TestApiView(APIView):
    def get(self, request):
        return Response({"message": "API routing works!"})


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/test/", TestApiView.as_view()),
    path("api/", include(router.urls)),
    path("api-auth/", include("rest_framework.urls")),
    path("api/auth/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]

