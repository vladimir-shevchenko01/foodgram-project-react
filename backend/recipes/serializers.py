from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from components.models import IngredientModel
from components.serializers import AddIngredientsSerializer, TagSerializer
from recipes.models import (FavoriteRecipeModel, RecipeIngredientModel,
                            RecipeModel, ShoppingCartModel)
from users.serializers import UserSerializer


class RecipeIngredientSerializer(serializers.ModelSerializer):
    """Сериализатор ингредиента в рецепте со всеми данными."""

    id = serializers.PrimaryKeyRelatedField(
        source='ingredient',
        read_only=True,
    )
    name = serializers.CharField(
        source='ingredient.name',
        read_only=True,
    )
    measurement_unit = serializers.CharField(
        source='ingredient.measurement_unit',
        read_only=True,
    )

    class Meta:
        model = RecipeIngredientModel
        # fields = ('id', 'name', 'measurement_unit')
        exclude = ('ingredient', 'recipe')


class RecipeFullDataSerializer(serializers.ModelSerializer):
    """Сериализатор рецепта со всеми данными ."""

    image = Base64ImageField(read_only=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    author = UserSerializer(read_only=True)
    tags = TagSerializer(many=True)
    ingredients = RecipeIngredientSerializer(
        source='recipe_ingredients',
        many=True,
        read_only=True
    )

    class Meta:
        model = RecipeModel
        fields = (
            'id', 'tags', 'author', 'ingredients',
            'is_favorited', 'is_in_shopping_cart',
            'name', 'image', 'text', 'cooking_time'
        )

    def get_is_favorited(self, obj):
        """Проверка на наличие рецепта в избранном."""

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


class RecipeShortDataSerializer(serializers.ModelSerializer):
    """Сериализатор рецепта при создании и изменении."""

    image = Base64ImageField()
    ingredients = AddIngredientsSerializer(many=True)

    class Meta:
        model = RecipeModel
        fields = (
            'ingredients', 'tags', 'image',
            'name', 'text', 'cooking_time',
        )

    def _create_ingredients_for_recipe(self, recipe, ingredients):
        """Создаем объект RecipeIngredientModel."""

        recipe_ingredients = []

        # Записываем ингредиенты в список объектов RecipeIngredientModel
        for ingredient_data in ingredients:
            id = ingredient_data['id'].id
            amount = ingredient_data['amount']

            recipe_ingredient = RecipeIngredientModel(
                recipe=recipe,
                ingredient_id=id,
                amount=amount
            )
            recipe_ingredients.append(recipe_ingredient)
        # Сортируем ингредиенты по алфавиту
        sorted_recipe_ingredients = sorted(
            recipe_ingredients,
            key=lambda x: x.ingredient.name
        )

        # Используем bulk_create для добавления всех объектов в базу данных.
        RecipeIngredientModel.objects.bulk_create(sorted_recipe_ingredients)

    def validate(self, obj):
        """Проверка обязательных полей."""
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
        return obj

    def validate_ingredients(self, obj):
        """Проверка на наличие повторяющихся ингредиентов."""

        ingredients = [ing.get('id') for ing in obj]
        if len(ingredients) != len(set(ingredients)):
            raise serializers.ValidationError(
                'Ингредиенты не могут повторяться.'
            )

        # Проверка на наличие ингредиента в БД.
        for ing in ingredients:
            if not IngredientModel.objects.filter(pk=ing.id).exists():
                raise serializers.ValidationError(
                    'Такого ингредиента нет в базе данных.'
                )

        return obj

    def validate_tags(self, tags):
        """Проверка на наличие повторяющихся тегов."""

        tag_ids = [tag.id for tag in tags]
        if len(tag_ids) != len(set(tag_ids)):
            raise serializers.ValidationError('Тэги не могут повторяться.')

        return tags

    def create(self, validated_data):
        """Создаем рецепт."""

        author = self.context['request'].user
        ingredients_data = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')

        recipe = RecipeModel.objects.create(
            author=author,
            **validated_data
        )
        recipe.tags.set(tags)

        self._create_ingredients_for_recipe(recipe, ingredients_data)

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
            # Удаляем все существующие ингредиенты.
            instance.ingredients.clear()
            # Создаем новые ингредиенты в рецепте.
            self._create_ingredients_for_recipe(instance, ingredients_data)

        instance.save()
        return instance

    def to_representation(self, instance):
        """Возвращаемые данные."""

        return RecipeFullDataSerializer(
            instance,
            context={
                'request': self.context.get('request')
            }).data


class FavoriteRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для добавления рецепта в избранное."""

    class Meta:
        model = FavoriteRecipeModel
        fields = '__all__'


class ShowDataAddToFavoriteOrToCartSerializer(serializers.ModelSerializer):
    """
    Сериализатор для отображения добавленного в избранное или корзину.
    """

    class Meta:
        model = RecipeModel
        fields = ('id', 'name', 'image', 'cooking_time',)


class ShoppingCartSerializer(serializers.ModelSerializer):
    """Сериализатор корзины покупок."""

    class Meta:
        model = ShoppingCartModel
        fields = '__all__'
