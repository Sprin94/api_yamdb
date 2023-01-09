from django.shortcuts import get_object_or_404

from reviews.models import Title, Review


class TitleDefault:
    requires_context = True

    def __call__(self, serializer_field):
        title_id = serializer_field.context['view'].kwargs.get('title_id')
        return get_object_or_404(Title, pk=title_id)


class ReviewDefault:
    requires_context = True

    def __call__(self, serializer_field):
        review_id = serializer_field.context['view'].kwargs.get('review_id')
        return get_object_or_404(Review, pk=review_id)
