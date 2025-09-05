from django.shortcuts import render
from rest_framework import viewsets, permissions, filters
from .models import ShoppingList, ShoppingListItem
from .serializers import ShoppingListSerializer, ShoppingListItemSerializer

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return getattr(obj, "user_id", None) == request.user.id

class UserQuerySetMixin:
    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)

class ShoppingListViewSet(UserQuerySetMixin, viewsets.ModelViewSet):
    model = ShoppingList
    queryset = ShoppingList.objects.all().order_by("-id")
    serializer_class = ShoppingListSerializer
    permission_classes = [IsOwnerOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['title']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ShoppingListItemViewSet(viewsets.ModelViewSet):
    queryset = ShoppingListItem.objects.all()
    serializer_class = ShoppingListItemSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['quantity']

    def perform_create(self, serializer):
        shopping_list = serializer.validated_data.get('shopping_list')
        if shopping_list.user != self.request.user:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("You do not have permission to add items to this list.")
        serializer.save()

    def get_queryset(self):
        # Only allow access to items belonging to lists owned by the user
        user = self.request.user
        return ShoppingListItem.objects.filter(shopping_list__user=user)

    def perform_destroy(self, instance):
        # Only allow deletion if the user owns the shopping list
        if instance.shopping_list.user == self.request.user:
            instance.delete()
        else:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("You do not have permission to delete this item.")