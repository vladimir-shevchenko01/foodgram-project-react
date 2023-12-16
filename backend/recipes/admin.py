from django.contrib import admin

from recipes.models import (FavoriteRecipeModel, RecipeIngredientModel,
                            RecipeModel, ShoppingCartModel)


class RecipeIngredientAdmin(admin.StackedInline):
    """Для отображения ингредиентов в рецептах."""

    model = RecipeIngredientModel
    autocomplete_fields = ('ingredient',)
    min_num = 1
    extra = 1


class RecipeTagInline(admin.TabularInline):
    """Для отображения тэгов в рецептах."""

    model = RecipeModel.tags.through
    extra = 1


@admin.register(RecipeModel)
class RecipeAdmin(admin.ModelAdmin):

    inlines = [RecipeIngredientAdmin, RecipeTagInline]
    list_display = (
        'pk', 'name', 'text', 'author',
        'display_ingredients', 'display_tags'
    )
    list_editable = (
        'name', 'text', 'author'
    )
    list_filter = ('name', 'author', 'tags',)
    search_fields = ('name', 'text', 'author__username',)
    empty_value_display = '-пусто-'

    @admin.display(description='Ингредиенты')
    def display_ingredients(self, obj):
        return ', '.join(
            [ingredient.name for ingredient in obj.ingredients.all()]
        )

    @admin.display(description='Тэги')
    def display_tags(self, obj):
        return ', '.join([tag.name for tag in obj.tags.all()])


@admin.register(RecipeIngredientModel)
class RecipeIngredientAdmin(admin.ModelAdmin):

    list_display = (
        'pk', 'recipe', 'ingredient', 'amount',
    )
    list_editable = (
        'recipe', 'ingredient', 'amount',
    )


@admin.register(ShoppingCartModel)
class ShoppingCartAdmin(admin.ModelAdmin):

    list_display = ('user', 'recipe',)


@admin.register(FavoriteRecipeModel)
class FavoriteAdmin(admin.ModelAdmin):

    list_display = ('user', 'recipe',)
