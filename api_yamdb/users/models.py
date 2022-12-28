import uuid

from django.core.mail import send_mail
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.exceptions import ValidationError


def generate_uuid(max_length=12) -> str:
    """Генерирует UUID"""
    return uuid.uuid4().hex[:max_length]


def username_not_me(username):
    if username == 'me':
        raise ValidationError('username не может быть "me"')


class UserManager(BaseUserManager):

    def create_user(self, username, email, password=None,
                    role='user', bio=''):
        """ Создает и возвращает пользователя с email и именем. """

        if username is None:
            raise TypeError('Users must have a username.')

        if email is None:
            raise TypeError('Users must have an email address.')

        user = self.model(
            username=username,
            email=self.normalize_email(email),)

        code = generate_uuid()
        if password is None:
            password = code

        user.set_password(password)
        user.is_superuser = False
        user.is_staff = False
        user.confirmation_code = code
        user.role = role
        user.bio = bio
        user.save()
        send_mail(
            'Код для получения токена',
            f'Код для получения JWT токена: {code}',
            'yamdb@gmail.com',
            [email],
            fail_silently=False,
        )
        return user

    def create_superuser(self, username, email, password):
        """ Создает и возвращает пользователя с привилегиями суперадмина."""

        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.role = User.RoleChoice.ADMIN
        user.save()

        return user


class User(AbstractUser):
    "Пользовательская модель юзера"
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
        null=True,
    )
    bio = models.TextField(
        verbose_name='Био',
        blank=True,
    )

    class RoleChoice(models.TextChoices):
        USER = 'user', 'Пользователь'
        MODERATOR = 'moderator', 'Модератор'
        ADMIN = 'admin', 'Администратор'

    role = models.CharField(
        verbose_name='Роль',
        choices=RoleChoice.choices,
        default=RoleChoice.USER,
        max_length=10
    )

    objects = UserManager()

    def __str__(self):
        return self.username
