from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from foodgram.pagination import CustomPagination
from foodgram.settings import FILE_NAME
from foodgram.permissions import IsAuthorOrReadOnly
from recipes.models import (
    FavoriteRecipeModel,
    RecipeIngredientModel,
    RecipeModel,
    ShoppingCartModel,
)
from recipes.serializers import (
    FavoriteRecipeSerializer,
    RecipeIngredientSerializer,
    RecipeFullDataSerializer,
    ShowFavoriteRecipeSerializer,
    ShoppingCartSerializer,
    ShowRecipeInCartSerializer,
    RecipeShortDataSerializer,
)
from rest_framework.permissions import IsAuthenticated


class RecipeViewSet(viewsets.ModelViewSet):
    '''Отображение рецептов.'''

    queryset = RecipeModel.objects.all()
    # serializer_class = RecipeFullDataSerializer
    permission_classes = [IsAuthorOrReadOnly]
    pagination_class = CustomPagination

    def get_serializer_class(self):
        if self.action in ['create', 'partial_update']:
            print(f'______________заходим чрез изменение с коротким сериализатором__________')
            return RecipeShortDataSerializer
        else:
            return RecipeFullDataSerializer

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(author=user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # def perform_update(self, serializer):
    #     print(f'______________сохраняем сериализатор__________')
    #     print(f'______________{serializer}__________!!@!!')
    #     serializer.save(author=self.request.user)
    #     return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_destroy(self, instance):
        instance.delete()

    @action(detail=True,
            methods=['post', 'delete'],
            url_path='favorite',
            permission_classes=[IsAuthenticated])
    def favorite(self, request, pk=None):
        user = request.user
        recipe = get_object_or_404(RecipeModel, id=pk)

        if request.method == 'POST':
            # Если пользователь не авторизован, возвращаем ошибку.
            if not request.user.is_authenticated:
                return Response(
                    {'details': 'Вы не авторизованы.'},
                    status=status.HTTP_401_UNAUTHORIZED,
                )
            # Проверяем находится ли данный рецепт в избранном.
            # Если рецепта нет, создаем новую запись.
            if FavoriteRecipeModel.objects.filter(
                user=user, recipe=recipe
            ).exists():
                return Response(
                    {'details': 'Этот рецепт уже есть в вашем избранном.'},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Сохраняем сериализатор с обновленными данными.
            serializer = FavoriteRecipeSerializer(
                data={'user': user.id, 'recipe': recipe.id}
            )
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
            # Ищем рецепт в избранном и удаляем его.
            favorite_recipes = get_object_or_404(
                FavoriteRecipeModel,
                user=user,
                recipe=recipe
            )
            favorite_recipes.delete()
            return Response(
                {'details': 'Рецепт удалён из избранного избраное'},
                status=status.HTTP_204_NO_CONTENT
            )

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=[IsAuthenticated]
    )
    def shopping_cart(self, request, pk=None):
        user = request.user
        recipe = get_object_or_404(RecipeModel, id=pk)

        if request.method == 'POST':
            # Если пользователь не авторизован, возвращаем ошибку.
            if not request.user.is_authenticated:
                return Response(
                    {'details': 'Учетные данные не были предоставлены.'},
                    status=status.HTTP_401_UNAUTHORIZED,
                )

            # Проверяем, находится ли рецепт уже в корзине пользователя
            elif ShoppingCartModel.objects.filter(
                user=user, recipe=recipe
            ).exists():
                return Response(
                    {'details': 'Этот рецепт уже есть в вашей корзине.'},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Добавляем рецепт в корзину пользователя
            serializer = ShoppingCartSerializer(
                data={'user': user.id, 'recipe': recipe.id}
            )

            if serializer.is_valid():
                serializer.save()
                cart_serializer = ShowRecipeInCartSerializer(recipe)
                return Response(
                    cart_serializer.data,
                    status=status.HTTP_201_CREATED
                )
            else:
                return Response(
                    serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST
                )

        if request.method == 'DELETE':
            # Если пользователь не авторизован, возвращаем ошибку.
            if not request.user.is_authenticated:
                return Response(
                    {'details': 'Вы не авторизованы.'},
                    status=status.HTTP_401_UNAUTHORIZED,
                )
            # Проверяем, находится ли рецепт в корзине пользователя
            if not ShoppingCartModel.objects.filter(
                user=user, recipe=recipe
            ).exists():
                return Response(
                    {'details': 'Такого рецепта нет в вашей корзине.'},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Удаляем рецепт из корзины пользователя
            shopping_cart_item = ShoppingCartModel.objects.get(
                user=user, recipe=recipe
            )
            shopping_cart_item.delete()

            return Response(
                {'details': 'Рецепт удалён из корзины покупок'},
                status=status.HTTP_204_NO_CONTENT
            )

    @action(
        detail=False,
        methods=['get'],
        permission_classes=[IsAuthenticated]
    )
    def download_shopping_cart(self, request):
        '''Реализация эндпоинта download_shopping_list.'''
        user = request.user
        shopping_list = ShoppingCartModel.objects.filter(user=user)

        header = 'Список покупок:\n_______________\n\n'
        shopping_list_content = [header]
        ingredients_summary = {}

        for cart_item in shopping_list:

            recipe = cart_item.recipe
            ingredients = RecipeIngredientModel.objects.filter(recipe=recipe)

            for ingredient in ingredients:
                ingredient_name = f'{ingredient.ingredient.name}, ' \
                                  f'{ingredient.ingredient.measurement_unit}' \
                                  f'.:  '
                ingredient_amount = ingredient.amount

                # Добавление или обновление данных в словаре.
                if ingredient_name in ingredients_summary:
                    ingredients_summary[ingredient_name] += ingredient_amount
                else:
                    ingredients_summary[ingredient_name] = ingredient_amount
                print(ingredients_summary)
        for key, value in ingredients_summary.items():
            shopping_list_content.append(f'{key}{value}\n')

        # Отправка файла в ответе.
        response = HttpResponse(content_type='text/plain')
        response['Content-Disposition'] = f'attachment; filename={FILE_NAME}'
        # Записываем собраные данные в ответ.
        response.writelines(shopping_list_content)
        return response


class RecipeIngredientViewSet(viewsets.ModelViewSet):
    queryset = RecipeIngredientModel.objects.all()
    serializer_class = RecipeIngredientSerializer
