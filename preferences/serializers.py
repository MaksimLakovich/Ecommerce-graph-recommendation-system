from rest_framework import serializers

from preferences.models import UserPreference


class UserPreferenceSerializer(serializers.ModelSerializer):
    """Класс-сериализатор с использованием класса *ModelSerializer* для осуществления базовой сериализация в DRF
    на основе модели UserPreference."""

    class Meta:
        model = UserPreference
        fields = ["product_id", "aisle_id"]
