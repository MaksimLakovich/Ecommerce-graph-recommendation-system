from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import TemplateView, View
from rest_framework import permissions, viewsets
from rest_framework.response import Response

from recommender.services import get_recommendations_for_user

from recommender.serializers import UserRecommendationsSerializer


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
