from rest_framework import viewsets, permissions, filters
from .models import Recipe, Ingredient, RecipeIngredient
from .serializers import RecipeSerializer, IngredientSerializer, RecipeIngredientWriteSerializer

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return getattr(obj, "user_id", None) == request.user.id

class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all().order_by("-created_at")
    serializer_class = RecipeSerializer
    permission_classes = [IsOwnerOrReadOnly]
    filterset_fields = ["servings"]
    search_fields = ["title","description"]
    ordering_fields = ["created_at","title"]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all().order_by("name")
    serializer_class = IngredientSerializer
    search_fields = ["name"]

class RecipeIngredientViewSet(viewsets.ModelViewSet):
    queryset = RecipeIngredient.objects.all()
    serializer_class = RecipeIngredientWriteSerializer
