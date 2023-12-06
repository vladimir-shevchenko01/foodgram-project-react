from django.core.validators import RegexValidator
from django.db import models

from foodgram.settings import (
    MEASUREMENT_UNIT_MAX_LENGTH, NAME_MAX_LENGTH, SLUG_MAX_LENGTH
)


class IngredientModel(models.Model):
    '''Модель ингредиента.'''

    name = models.CharField(
        max_length=NAME_MAX_LENGTH,
        verbose_name="Наименование ингредиента",
    )
    measurement_unit = models.CharField(
        max_length=MEASUREMENT_UNIT_MAX_LENGTH,
        verbose_name="Единица измерения",
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "Ингредиент"
        verbose_name_plural = "Ингредиенты"
        unique_together = ['name', 'measurement_unit']

    def __str__(self):
        return f'{self.name}, {self.measurement_unit}.'


class TagModel(models.Model):
    '''Модель тэга.'''

    name = models.CharField(
        verbose_name="Наименование тэга",
        max_length=NAME_MAX_LENGTH,
    )
    color = models.CharField(
        max_length=7,
        null=True,
        verbose_name="HEX code - цвет",
        validators=[
            RegexValidator(
                regex="^#[0-9A-Fa-f]{6}$",
                message="Введите корректный цвет в формате HEX",
                code="invalid_color",
            )
        ],
    )
    slug = models.SlugField(
        max_length=SLUG_MAX_LENGTH,
        verbose_name="Слаг",
        unique=True,
        null=True,
    )

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"

    def __str__(self):
        return self.name
