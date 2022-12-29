from rest_framework import serializers
from statistics import mean

from reviews.models import Genre, Category, Title


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        slug_field='slug', 
        queryset=Genre.objects.all(),
        many=True)

    
    rating = serializers.SerializerMethodField()
    
    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'rating', 'description', 'genre', 'category')

    def get_rating(self, obj):
        reviews = obj.reviews.all()

        scores = []

        for review in reviews:
            scores.append(review.score)

        return round(mean(scores))
