from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from rest_framework import permissions, viewsets

from preferences.forms import UserPreferencesForm
from preferences.models import UserInteraction, UserPreference
from recommender.services import reset_recommendations_cache

from .serializers import UserPreferenceSerializer


class UserPreferencesView(LoginRequiredMixin, FormView):
    """Страница 'Мои предпочтения' с выбором товарных предпочтений покупателем."""

    template_name = "preferences/user_preferences.html"
    form_class = UserPreferencesForm
    success_url = reverse_lazy("preferences:user_preferences_page")

    def get_initial(self):
        """Подставляем ранее выбранные aisles пользователя."""
        initial = super().get_initial()
        user_aisles = UserPreference.objects.filter(user_id=self.request.user).values_list(
            "aisle_id", flat=True
        )
        initial["aisles"] = user_aisles
        return initial

    def form_valid(self, form):
        """Сохраняем выбранные aisles и обновляем UserPreference и UserInteraction."""
        user = self.request.user
        aisles = form.cleaned_data["aisles"]

        # Удаляем старые предпочтения и взаимодействия для типа "preference" потому что будем их перезаписывать
        # после того как покупатель снова что-то зафиксировал
        UserPreference.objects.filter(user_id=user).delete()
        UserInteraction.objects.filter(user_id=user, interaction_type="preference").delete()

        # Создаем новые актуальные предпочтения
        for aisle in aisles:
            UserPreference.objects.create(user_id=user, aisle_id=aisle)

            UserInteraction.objects.create(
                user_id=user,
                aisle_id=aisle,
                product_id=None,
                interaction_type="preference",
                source="explicit",
            )

        return super().form_valid(form)


class UserPreferencesViewSet(viewsets.ModelViewSet):
    """API-вью для управления предпочтениями пользователя."""

    serializer_class = UserPreferenceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Показываем только предпочтения текущего пользователя
        return UserPreference.objects.filter(user_id=self.request.user)

    def perform_create(self, serializer):
        # Сохраняем UserPreference с привязкой к текущему пользователю
        preference = serializer.save(user_id=self.request.user)

        # Создаём UserInteraction
        UserInteraction.objects.create(
            user_id_id=self.request.user.id,
            product_id_id=preference.product_id_id,
            aisle_id_id=preference.aisle_id_id,
            interaction_type="preference",
            source="explicit",
            weight=5.0
        )

        # Сбрасываем кэш рекомендаций
        reset_recommendations_cache(self.request.user.id)
