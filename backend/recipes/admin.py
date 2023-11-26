from django.contrib import admin

from recipes.models import Recipe, RecipeIngredient


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'author', 'cooking_time', 'text', 'image')
    list_editable = ('cooking_time', 'text', 'image')


@admin.register(RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = (
        'pk', 'recipe', 'ingredient', 'amount'
    )
    list_editable = (
        'recipe', 'ingredient', 'amount'
    )

