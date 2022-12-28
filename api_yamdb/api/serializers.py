from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from reviews.models import Comment, Review, Title


class CommentSerializer(serializers.ModelSerializer):
    title = serializers.SlugRelatedField(
        read_only=True, slug_field='name')
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username')

    class Meta:
        fields = '__all__'
        model = Comment


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username')

    class Meta:
        fields = '__all__'
        model = Review
        validators = [
            UniqueTogetherValidator(
                queryset=Review.objects.all(),
                fields=['title', 'author'],
                message='Нельзя добавить больше одного'
                        'отзыва на произведение')]
