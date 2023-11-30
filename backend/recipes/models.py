from django.core.validators import MinValueValidator
from django.db import models

from components.models import Ingredient, Tag
from users.models import CustomUser


class Recipe(models.Model):
    '''_______________________'''

    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор рецепта',
    )
    name = models.CharField(
        max_length=200,
        verbose_name='Название блюда',
    )
    image = models.ImageField(
        verbose_name='Фото готовоreго блюда',
        upload_to='recipe_image',
    )
    text = models.TextField(
        verbose_name='Описание рецепта',
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        related_name='recipes',
        verbose_name='Ингридиенты',
        through='RecipeIngredient',
    )
    cooking_time = models.IntegerField(
        verbose_name='Время приготовления, мин',
        validators=[MinValueValidator(1)],
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='recipes',
        blank=True,
        verbose_name='Тэги',
    )

    class Meta:
        ordering = ['-id']
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    '''_______________________'''

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
    )
    ingredient = models.ForeignKey(
        Ingredient,
        related_name='recipe_ingredient',
        on_delete=models.CASCADE,
    )
    amount = models.IntegerField(
        verbose_name='Количество',
        validators=[MinValueValidator(1)]
    )

    class Meta:
        unique_together = ['recipe', 'ingredient']

    def __str__(self):
        return f'Для приготовления {self.recipe} нужно: ' \
               f'{self.ingredient} {self.amount} ' \
               f'{self.ingredient.measurement_unit}'


class FavoriteRecipe(models.Model):
    '''_______________________'''

    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='favorited_by_user',
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Избранный рецепт',
    )

    class Meta:
        verbose_name = 'Избранный рецепт'
        verbose_name_plural = 'Избранные рецепты'
        unique_together = ['user', 'recipe']

    def __str__(self):
        return f'{self.user} добавил в избранное  {self.recipe}'


# class ShoppingCart(models.Model):
#     '''_____________'''

#     user = models.ForeignKey(
#         CustomUser,
#         on_delete=models.CASCADE,
#         related_name='users_cart',
#         verbose_name='Пользователь',
#     )
#     recipe = models.ForeignKey(
#         Recipe,
#         on_delete=models.CASCADE,
#         related_name='recipe_in_cart',
#         verbose_name='Избранный рецепт',
#     )

#     class Meta:
#         verbose_name = 'Корзина с покупоками'
#         verbose_name_plural = 'Корзина с покупоками'
#         unique_together = ['user', 'recipe']

#     def __str__(self):
#         return f'Рецепт {self.recipe} в списке покупок'
