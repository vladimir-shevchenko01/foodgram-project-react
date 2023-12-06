from django.core.validators import MinValueValidator
from django.db import models

from components.models import IngredientModel, TagModel
from foodgram.settings import NAME_MAX_LENGTH
from users.models import CustomUser


class RecipeModel(models.Model):
    '''Модель рецепта.'''

    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор рецепта',
    )
    name = models.CharField(
        max_length=NAME_MAX_LENGTH,
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
        IngredientModel,
        through='RecipeIngredientModel',
        verbose_name='Ингредиенты'
    )

    cooking_time = models.IntegerField(
        verbose_name='Время приготовления, мин',
        validators=[MinValueValidator(1)],
    )
    tags = models.ManyToManyField(
        TagModel,
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


class RecipeIngredientModel(models.Model):
    '''Модель связывающая ингридиенты и рецепты.'''

    recipe = models.ForeignKey(
        RecipeModel,
        on_delete=models.CASCADE,
    )
    ingredient = models.ForeignKey(
        IngredientModel,
        on_delete=models.CASCADE,
        verbose_name='Ингредиент'
    )

    amount = models.IntegerField(
        verbose_name='Количество',
        validators=[MinValueValidator(1)]
    )

    class Meta:
        verbose_name = 'Ингредиент в рецепте'
        verbose_name_plural = 'Ингредиенты в рецептах'
        unique_together = ['recipe', 'ingredient']

    def __str__(self):
        return f'Для приготовления {self.recipe} нужно: ' \
               f'{self.ingredient} {self.amount} ' \
               f'{self.ingredient.measurement_unit}'


class FavoriteRecipeModel(models.Model):
    '''Модель для рецептов в избранном.'''
    
    # id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='favorited_by_user',
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        RecipeModel,
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


class ShoppingCartModel(models.Model):
    '''Модель корзины.'''

    # id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='cart_of_user',
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        RecipeModel,
        on_delete=models.CASCADE,
        related_name='recipe_in_cart',
        verbose_name='Рецепт в корзине',
    )

    class Meta:
        verbose_name = 'Корзина с покупками'
        verbose_name_plural = 'Корзины с покупками'
        unique_together = ['user', 'recipe']

    def __str__(self):
        return f'Рецепт {self.recipe} в списке покупок'
