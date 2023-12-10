from django.contrib import admin
from django.utils.html import format_html

from components.models import IngredientModel, TagModel


@admin.register(IngredientModel)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'measurement_unit')
    list_filter = ('name', )
    search_fields = ('name', )


@admin.register(TagModel)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'get_color_of_tag')

    @admin.display(description='Цвет тега')
    def get_color_of_tag(self, obj):
        return format_html(
            '<span style="color: {};">{}</span>',
            obj.color,
            obj.color
        )
