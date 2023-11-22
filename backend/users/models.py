from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    '''
    Кастомная модель пользователя.
    '''
    email = models.EmailField(
        'email',
        max_length=254,
        unique=True,
    )

    first_name = models.CharField(
        'Имя',
        max_length=150,
    )

    last_name = models.CharField(
        'Фамилия',
        max_length=150,
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta:
        verbose_name = 'Пользователь',
        verbose_name_plural = 'Пользователи'
        ordering = ('id',)

    def __str__(self):
        return self.username



class Subscribe(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='subscriber',
        verbose_name='Подписчик'
    )
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='subscribing',
        verbose_name='Подписан'
    )

    def __str__(self):
        return f'{self.user.username} подписан на {self.author.username}'

    class Meta:
        verbose_name = 'Подписка на авторов'
        verbose_name_plural = 'Подписки на авторов'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='unique user author subscription'
            )
        ]
