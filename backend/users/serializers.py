from rest_framework import serializers

from users.models import CustomUser, Subscribe


class UserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        # fields = (
        #     'email', 'id', 'username', 'first_name',
        #     'last_name', 'is_subscribed', 'password'
        # )
        
        fields = ['email',  'id', 'username', 'first_name', 'last_name', 'is_subscribed', 'password']
        read_only_fields = ['is_staff', 'is_superuser']
        
    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)  # Создание пользователя с автоматическим хешированием пароля
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for key, value in validated_data.items():
            setattr(instance, key, value)
        if password:
            instance.set_password(password)  # Обновление пароля с автоматическим хешированием
        instance.save()
        return instance

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
        # Включаем данные об авторе
        # Возвращаем модифицированные данные, включая детали об авторе
        data['author'] = UserSerializer(instance.author).data
        data['author']['is_subscribed'] = True
        return data['author']
