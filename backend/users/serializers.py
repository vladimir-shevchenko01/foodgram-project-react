import django.contrib.auth.password_validation as validators
from django.core import exceptions
from rest_framework import serializers

import recipes.serializers as Recipe_Serializers
from recipes.models import RecipeModel
from users.models import CustomUser, SubscribeModel


class UserSerializer(serializers.ModelSerializer):
    '''Пользовательский сериали'''

    is_subscribed = serializers.SerializerMethodField()

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return SubscribeModel.objects.filter(
                user=request.user, author=obj
            ).exists()
        return False

    class Meta:
        model = CustomUser
        fields = [
            'email', 'id', 'username',
            'first_name', 'last_name', 'is_subscribed'
        ]


class UserCreateSerializer(serializers.ModelSerializer):
    '''Сериализатор для создания пользователя.'''

    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        # Создание пользователя с автоматическим хешированием пароля.
        user = CustomUser.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        return user

    class Meta:
        model = CustomUser
        fields = [
            'email', 'id', 'username',
            'first_name', 'last_name', 'password',
        ]


class SetNewPasswordSerializer(serializers.Serializer):
    '''Обновить пароль.'''
    current_password = serializers.CharField()
    new_password = serializers.CharField()

    def validate(self, obj):
        '''Валидация пароля.'''
        password = obj.get('new_password')
        errors = {}
        try:
            validators.validate_password(password=password, user=obj)
        except exceptions.ValidationError as e:
            errors['password'] = list(e.messages)
        if errors:
            raise serializers.ValidationError(errors)
        return super(SetNewPasswordSerializer, self).validate(obj)

    def update(self, instance, validated_data):
        '''Обновление пароля.'''
        current_password = validated_data.get('current_password')
        new_password = validated_data.get('new_password')
        # Проверяем введенные данные.
        if not instance.check_password(current_password):
            raise serializers.ValidationError(
                {'current_password': 'Неверный текущий пароль.'}
            )
        elif current_password == new_password:
            raise serializers.ValidationError(
                {'new_password': 'Нельзя использовать старый пароль.'}
            )
        else:
            instance.set_password(validated_data['new_password'])
            instance.save()
            return validated_data


class SubscribeSerializer(serializers.ModelSerializer):
    email = serializers.ReadOnlyField(source='author.email')
    id = serializers.ReadOnlyField(source='author.id')
    username = serializers.ReadOnlyField(source='author.username')
    first_name = serializers.ReadOnlyField(source='author.first_name')
    last_name = serializers.ReadOnlyField(source='author.last_name')
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.ReadOnlyField(source='author.recipes.count')

    class Meta:
        model = SubscribeModel
        fields = (
            'email', 'id',
            'username', 'first_name',
            'last_name', 'is_subscribed',
            'recipes', 'recipes_count'
        )

    def create(self, validated_data):
        """Обработка создания подписки."""

        user = validated_data['user']
        author = validated_data['author']
        if SubscribeModel.objects.filter(user=user, author=author).exists():
            raise serializers.ValidationError(
                'Вы уже подписаны на этого пользователя.'
            )
        return SubscribeModel.objects.create(**validated_data)

    def get_is_subscribed(self, obj):
        return SubscribeModel.objects.filter(
            user=obj.user, author=obj.author
        ).exists()

    def get_recipes(self, obj):
        author = obj.author
        request = self.context.get('request')
        recipe_queryset = RecipeModel.objects.filter(author=author)
        if request and request.GET.get('recipes_limit'):
            limit = request.GET.get('recipes_limit')
            recipe_queryset = recipe_queryset[:int(limit)]
        recipe_serializer = (
            Recipe_Serializers.ShowDataAddToFavoriteOrToCartSerializer(
                recipe_queryset, many=True)
        )
        return recipe_serializer.data
