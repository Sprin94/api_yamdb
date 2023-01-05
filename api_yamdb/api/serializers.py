from django.db.models import Avg
from rest_framework import serializers

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
        many=True,
        queryset=Genre.objects.all()
    )

    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )
    
    rating = serializers.SerializerMethodField()
    
    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'rating', 'description', 'genre', 'category')

    def get_rating(self, obj):
        return obj.reviews.aggregate(Avg('rating'))
