from rest_framework import serializers
from users.models import CustomUser, Subscribe


class UserSerializer(serializers.ModelSerializer):
    '''Вывод данных о пользователях.'''
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = (
            'email', 'id', 
            
            'id', 'username', 'email', 'first_name',
            'last_name', 'is_subscribed'
        )

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return Subscribe.objects.filter(
                user=request.user, author=obj
            ).exists()
        return False


class SubscribeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subscribe
        fields = '__all__'


class SubscriptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subscribe
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['author'] = UserSerializer(instance.author).data  # Включаем данные об авторе
        data['author']['is_subscribed'] = True # Указываем, что мы подписаны на автора
        return data['author']  # Возвращаем модифицированные данные, включая детали об авторе
