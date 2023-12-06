from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import CustomUser, SubscribeModel


# admin.site.register(CustomUser)
@admin.register(CustomUser)
class UserAdmin(admin.ModelAdmin):
    
    def save_model(self, request, obj, form, change):
        obj.set_password(obj.password)
        obj.save()

    list_display = (
        'username', 'pk', 'email', 'password', 'first_name', 'last_name',
    )
    list_filter = ('username', 'email')
    search_fields = ('username', 'email')
    empty_value_display = '-пусто-'



@admin.register(SubscribeModel)
class SubscribeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'author')
    list_editable = ('user', 'author')
    empty_value_display = '-'
