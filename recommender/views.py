from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.shortcuts import redirect
from django.views.generic import TemplateView, View
from rest_framework import permissions, viewsets
from rest_framework.response import Response

from catalog.models import Aisle, Product
from preferences.models import UserInteraction
from recommender.serializers import UserRecommendationsSerializer
from recommender.services import get_recommendations_for_user


class UserRecommendationsView(LoginRequiredMixin, TemplateView):
    """Вью для отображения страницы "Рекомендации для меня" с отображением рассчитанных рекомендаций для
    данного покупателя.
    Использует метод `get_context_data` для передачи в шаблон:
    - first_name: имя пользователя
    - recommendations: словарь с рекомендациями по алгоритмам PageRank, Collaborative Filtering и kNN."""

    template_name = "recommender/user_recommendations.html"

    def get_context_data(self, **kwargs):
        """Получение контекста для шаблона.
        Возвращает:
            dict: словарь с данными для шаблона, включая имя пользователя и рекомендации."""
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['first_name'] = user.first_name
        recommendations = get_recommendations_for_user(user.id)
        context['recommendations'] = recommendations

        return context


class UserRecommendationsViewSet(viewsets.ViewSet):
    """DRF ViewSet для работы с рекомендациями.
    GET /recommendations/api/recommendations/ возвращает рекомендации текущего пользователя."""

    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        """Возвращает рекомендации текущего пользователя."""
        user = request.user
        recommendations = get_recommendations_for_user(user.id)
        serializer = UserRecommendationsSerializer(recommendations)

        return Response(serializer.data)


class GenerateUserRecommendationsView(LoginRequiredMixin, View):
    """Вью для генерации рекомендаций для текущего пользователя и редиректа на страницу с результатами.
    Используется при нажатии кнопки "Получить рекомендации" на странице предпочтений."""

    def get(self, request, *args, **kwargs):
        """Генерация рекомендаций для текущего пользователя и сохранение в кэш. После генерации выполняется
        редирект на страницу с рекомендациями."""
        user = request.user
        # Генерация рекомендаций и кэширование
        get_recommendations_for_user(user.id)
        # Редирект на страницу с рекомендациями

        return redirect("recommender:user_recommendations_page")


class RecommendationStatisticsView(TemplateView):
    """Страница статистики рекомендаций.
    Отображает:
    - топ-10 продуктов по суммарному весу взаимодействий всех пользователей.
    - топ-5 категорий (aisles) по суммарному весу фиксированых предпочтений среди всех пользователей."""

    template_name = "recommender/recommendation_statistics.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # ШАГ 1: Берем все взаимодействия с продуктами (product_id не NULL) для показа топ-10
        # Суммируем вес (weight) для каждого продукта
        popular_products = (
            UserInteraction.objects
            .filter(product_id__isnull=False)
            .values("product_id")
            .annotate(total_weight=Sum("weight"))
            .order_by("-total_weight")[:10]
        )

        product_ids = [item["product_id"] for item in popular_products]
        products = Product.objects.filter(id__in=product_ids)
        id_to_name = {p.id: p.product_name for p in products}

        top_products = [
            {"name": id_to_name.get(item["product_id"], f"Продукт {item['product_id']}"),
             "weight": item["total_weight"]}
            for item in popular_products
        ]

        context["top_products"] = top_products

        # ШАГ 2: Берем все предпочтения всех покупателей (aisle_id не NULL) для показа топ-5
        # Суммируем вес (weight) для каждой предпочитаемой категории
        popular_aisles = (
            UserInteraction.objects
            .filter(aisle_id__isnull=False)
            .values("aisle_id")
            .annotate(total_weight=Sum("weight"))
            .order_by("-total_weight")[:5]
        )

        aisle_ids = [item["aisle_id"] for item in popular_aisles]
        aisles = Aisle.objects.filter(id__in=aisle_ids)
        id_to_name_aisle = {a.id: a.aisle for a in aisles}

        top_aisles = [
            {"name": id_to_name_aisle.get(item["aisle_id"], f"Категория {item['aisle_id']}"),
             "weight": item["total_weight"]}
            for item in popular_aisles
        ]

        context["top_aisles"] = top_aisles

        return context
