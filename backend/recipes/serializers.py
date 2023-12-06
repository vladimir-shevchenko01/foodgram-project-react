from drf_extra_fields.fields import Base64ImageField
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from users.serializers import UserSerializer
from components.serializers import IngredientSerializer, AddIngredientsSerializer
from components.models import TagModel, IngredientModel
from recipes.models import (
    FavoriteRecipeModel,
    RecipeIngredientModel,
    RecipeModel, ShoppingCartModel
)
from users.serializers import UserSerializer


class RecipeFullDataSerializer(serializers.ModelSerializer):
    '''Сериализатор рецепта со всеми данными .'''

    image = Base64ImageField(read_only=True)
    ingredients = serializers.SerializerMethodField()
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    author = UserSerializer(read_only=True)

    def get_ingredients(self, obj):
        recipe_ingredients = RecipeIngredientModel.objects.filter(recipe=obj)
        return RecipeIngredientSerializer(
            recipe_ingredients,
            many=True
        ).data

    def get_is_favorited(self, obj):
        # Проверка на наличие рецепта в избранном.
        user = self.context['request'].user

        if user.is_authenticated:
            return FavoriteRecipeModel.objects.filter(
                user=user, recipe=obj).exists()
        return False

    def get_is_in_shopping_cart(self, obj):
        user = self.context['request'].user
        return (
            self.context.get('request').user.is_authenticated
            and ShoppingCartModel.objects.filter(
                user=user,
                recipe=obj).exists()
        )

    class Meta:
        model = RecipeModel
        fields = '__all__'


class RecipeIngredientSerializer(serializers.ModelSerializer):
    '''Сериализатор ингредиента в рецепте.'''

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
        model = RecipeIngredientModel
        exclude = ('ingredient', 'recipe')


class RecipeShortDataSerializer(serializers.ModelSerializer):
    '''Сериализатор рецепта.'''
    image = Base64ImageField()
    ingredients = AddIngredientsSerializer(many=True)

    def update(self, instance, validated_data):
        ingredients_data = validated_data.pop('ingredients', None)
        print(f'_____{ingredients_data}______________________')
        # Обновляем основные поля рецепта.
        instance.name = validated_data.get('name', instance.name)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get('cooking_time', instance.cooking_time)
        instance.tags.set(validated_data.get('tags', instance.tags.all()))
        # instance.ingredients.set(validated_data.get('ingredients', instance.ingredients.all()))

        # Заменяем ингредиенты, если они есть, на новые.
        if ingredients_data is not None:
            # Удаляем все существующие ингредиенты
            instance.ingredients.clear()
            for ingredient_data in ingredients_data:
                id = ingredient_data.get('id')
                ingredient = get_object_or_404(IngredientModel, pk=id)
                RecipeIngredientModel.objects.create(
                    recipe=instance,
                    ingredient=ingredient,
                    amount=ingredient_data.get('amount')
                )

        # Обновляем изображение.
        instance.image = validated_data.get('image', instance.image)

        instance.save()
        return instance

    class Meta:
        model = RecipeModel
        fields = (
            'ingredients', 'tags', 'image',
            'name', 'text', 'cooking_time',
        )


class FavoriteRecipeSerializer(serializers.ModelSerializer):
    '''Сериализатор для добавления рецепта в избранное.'''

    class Meta:
        model = FavoriteRecipeModel
        fields = ('__all__')


class ShowFavoriteRecipeSerializer(serializers.ModelSerializer):
    '''Сериализатор для отображения рецепта при добавлении в избранное.'''

    class Meta:
        model = RecipeModel
        fields = ('id', 'name', 'image', 'cooking_time')


class ShoppingCartSerializer(serializers.ModelSerializer):
    '''Сериализатор корзины покупок.'''

    class Meta:
        model = ShoppingCartModel
        fields = ('__all__')


class ShowRecipeInCartSerializer(serializers.ModelSerializer):
    '''Сериализатор содержания корзины.'''

    class Meta:
        model = RecipeModel
        fields = ('id', 'name', 'image', 'cooking_time')
