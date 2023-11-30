from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import (AllowAny, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response

from recipes.models import FavoriteRecipe, Recipe, RecipeIngredient
from recipes.serializers import (FavoriteRecipeSerializer,
                                 RecipeIngredientSerializer, RecipeSerializer, ShowFavoriteRecipeSerializer)
from users.models import CustomUser
from users.serializers import UserSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(author=user)

    def perform_update(self, serializer):
        serializer.save(author=self.request.user)

    def perform_destroy(self, instance):
        instance.delete()

    @action(detail=True,
            methods=['post', 'delete'],
            url_path='favorite',
            permission_classes=[IsAuthenticated])
    def favorite(self, request, pk=None):
        user = request.user
        recipe = get_object_or_404(Recipe, id=pk)

        if request.method == 'POST':
            # Проверяем находится ли данный рецепт у нас в избранном.
            # Если рецепта нет, создаем новую запись.
            if FavoriteRecipe.objects.filter(user=user, recipe=recipe).exists():
                return Response(
                    {"message": "Этот рецепт уже есть в вашем избранном."},
                    status=status.HTTP_200_OK,
                )
            # Сохраняем сериализатор с обновленными данными.
            serializer = FavoriteRecipeSerializer(
                data={'user': user.id, 'recipe': recipe.id}
            )
            print(f'_______{serializer}_____________')
            if serializer.is_valid():
                serializer.save()
                favorite_recipe_serializer = ShowFavoriteRecipeSerializer(
                    recipe
                )
                return Response(
                    favorite_recipe_serializer.data,
                    status=status.HTTP_201_CREATED
                )
            else:
                return Response(
                    serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST
                )

        if request.method == 'DELETE':
            favorite_recipes = get_object_or_404(
                FavoriteRecipe,
                user=user,
                recipe=recipe
            )
            favorite_recipes.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)


class RecipeIngredientViewSet(viewsets.ModelViewSet):
    queryset = RecipeIngredient.objects.all()
    serializer_class = RecipeIngredientSerializer


class AddOrDeleteFavoriteRecipe(viewsets.ModelViewSet):
    queryset = FavoriteRecipe.objects.all()
    serializer_class = FavoriteRecipeSerializer
    
    
    @action(detail=True,
            methods=['post', 'delete'],
            url_path='subscribe',
            permission_classes=[IsAuthenticated])
    def favorite(self, request, pk=None):
        user = request.user
        author = get_object_or_404(CustomUser, id=pk)

        if request.method == 'POST':
            # Проверяем, существует ли уже подписка от пользователя на автора.
            # Если подписка не существует, создаем новую запись.
            if Subscribe.objects.filter(user=user, author=author).exists():
                return Response(
                    {"message": "Вы уже подписаны на этого автора"},
                    status=status.HTTP_200_OK,
                )
            # Сохраняем сериализатор с обновленными данными.
            serializer = SubscribeSerializer(
                data={'user': user.id, 'author': author.id}
            )
            if serializer.is_valid():
                serializer.save()
                author_serializer = UserSerializer(
                    author,
                    context={'request': request},
                )
                return Response(
                    author_serializer.data,
                    status=status.HTTP_201_CREATED
                )
            else:
                return Response(
                    serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST
                )

        if request.method == 'DELETE':
            subscription = get_object_or_404(
                Subscribe,
                user=user,
                author=author
            )
            subscription.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
