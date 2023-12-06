from rest_framework import serializers

from components.models import IngredientModel, TagModel
from recipes.models import RecipeIngredientModel


class IngredientSerializer(serializers.ModelSerializer):
    '''Сериализатор ингредиента.'''

    class Meta:
        model = IngredientModel
        fields = '__all__'


class AddIngredientsSerializer(serializers.ModelSerializer):
    '''_________________________'''
    id = serializers.IntegerField()

    class Meta:
        model = RecipeIngredientModel
        fields = ('id', 'amount')


class TagSerializer(serializers.ModelSerializer):
    '''Сериализатор тэга.'''

    class Meta:
        model = TagModel
        fields = '__all__'
