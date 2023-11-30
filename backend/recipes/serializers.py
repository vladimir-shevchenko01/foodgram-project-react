from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from recipes.models import FavoriteRecipe, Recipe, RecipeIngredient
from users.serializers import UserSerializer


class RecipeSerializer(serializers.ModelSerializer):
    image = Base64ImageField(max_length=None, use_url=True)
    ingredients = serializers.SerializerMethodField()
    is_favorited = serializers.SerializerMethodField()
    author = UserSerializer(read_only=True)

    def get_ingredients(self, obj):
        recipe_ingredients = RecipeIngredient.objects.filter(recipe=obj)
        return RecipeIngredientSerializer(
            recipe_ingredients,
            many=True
        ).data

    def get_is_favorited(self, obj):
        # Проверяем добавил ли пользователь рецепт в избранное.
        user = self.context['request'].user
        return FavoriteRecipe.objects.filter(user=user, recipe=obj).exists()

    class Meta:
        model = Recipe
        fields = '__all__'


class RecipeIngredientSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    measurement_unit = serializers.SerializerMethodField()

    def get_id(self, obj):
        return obj.ingredient.id

    def get_name(self, obj):
        return obj.ingredient.name

    def get_measurement_unit(self, obj):
        return obj.ingredient.measurement_unit

    class Meta:
        model = RecipeIngredient
        exclude = ('ingredient', 'recipe')


class FavoriteRecipeSerializer(serializers.ModelSerializer):

    class Meta:
        model = FavoriteRecipe
        fields = ('__all__')
        # fields = ('id', 'name', 'image', 'cooking_time')

class ShowFavoriteRecipeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        # fields = ('__all__')
        fields = ('id', 'name', 'image', 'cooking_time')