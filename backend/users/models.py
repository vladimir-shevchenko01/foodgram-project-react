from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models

from foodgram.settings import EMAIL_LENGTH_FIELD, NAME_MAX_LENGTH


class CustomUser(AbstractUser):
    """Кастомная модель пользователя."""

    email = models.EmailField(
        max_length=EMAIL_LENGTH_FIELD,
        verbose_name='email',
        unique=True,
    )

    first_name = models.CharField(
        max_length=NAME_MAX_LENGTH,
        verbose_name='Имя',
    )

    last_name = models.CharField(
        max_length=NAME_MAX_LENGTH,
        verbose_name='Фамилия',
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta:
        verbose_name = 'Пользователь',
        verbose_name_plural = 'Пользователи'
        ordering = ('id',)

    def __str__(self):
        return self.username


class SubscribeModel(models.Model):
    """Модель подписки."""

    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='subscriber',
        verbose_name='Пользователь - подписчик'
    )
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='subscribing',
        verbose_name='Автор на которого подписывается пользователь'
    )

    def __str__(self):
        return f'{self.user.username} подписан на {self.author.username}'

    class Meta:
        verbose_name = 'Подписка на авторов'
        verbose_name_plural = 'Подписки на авторов'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='unique_user_author_subscription'
            )
        ]

    def clean(self):
        # Проверяем, чтобы пользователь не
        # смог подписаться на самого себя.
        if self.user == self.author:
            raise ValidationError(
                'Пользователь не может подписаться на самого себя.'
            )
