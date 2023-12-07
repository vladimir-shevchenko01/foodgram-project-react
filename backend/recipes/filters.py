from django_filters.rest_framework import BooleanFilter, ModelMultipleChoiceFilter, FilterSet, ModelChoiceFilter
from recipes.models import RecipeModel
from components.models import TagModel
from users.models import CustomUser


class RecipeFilter(FilterSet):
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
    author = ModelChoiceFilter(
        queryset=CustomUser.objects.all())
    tags = ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=TagModel.objects.all()
    )

    class Meta:
        model = RecipeModel
        fields = ['is_favorited', 'is_in_shopping_cart', 'author', 'tags']

    def filter_is_favorited(self, queryset, name, value):
        user = self.request.user
        if value:
            return queryset.filter(favorites__user=user)
        return queryset

    def filter_is_in_shopping_cart(self, queryset, name, value):
        user = self.request.user
        if value:
            return queryset.filter(recipe_in_cart__user=user)
        return queryset