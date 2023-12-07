from drf_extra_fields.fields import Base64ImageField
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from users.serializers import UserSerializer
from components.serializers import AddIngredientsSerializer, TagSerializer
from components.models import IngredientModel
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
    tags = TagSerializer(many=True)

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
        fields = [
            'id', 'tags', 'author', 'ingredients',
            'is_favorited', 'is_in_shopping_cart',
            'name', 'image', 'text', 'cooking_time'
        ]


class RecipeIngredientSerializer(serializers.ModelSerializer):
    '''Сериализатор ингредиента в рецепте со всеми данными.'''

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
    '''Сериализатор рецепта при создании и изменении'''
    image = Base64ImageField()
    ingredients = AddIngredientsSerializer(many=True)

    def create_ingredients_for_recipe(self, recipe, ingredients):
        # Записываем ингредиенты в таблицу ингредиентов в рецепте.
        for ingredient_data in ingredients:
            id = ingredient_data['id']
            amount = ingredient_data['amount']

            RecipeIngredientModel.objects.create(
                recipe=recipe,
                ingredient_id=id,
                amount=amount
            )

    def validate(self, obj):
        # Проверка обязательных полей.
        required_fields = [
            'tags', 'ingredients', 'name', 'text', 'cooking_time', 'image'
        ]
        missing_fields = [
            field for field in required_fields if not obj.get(field)
        ]
        if missing_fields:
            raise serializers.ValidationError(
                f'Отсутствуют обязательные поля: {", ".join(missing_fields)}'
            )

        # Проверка на наличие повторяющихся ингредиентов.
        ingredients = [ing['id'] for ing in obj.get('ingredients')]
        if len(ingredients) != len(set(ingredients)):
            raise serializers.ValidationError(
                'Ингредиенты не могут повторяться.'
            )

        # Проверка на наличие ингредиента в БД.
        for ing in ingredients:
            if not IngredientModel.objects.filter(pk=ing).exists():
                raise serializers.ValidationError(
                    'Такого ингредиента нет в базе данных.'
                )

        # Проверка на наличие повторяющихся тегов.
        tags = [tag.id for tag in obj.get('tags')]
        if len(tags) != len(set(tags)):
            raise serializers.ValidationError(
                'Тэги не могут повторяться.'
            )

        for ing in obj.get('ingredients'):
            if ing['amount'] < 1:
                raise serializers.ValidationError(
                    'Количество ингредиента не может быть менее 1.'
                )

        return obj

    def create(self, validated_data):

        ingredients_data = validated_data.pop('ingredients')

        recipe = RecipeModel.objects.create(
            author=self.context['request'].user,
            name=validated_data['name'],
            text=validated_data['text'],
            cooking_time=validated_data['cooking_time'],
            image=validated_data['image']
        )
        tags = validated_data.get('tags')
        recipe.tags.set(tags)

        self.create_ingredients_for_recipe(recipe, ingredients_data)
        return recipe

    def update(self, instance, validated_data):
        ingredients_data = validated_data.pop('ingredients', None)
        # Обновляем основные поля рецепта.
        instance.name = validated_data.get('name', instance.name)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get(
            'cooking_time', instance.cooking_time
        )
        instance.tags.set(validated_data.get('tags', instance.tags.all()))
        instance.image = validated_data.get('image', instance.image)

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

        instance.save()
        return instance
    
    def to_representation(self, instance):
        return RecipeFullDataSerializer(
            instance,
            context={
                'request': self.context.get('request')
            }).data

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
