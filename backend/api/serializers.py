from rest_framework import serializers

from users.models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    '''Вывод данных о пользователях.'''

    class Meta:
        model = CustomUser
        fields = (
            'username', 'email', 'first_name',
            'last_name', 'is'
        )
