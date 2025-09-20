from django.contrib import admin

from catalog.models import Aisle, Department, Product


@admin.register(Department)
class AdminDepartment(admin.ModelAdmin):
    """Настройка отображения данных модели Department в админке."""
    list_display = (
        "id",
        "dataset_department_id",
        "department",
    )
    list_filter = ("department",)
    search_fields = (
        "dataset_department_id",
        "department",
    )


@admin.register(Aisle)
class AdminAisle(admin.ModelAdmin):
    """Настройка отображения данных модели Aisle в админке."""
    list_display = (
        "id",
        "dataset_aisle_id",
        "aisle",
    )
    list_filter = ("aisle",)
    search_fields = (
        "dataset_aisle_id",
        "aisle",
    )


@admin.register(Product)
class AdminProduct(admin.ModelAdmin):
    """Настройка отображения данных модели Product в админке."""
    list_display = (
        "id",
        "dataset_product_id",
        "product_name",
        "aisle_id",
        "department_id",
    )
    list_filter = (
        "product_name",
        "aisle_id",
        "department_id",
    )
    search_fields = (
        "dataset_product_id",
        "product_name",
        "aisle__aisle",
        "department__department",
    )
