from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404

from reviews.models import Comment, Review, Title


class CommentSerializer(serializers.ModelSerializer):
    title = serializers.SlugRelatedField(
        read_only=True, slug_field='name')
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username')

    def validate(self, data):
        request = self.context['request']
        title = get_object_or_404(
            Title, pk=self.context['view'].kwargs.get('title_id'))
        if request.method == 'POST':
            if Review.objects.filter(title=title,
                                     author=request.user).exists():
                raise ValidationError('Нельзя добавить больше одного'
                                      'отзыва на произведение')
        return data

    class Meta:
        fields = '__all__'
        model = Comment


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username')

    class Meta:
        fields = '__all__'
        model = Review
