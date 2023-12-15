from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import CustomUser, SubscribeModel


@admin.register(CustomUser)
class UserAdmin(UserAdmin):

    list_display = (
        'username', 'pk', 'email',
        'get_subscribers_count',
        'get_recipes_count',
        'first_name',
        'last_name',
    )
    list_filter = ('username', 'email', )
    search_fields = ('username', 'email', )
    exclude = ('Token', 'Groups', )
    empty_value_display = '-пусто-'

    def get_subscribers_count(self, obj):
        # Получаем число подписчиков.
        return obj.subscribing.count()
    get_subscribers_count.short_description = 'Число подписчиков'

    def get_recipes_count(self, obj):
        # Получаем число рецептов.
        return obj.recipes.count()
    get_recipes_count.short_description = 'Число рецептов'

    def save_model(self, request, obj, form, change):
        # Для изменения пароля используйте set_password.
        if 'password' in form.changed_data:
            obj.set_password(form.cleaned_data['password'])
        obj.save()


@admin.register(SubscribeModel)
class SubscribeAdmin(admin.ModelAdmin):

    list_display = ('pk', 'user', 'author')
    list_editable = ('user', 'author')
    empty_value_display = '-пусто-'
