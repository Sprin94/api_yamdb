from django.contrib.auth import get_user_model
from django.db import models
from users.models import User


class Review(models.Model):
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, verbose_name='Название',
        related_name='reviews')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews',
        verbose_name='Автор')
    text = models.TextField(verbose_name='Текст')
    score = models.IntegerField(
        choices=list(zip(range(1, 11), range(1, 11))))
    pub_date = models.DateTimeField(
        'Дата публикации', auto_now_add=True, db_index=True)

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['pub_date']
        constraints = [models.UniqueConstraint(
            fields=['title', 'author'], name='unic_rev'),]


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['created']
