from django_filters.rest_framework import (BooleanFilter, FilterSet,
                                           ModelMultipleChoiceFilter)

from components.models import TagModel
from recipes.models import RecipeModel


class RecipeFilter(FilterSet):
    """Правила фильтрации."""
    is_favorited = BooleanFilter(
        field_name='favorite_recipes',
        method='filter_is_favorited',
        label='В избранном'
    )
    is_in_shopping_cart = BooleanFilter(
        field_name='is_in_shopping_cart',
        method='filter_is_in_shopping_cart',
        label='В корзине'
    )
    tags = ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=TagModel.objects.all()
    )

    class Meta:
        model = RecipeModel
        fields = ('is_favorited', 'is_in_shopping_cart', 'author', 'tags', )

    def filter_boolean_field(self, queryset, name, value, field_name):
        user = self.request.user
        if user.is_authenticated and value:
            filter_params = {f'{field_name}__user': user}
            return queryset.filter(**filter_params)
        return queryset

    def filter_is_favorited(self, queryset, name, value):
        return self.filter_boolean_field(
            queryset, name, value, 'favorites'
        )

    def filter_is_in_shopping_cart(self, queryset, name, value):
        return self.filter_boolean_field(
            queryset, name, value, 'recipe_in_cart'
        )
