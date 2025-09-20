from django.db import models

from catalog.models import Product
from users.models import AppUser


class Order(models.Model):
    """Модель представляет заказы."""
    dataset_order_id = models.IntegerField(
        unique=True,
        db_index=True,
        verbose_name="ID заказа в датасете:",
        help_text="Введите ID заказа",
    )
    user_id = models.ForeignKey(
        to=AppUser,
        on_delete=models.CASCADE,
        related_name="orders",
        verbose_name="Владелец заказа:",
        help_text="Укажите владельца заказа",
    )
    order_number = models.PositiveIntegerField(
        blank=False,
        null=False,
        verbose_name="Номер заказа пользователя:",
        help_text="Укажите номер заказа пользователя",
    )
    order_dow = models.IntegerField(
        blank=False,
        null=False,
        verbose_name="День недели в заказе (0 = воскресенье, 1 = понедельник и т.д.):",
        help_text="Укажите день недели в заказе (0 = воскресенье, 1 = понедельник и т.д.)",
    )
    order_hour_of_day = models.IntegerField(
        blank=False,
        null=False,
        verbose_name="Час в заказе (например: 14 = 14:00):",
        help_text="Укажите час в заказе (например: 14 = 14:00)",
    )
    days_since_prior_order = models.IntegerField(
        blank=True,
        null=True,
        verbose_name="Сколько дней прошло с предыдущего заказа:",
        help_text="Укажите сколько дней прошло с предыдущего заказа",
    )

    def __str__(self):
        """Метод определяет строковое представление объекта. Полезно для отображения объектов в админке/консоли."""
        return f"Заказ №{self.dataset_order_id} у покупателя {self.user_id}"

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
        ordering = ["id", "dataset_order_id", "user_id"]


class OrderProduct(models.Model):
    """Модель представляет продукты в заказе (содержимое заказа)."""
    order_id = models.ForeignKey(
        to=Order,
        on_delete=models.CASCADE,
        related_name="order_products",
        verbose_name="ID заказа:",
        help_text="Укажите ID заказа",
    )
    product_id = models.ForeignKey(
        to=Product,
        on_delete=models.CASCADE,
        related_name="order_products",
        verbose_name="ID продуктов в заказе:",
        help_text="Укажите ID продуктов в заказе",
    )
    add_to_cart_order = models.PositiveSmallIntegerField(
        blank=False,
        null=False,
        verbose_name="Порядковый номер добавления товара в корзину:",
        help_text="Укажите порядковый номер добавления товара в корзину",
    )
    reordered = models.PositiveSmallIntegerField(
        blank=False,
        null=False,
        verbose_name="Признак повторной покупки (1 - уже заказывался ранее, 0 - заказан впервые):",
        help_text="Укажите признак повторной покупки (1 - уже заказывался ранее, 0 - заказан впервые)",
    )
