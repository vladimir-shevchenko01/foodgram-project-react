from django.contrib import admin

from recipes.models import Recipe, RecipeIngredient


class RecipeTagInline(admin.TabularInline):
    model = Recipe.tags.through


class RecipeIngredientAdmin(admin.StackedInline):
    model = RecipeIngredient
    autocomplete_fields = ('ingredient',)


class RecipeIngredientsInline(admin.TabularInline):
    model = Recipe.ingredients.through


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = [RecipeTagInline, RecipeIngredientAdmin]
    list_display = ('pk', 'name', 'author')
    list_editable = (
        'name', 'author'
    )
    list_filter = ('name', 'author', 'tags')
    empty_value_display = '-пусто-'




@admin.register(RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = (
        'pk', 'recipe', 'ingredient', 'amount'
    )
    list_editable = (
        'recipe', 'ingredient', 'amount'
    )
