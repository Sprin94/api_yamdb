from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from django.db.models import Avg
from django.contrib.auth import get_user_model

from reviews.models import Comment, Review, Title, Genre, Category, Title
from .utils import TitleDefault, ReviewDefault

User = get_user_model()


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all(),
        default=serializers.CurrentUserDefault(),
    )
    review = serializers.PrimaryKeyRelatedField(
        queryset=Title.objects.all(),
        default=ReviewDefault(),
        write_only=True,
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date', 'review')


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all(),
        default=serializers.CurrentUserDefault(),
    )
    title = serializers.PrimaryKeyRelatedField(
        queryset=Title.objects.all(),
        default=TitleDefault(),
        write_only=True,
    )

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date', 'title')
        validators = [
            UniqueTogetherValidator(
                queryset=Review.objects.all(),
                fields=['title', 'author'],
                message='Нельзя добавить больше одного '
                        'отзыва на произведение')]


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
        fields = ('id', 'name', 'year', 'rating', 'description', 'genre',
                  'category')

    def get_rating(self, obj):
        return obj.reviews.aggregate(Avg('score')).get('score__avg')


class TitleGetSerializer(TitleSerializer):
    genre = GenreSerializer(many=True)
    category = CategorySerializer()
