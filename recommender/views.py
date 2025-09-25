from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import redirect
from django.views.generic import TemplateView, View

from recommender.services import get_recommendations_for_user


class UserRecommendationsView(LoginRequiredMixin, TemplateView):
    """Страница *Рекомендации для меня* с отображением рассчитанных рекомендаций для данного покупателя."""

    template_name = "recommender/user_recommendations.html"

    def get_context_data(self, **kwargs):
        """ ? """
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['first_name'] = user.first_name
        recommendations = get_recommendations_for_user(user.id)
        context['recommendations'] = recommendations

        return context


class UserRecommendationsAPIView(LoginRequiredMixin, View):
    """ ? """

    def get(self, request, *args, **kwargs):
        """ ? """
        user = self.request.user
        recommendations = get_recommendations_for_user(user.id)

        return JsonResponse(recommendations)


class GenerateUserRecommendationsView(LoginRequiredMixin, View):
    """Высчитывает рекомендации для пользователя и редиректит на страницу с результатами."""

    def get(self, request, *args, **kwargs):
        user = request.user
        # Генерация рекомендаций и кэширование
        get_recommendations_for_user(user.id)
        # Редирект на страницу с рекомендациями
        return redirect("recommender:user_recommendations_page")
