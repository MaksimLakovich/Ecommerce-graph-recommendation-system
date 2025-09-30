from django.contrib import admin

from orders.models import Order, OrderProduct


@admin.register(Order)
class AdminOrder(admin.ModelAdmin):
    """Настройка отображения данных модели Order в админке."""
    list_display = (
        "id",
        "dataset_order_id",
        "user_id",
        "order_number",
        "order_dow",
        "order_hour_of_day",
        "days_since_prior_order",
    )
    list_filter = ("dataset_order_id",)
    search_fields = (
        "dataset_order_id",
        "user__email",
    )


@admin.register(OrderProduct)
class AdminOrderProduct(admin.ModelAdmin):
    """Настройка отображения данных модели OrderProduct в админке."""
    list_display = (
        "id",
        "order_id",
        "product_id",
        "add_to_cart_order",
        "reordered",
    )
    list_filter = ("order_id", "product_id", "reordered",)
    search_fields = (
        "order__dataset_order_id",
        "product__product_name",
        "reordered",
    )
