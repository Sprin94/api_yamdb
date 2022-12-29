from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Category(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        ordering = ('-id',)


class Genre(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        ordering = ('-id',)


class Title(models.Model):
    name = models.CharField(max_length=256)
    year = models.IntegerField()
    rating = models.IntegerField(
        default=None
    )
    description = models.TextField()
    genre = models.ForeignKey(
        Genre,
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )
    category = models.OneToOneField(
        Category,
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )
