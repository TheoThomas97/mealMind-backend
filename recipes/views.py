from rest_framework import viewsets, permissions, filters
from .models import Recipe, Ingredient, RecipeIngredient
from .serializers import RecipeSerializer, IngredientSerializer, RecipeIngredientSerializer

class OwnerQuerySetMixin:
    def get_queryset(self):
        # Filter by owner if model has it
        qs = self.model.objects.all()
        if hasattr(self.model, "owner") and self.request.user.is_authenticated:
            qs = qs.filter(owner=self.request.user)
        return qs

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return getattr(obj, "user_id", None) == request.user.id

class RecipeViewSet(OwnerQuerySetMixin, viewsets.ModelViewSet):
    model = Recipe
    queryset = Recipe.objects.all().order_by("-id")
    serializer_class = RecipeSerializer
    permission_classes = [permissions.IsAuthenticated | IsOwnerOrReadOnly]
    filterset_fields = []
    search_fields = ["title","description"]
    ordering_fields = ["id","title"]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.owner != request.user:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("You do not have permission to delete this recipe.")
        return super().destroy(request, *args, **kwargs)

class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all().order_by("name")
    serializer_class = IngredientSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name"]
    ordering_fields = ["name", "id"]

    def perform_create(self, serializer):
        # Only set owner if user is authenticated
        user = self.request.user if self.request.user.is_authenticated else None
        serializer.save(owner=user)

class RecipeIngredientViewSet(viewsets.ModelViewSet):
    def perform_destroy(self, instance):
        # Only allow deletion if the user owns the recipe
        if instance.recipe.owner == self.request.user:
            instance.delete()
        else:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("You do not have permission to delete this ingredient from the recipe.")
    queryset = RecipeIngredient.objects.all()
    serializer_class = RecipeIngredientSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['amount']
