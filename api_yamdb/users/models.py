import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.exceptions import ValidationError


def generate_uuid(max_length=12) -> str:
    """Генерирует UUID"""
    return uuid.uuid4().hex[:max_length]


def username_not_me(username):
    if username == 'me':
        raise ValidationError('username не может быть \"me\"')


class User(AbstractUser):
    username_validator = UnicodeUsernameValidator()
    username = models.CharField(
        max_length=150,
        unique=True,
        validators=[username_validator, username_not_me],
    )
    email = models.EmailField(
        verbose_name='Email',
        unique=True,
        max_length=254,

    )
    confirmation_code = models.CharField(
        verbose_name='Код подтверждения',
        max_length=50,
        unique=True,
        default=generate_uuid,
    )
    bio = models.TextField(
        verbose_name='Био',
        blank=True,
    )

    class RoleChoice(models.TextChoices):
        USER = 1, 'Пользователь'
        MODERATOR = 2, 'Модератор'
        ADMIN = 3, 'Администратор'

    role = models.IntegerField(
        verbose_name='Роль',
        choices=RoleChoice.choices,
        default=RoleChoice.USER
    )
