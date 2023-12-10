from django.contrib import admin

from recipes.models import RecipeIngredientModel, RecipeModel


class RecipeIngredientAdmin(admin.StackedInline):
    model = RecipeIngredientModel
    autocomplete_fields = ('ingredient',)


@admin.register(RecipeModel)
class RecipeAdmin(admin.ModelAdmin):
    inlines = [RecipeIngredientAdmin]
    list_display = ('pk', 'name', 'text', 'author')
    list_editable = (
        'name', 'text', 'author'
    )
    list_filter = ('name', 'author', 'tags')
    empty_value_display = '-пусто-'


@admin.register(RecipeIngredientModel)
class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = (
        'pk', 'recipe', 'ingredient', 'amount'
    )
    list_editable = (
        'recipe', 'ingredient', 'amount'
    )
