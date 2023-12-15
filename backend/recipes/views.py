from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from foodgram.pagination import CustomPagination
from foodgram.permissions import IsAuthorOrReadOnly
from foodgram.settings import FILE_NAME
from recipes.filters import RecipeFilter
from recipes.models import FavoriteRecipeModel, RecipeModel, ShoppingCartModel
from recipes.serializers import (FavoriteRecipeSerializer,
                                 RecipeFullDataSerializer,
                                 RecipeShortDataSerializer,
                                 ShoppingCartSerializer,
                                 ShowDataAddToFavoriteOrToCartSerializer)


class RecipeViewSet(viewsets.ModelViewSet):
    """Отображение рецептов."""

    queryset = RecipeModel.objects.all()
    permission_classes = [IsAuthorOrReadOnly]
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        if self.action in ['create', 'partial_update']:
            return RecipeShortDataSerializer
        else:
            return RecipeFullDataSerializer

    def _handle_favorite_shopping_cart(
        self, request, pk, model, serializer_class, show_serializer
    ):
        user = request.user

        # Обработка POST-запроса.
        if request.method == 'POST':
            # Проверяем существует ли такой рецепт в базе.
            if not RecipeModel.objects.filter(pk=pk).exists():
                return Response(
                    {'details': (
                        'Такого рецепта не существует.'
                    )},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            recipe = get_object_or_404(RecipeModel, pk=pk)
            # Проверяем, находится ли рецепт уже в
            # избранном или корзине пользователя.
            if model.objects.filter(user=user, recipe=recipe).exists():
                return Response(
                    {'details': (
                        f'Этот рецепт уже есть у вас в {model.__name__}.'
                    )},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Добавляем рецепт в избранное или корзину пользователя.
            serializer = serializer_class(
                data={'user': user.id, 'recipe': recipe.id}
            )
            if serializer.is_valid():
                serializer.save()
                show_response_serializer = show_serializer(recipe)
                return Response(
                    show_response_serializer.data,
                    status=status.HTTP_201_CREATED
                )
            else:
                return Response(
                    serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST
                )

        # Обработка DELETE-запроса.
        elif request.method == 'DELETE':
            recipe = get_object_or_404(RecipeModel, pk=pk)
            # Проверяем, находится ли рецепт в
            # избранном или корзине пользователя.
            if not model.objects.filter(user=user, recipe=recipe).exists():
                return Response(
                    {'details': f'Такого рецепта не было в {model.__name__}.'},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Удаляем рецепт из избранного или корзины пользователя.
            cart = get_object_or_404(model, user=user, recipe=recipe)
            cart.delete()
            return Response(
                {'details': f'Рецепт удалён из {model.__name__}'},
                status=status.HTTP_204_NO_CONTENT
            )

    @action(
        detail=True,
        methods=['post', 'delete'],
        url_path='favorite',
        permission_classes=[IsAuthenticated]
    )
    def favorite(self, request, pk=None):

        return self._handle_favorite_shopping_cart(
            request,
            pk,
            FavoriteRecipeModel,
            FavoriteRecipeSerializer,
            ShowDataAddToFavoriteOrToCartSerializer,
        )

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=[IsAuthenticated]
    )
    def shopping_cart(self, request, pk=None):
        # self._validate_recipe_and_user(request, pk)
        return self._handle_favorite_shopping_cart(
            request,
            pk,
            ShoppingCartModel,
            ShoppingCartSerializer,
            ShowDataAddToFavoriteOrToCartSerializer,
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

        # Получаем информацию о корзине пользователя с суммарными данными.
        shopping_list = (
            user.cart_of_user.all().values(
                'recipe__ingredients__name',
                'recipe__ingredients__measurement_unit',
            )
            .annotate(total_amount=Sum('recipe__recipe_ingredients__amount'))
        )

        header = 'Список покупок:\n_______________\n\n'
        shopping_list_content = [header]
        ingredients_summary = {}

        for ingredient in shopping_list:
            name = ingredient['recipe__ingredients__name']
            measurement_unit = ingredient[
                'recipe__ingredients__measurement_unit'
            ]
            ingredient_name = (
                f'{name}, {measurement_unit}.:  '
            )
            ingredient_amount = ingredient['total_amount']

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
