from django.contrib import admin

from preferences.models import UserInteraction, UserPreference


@admin.register(UserInteraction)
class AdminUserInteraction(admin.ModelAdmin):
    """Настройка отображения данных модели UserInteraction в админке."""
    list_display = (
        "id",
        "user_id",
        "product_id",
        "aisle_id",
        "interaction_type",
        "source",
        "weight",
    )
    list_filter = ("interaction_type", "source",)
    search_fields = (
        "user_id__email",
        "interaction_type",
        "source",
    )


@admin.register(UserPreference)
class AdminUserPreference(admin.ModelAdmin):
    """Настройка отображения данных модели UserPreference в админке."""
    list_display = (
        "id",
        "user_id",
        "product_id",
        "aisle_id",
    )
    list_filter = ("user_id",)
    search_fields = (
        "user_id__email",
    )
