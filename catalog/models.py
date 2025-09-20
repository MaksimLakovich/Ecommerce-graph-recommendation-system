from django.db import models


class Department(models.Model):
    """Модель представляет Департаменты (более общая категория, чем aisle)."""
    dataset_department_id = models.IntegerField(
        unique=True,
        db_index=True,
        verbose_name="ID департамента в датасете:",
        help_text="Введите ID департамента в датасете",
    )
    department = models.CharField(
        max_length=150,
        unique=True,
        verbose_name="Название департамента:",
        help_text="Введите название департамента",
    )

    def __str__(self):
        """Метод определяет строковое представление объекта. Полезно для отображения объектов в админке/консоли."""
        return f"{self.department}"

    class Meta:
        verbose_name = "Департамент"
        verbose_name_plural = "Департаменты"
        ordering = ["id", "dataset_department_id"]


class Aisle(models.Model):
    """Модель представляет Корзину/Ряд (группировка товаров внутри департамента)."""
    dataset_aisle_id = models.IntegerField(
        unique=True,
        db_index=True,
        verbose_name="ID ряда (корзины) в датасете:",
        help_text="Введите ID ряда (корзины)",
    )
    aisle = models.CharField(
        max_length=150,
        unique=True,
        verbose_name="Название ряда (корзины):",
        help_text="Введите название ряда (корзины)",
    )

    def __str__(self):
        """Метод определяет строковое представление объекта. Полезно для отображения объектов в админке/консоли."""
        return f"{self.aisle}"

    class Meta:
        verbose_name = "Ряд"
        verbose_name_plural = "Ряды"
        ordering = ["id", "dataset_aisle_id"]


class Product(models.Model):
    """Модель представляет продукты. Каждый продукт привязан к aisle и department."""
    dataset_product_id = models.IntegerField(
        unique=True,
        db_index=True,
        verbose_name="ID продукта в датасете:",
        help_text="Введите ID продукта",
    )
    product_name = models.CharField(
        max_length=300,
        verbose_name="Название продукта:",
        help_text="Введите название продукта",
    )
    aisle_id = models.ForeignKey(
        to=Aisle,
        on_delete=models.CASCADE,
        related_name="products",
        verbose_name="Ряд продукта:",
        help_text="Укажите ряд продукта",
    )
    department_id = models.ForeignKey(
        to=Department,
        on_delete=models.CASCADE,
        related_name="products",
        verbose_name="Департамент продукта:",
        help_text="Укажите департамент продукта",
    )

    def __str__(self):
        """Метод определяет строковое представление объекта. Полезно для отображения объектов в админке/консоли."""
        return f"{self.product_name}"

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
        ordering = ["id", "dataset_product_id"]
