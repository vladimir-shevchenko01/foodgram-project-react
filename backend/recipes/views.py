from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import (AllowAny, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response

from recipes.models import Recipe, RecipeIngredient, FavoriteRecipe
from recipes.serializers import RecipeIngredientSerializer, RecipeSerializer, FavoriteRecipeSerializer
from users.models import CustomUser
from users.serializers import UserSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

    def perform_create(self, serializer):
        print(f'______{self.request.user}____________')
        user = self.request.user
        serializer.save(author=user)

    def perform_update(self, serializer):
        print(f'______{self.request.user}____________')
        serializer.save(author=self.request.user)

    def perform_destroy(self, instance):
        instance.delete()


class RecipeIngredientViewSet(viewsets.ModelViewSet):
    queryset = RecipeIngredient.objects.all()
    serializer_class = RecipeIngredientSerializer


class AddToFavoriteRecipe(viewsets.ModelViewSet):
    queryset = FavoriteRecipe.objects.all()
    serializer_class = FavoriteRecipeSerializer
