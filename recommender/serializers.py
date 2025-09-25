from rest_framework import serializers


class UserRecommendationsSerializer(serializers.Serializer):
    """Сериализатор для представления рекомендаций пользователя по трем алгоритмам:
    - PageRank
    - Collaborative Filtering
    - k-Nearest Neighbors (kNN)
    Используется для отдачи JSON через DRF API."""

    pagerank = serializers.ListField(
        child=serializers.CharField(),
        help_text="Список рекомендованных продуктов по алгоритму PageRank"
    )
    collaborative = serializers.ListField(
        child=serializers.CharField(),
        help_text="Список рекомендованных продуктов по алгоритму Collaborative Filtering"
    )
    knn = serializers.ListField(
        child=serializers.CharField(),
        help_text="Список рекомендованных продуктов по алгоритму k-Nearest Neighbors (kNN)"
    )


class PopularProductSerializer(serializers.Serializer):
    """Сериализатор для представления популярных продуктов.
    Поля:
        - product_name: название продукта
        - total_weight: суммарный вес взаимодействий"""

    product_name = serializers.CharField()
    total_weight = serializers.FloatField()


class PopularAisleSerializer(serializers.Serializer):
    """Сериализатор для представления популярных категорий (aisles).
    Поля:
        - aisle_name: название категории
        - total_weight: суммарный вес взаимодействий"""

    aisle_name = serializers.CharField()
    total_weight = serializers.FloatField()
