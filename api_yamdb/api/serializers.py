from rest_framework import serializers

from reviews import models


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Genre
        fields = ('name', 'slug')


class TitleSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        slug_field='genre', 
        queryset=models.Genre.objects.all(),
        many=True)
    

    class Meta:
        model = models.Title
        fields = ('id', 'name', 'year', 'rating', 'description', 'genre', 'category')
