from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from recipes.models import Recipe, RecipeIngredient
from recipes.serializers import RecipeIngredientSerializer, RecipeSerializer
from users.models import CustomUser


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return RecipeSerializer
        elif self.action == 'create' or self.action == 'update' or self.action == 'partial_update':
            return RecipeSerializer
        return RecipeSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        serializer.save()

    def perform_destroy(self, instance):
        instance.delete()


class RecipeIngredientViewSet(viewsets.ModelViewSet):
    queryset = RecipeIngredient.objects.all()
    serializer_class = RecipeIngredientSerializer


