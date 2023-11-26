from rest_framework import serializers

from recipes.models import Recipe, RecipeIngredient


class RecipeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = '__all__'


class RecipeIngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = RecipeIngredient
        fields = '__all__'
