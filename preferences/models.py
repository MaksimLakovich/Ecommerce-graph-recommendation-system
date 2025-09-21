from django.db import models

from catalog.models import Aisle, Product
from users.models import AppUser


class UserInteraction(models.Model):
    """Универсальная таблица всех взаимодействий пользователя. Таблица хранит:
    1) как "explicit-события" (т.е., то что пользователь самостоятельно выберет на странице в качестве "Предпочтения").
    2) так и "implicit-события" (т.е., данные из покупок пользователя в датасете - это "add_to_cart", "reorder")."""

    # Набор типов взаимодействия, которые мы сейчас учитываем
    INTERACTION_CHOICES = [
        ("purchase", "Купленный продукт"),  # это все купленные продукты из "order_products_all_sample.csv"
        ("reorder", "Повторная покупка"),  # признак повторной покупки продукта (в датасете есть флаг reordered)
        # # просто для инфо: вот так потом можно расширить модель если в будущем появятся такие данные в БД/датасете
        # ("like", "Лайк продукту"),
        # ("view", "Просмотр продукта"),
        # ("add_to_cart", "Добавлен в корзину но не куплен"),
        ("preference", "Предпочтение пользователя"),  # явный выбор пользователя на странице "Ваши предпочтения"
    ]

    SOURCE_CHOICES = [
        ("implicit", "Неявные - извлечено из истории заказов"),  # То, что извлечено из истории заказов
        ("explicit", "Явные - задано пользователем"),  # То, что задано пользователем на странице "Ваши предпочтения"
    ]

    user_id = models.ForeignKey(
        to=AppUser,
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        related_name="interactions",
    )
    # Взаимодействие может быть про продукт (это то что в implicit) или про категорию/aisle (это уже explicit)
    product_id = models.ForeignKey(
        to=Product,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )
    aisle_id = models.ForeignKey(
        to=Aisle,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    interaction_type = models.CharField(
        max_length=100,
        null=False,
        blank=False,
        choices=INTERACTION_CHOICES,
    )
    source = models.CharField(
        max_length=100,
        null=False,
        blank=False,
        choices=SOURCE_CHOICES,
        default="implicit",
    )
    # Вес события - можно назначать разный для purchase/reorder/explicit-preference и т.д. Лайков в будущем например
    weight = models.FloatField(
        null=False,
        blank=False,
        default=1.0
    )

    def __str__(self):
        """Метод определяет строковое представление объекта. Полезно для отображения объектов в админке/консоли."""
        target = self.product_id or self.aisle_id or "—"
        return f"{self.user_id} / {self.interaction_type} / {target}"

    def save(self, *args, **kwargs):
        """Автоматически выставляем вес взаимодействия в зависимости от типа:
        - "Купленный продукт"
        - "Повторная покупка"
        - "Предпочтение пользователя"
        """
        if self.interaction_type == "purchase":
            self.weight = 1.0
        elif self.interaction_type == "reorder":
            self.weight = 2.0
        elif self.interaction_type == "preference":
            self.weight = 5.0
        else:
            self.weight = 0.5  # для всех остальных, если потом будут новые типы и я их тут явно не укажу
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Взаимодействие пользователя"
        verbose_name_plural = "Взаимодействия пользователей"
        indexes = [
            models.Index(fields=["user_id", "product_id"]),
            models.Index(fields=["user_id", "aisle_id"]),
        ]


class UserPreference(models.Model):
    """Явные предпочтения покупателя, которые он указал самостоятельно на странице "Мои предпочтения"."""

    user_id = models.ForeignKey(
        to=AppUser,
        on_delete=models.CASCADE,
        related_name="preferences",
    )
    product_id = models.ForeignKey(
        to=Product,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )
    aisle_id = models.ForeignKey(
        to=Aisle,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    def __str__(self):
        """Метод определяет строковое представление объекта. Полезно для отображения объектов в админке/консоли."""
        target = self.product_id or self.aisle_id or "—"
        return f"{self.user_id} → {target}"

    class Meta:
        verbose_name = "Явное предпочтение"
        verbose_name_plural = "Явные предпочтения"
        # Дополнительно: запретить дублирование одного и того же явного предпочтения
        constraints = [
            models.UniqueConstraint(fields=["user_id", "product_id"], name="unique_user_product_pref"),
            models.UniqueConstraint(fields=["user_id", "aisle_id"], name="unique_user_aisle_pref"),
        ]
