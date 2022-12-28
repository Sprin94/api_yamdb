from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)


class Genre(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

class Title(models.Model):
    name = models.CharField(max_length=256)
    year = models.IntegerField()
    rating = models.IntegerField()
    description = models.TextField()
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE
    )
    category = models.OneToOneField(
        Category,
        on_delete=models.CASCADE
    )