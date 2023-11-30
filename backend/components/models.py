from django.core.validators import RegexValidator
from django.db import models


class Ingredient(models.Model):
    '''_____________'''

    name = models.CharField(
        max_length=200,
        verbose_name="Наименование ингредиента",
    )
    measurement_unit = models.CharField(
        max_length=20,
        verbose_name="Единица измерения",
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "Ингредиент"
        verbose_name_plural = "Ингредиенты"
        unique_together = [['name', 'measurement_unit']]

    def __str__(self):
        return self.name


class Tag(models.Model):
    '''_____________'''

    name = models.CharField(
        verbose_name="Наименование тэга",
        max_length=200,
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
        max_length=200,
        verbose_name="Слаг",
        unique=True,
        null=True,
    )

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"

    def __str__(self):
        return self.name
