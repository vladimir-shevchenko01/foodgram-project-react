from rest_framework import serializers

from components.models import IngredientModel, TagModel
from foodgram.settings import MAX_VALUE, MIN_VALUE


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор ингредиента."""

    class Meta:
        model = IngredientModel
        fields = '__all__'


class AddIngredientsSerializer(serializers.ModelSerializer):
    """Сериализатор для добавленя ингредиента."""
    id = serializers.PrimaryKeyRelatedField(
        queryset=IngredientModel.objects.all(),
    )
    amount = serializers.IntegerField(
        min_value=MIN_VALUE,
        max_value=MAX_VALUE
    )

    class Meta:
        model = IngredientModel
        fields = ('id', 'amount')


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор тэга."""

    class Meta:
        model = TagModel
        fields = '__all__'
