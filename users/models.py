from django.contrib.auth.models import AbstractUser
from django.db import models

from users.managers import UserManager


class AppUser(AbstractUser):
    """Модель представляет Пользователя/Ппокупателя (авторизация по email)."""

    username = None  # type: ignore
    email = models.EmailField(
        unique=True,
        verbose_name="Почта (username):",
        help_text="Введите email",
    )
    first_name = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Имя:",
        help_text="Укажите имя",
    )
    last_name = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Фамилия:",
        help_text="Укажите фамилию",
    )
    city = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Город:",
        help_text="Укажите город",
    )
    avatar = models.ImageField(
        upload_to="user_avatar",
        blank=True,
        null=True,
        verbose_name="Аватар:",
        help_text="Загрузите аватар",
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    # Указываю кастомный менеджер для пользователя без поля username.
    # Указываю "type: ignore" чтоб убрать ошибку типизации mypy, так как пока не разобрался как правильно
    # работать с типизацией TypeVar.
    objects = UserManager()  # type: ignore

    def __str__(self):
        """Метод определяет строковое представление объекта. Полезно для отображения объектов в админке/консоли."""
        return f"{self.email}"

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ["id"]
