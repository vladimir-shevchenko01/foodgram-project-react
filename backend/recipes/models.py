from django.core.validators import MinValueValidator
from django.db import models

from components.models import Ingredient, Tag
from users.models import CustomUser


class Recipe(models.Model):
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор рецепта',
    )
    recipe_name = models.CharField(
        max_length=200,
        verbose_name='Название блюда',
    )
    image = models.ImageField(
        verbose_name='Фото готового блюда',
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
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации',
    )

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
    )
    ingredient = models.ForeignKey(
        Ingredient,
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
